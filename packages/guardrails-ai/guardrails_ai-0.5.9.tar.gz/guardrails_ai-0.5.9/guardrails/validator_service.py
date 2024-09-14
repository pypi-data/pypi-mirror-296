import asyncio
import itertools
import os
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from typing import Any, Awaitable, Dict, Iterable, List, Optional, Tuple, Union, cast

from guardrails.actions.filter import Filter, apply_filters
from guardrails.actions.refrain import Refrain, apply_refrain
from guardrails.classes.history import Iteration
from guardrails.classes.output_type import OutputTypes
from guardrails.classes.validation.validation_result import (
    FailResult,
    PassResult,
    StreamValidationResult,
    ValidationResult,
)
from guardrails.errors import ValidationError
from guardrails.merge import merge
from guardrails.types import ValidatorMap, OnFailAction
from guardrails.utils.exception_utils import UserFacingException
from guardrails.utils.hub_telemetry_utils import HubTelemetry
from guardrails.classes.validation.validator_logs import ValidatorLogs
from guardrails.actions.reask import FieldReAsk, ReAsk
from guardrails.telemetry.legacy_validator_tracing import trace_validation_result
from guardrails.telemetry import trace_validator
from guardrails.validator_base import Validator

ValidatorResult = Optional[Union[ValidationResult, Awaitable[ValidationResult]]]


def key_not_empty(key: str) -> bool:
    return key is not None and len(str(key)) > 0


class ValidatorServiceBase:
    """Base class for validator services."""

    def __init__(self, disable_tracer: Optional[bool] = True):
        self._disable_tracer = disable_tracer

    # NOTE: This is avoiding an issue with multiprocessing.
    #       If we wrap the validate methods at the class level or anytime before
    #       loop.run_in_executor is called, multiprocessing fails with a Pickling error.
    #       This is a well known issue without any real solutions.
    #       Using `fork` instead of `spawn` may alleviate the symptom for POSIX systems,
    #       but is relatively unsupported on Windows.
    def execute_validator(
        self,
        validator: Validator,
        value: Any,
        metadata: Optional[Dict],
        stream: Optional[bool] = False,
        *,
        validation_session_id: str,
        **kwargs,
    ) -> ValidatorResult:
        validate_func = validator.validate_stream if stream else validator.validate
        traced_validator = trace_validator(
            validator_name=validator.rail_alias,
            obj_id=id(validator),
            on_fail_descriptor=validator.on_fail_descriptor,
            validation_session_id=validation_session_id,
            **validator._kwargs,
        )(validate_func)
        if stream:
            result = traced_validator(value, metadata, **kwargs)
        else:
            result = traced_validator(value, metadata)
        return result

    def perform_correction(
        self,
        results: List[FailResult],
        value: Any,
        validator: Validator,
        on_fail_descriptor: Union[OnFailAction, str],
        rechecked_value: Optional[ValidationResult] = None,
    ):
        if on_fail_descriptor == OnFailAction.FIX:
            # FIXME: Should we still return fix_value if it is None?
            # I think we should warn and return the original value.
            return results[0].fix_value
        elif on_fail_descriptor == OnFailAction.FIX_REASK:
            # FIXME: Same thing here
            fixed_value = results[0].fix_value

            if isinstance(rechecked_value, FailResult):
                return FieldReAsk(
                    incorrect_value=fixed_value,
                    fail_results=results,
                )

            return fixed_value
        if on_fail_descriptor == "custom":
            if validator.on_fail_method is None:
                raise ValueError("on_fail is 'custom' but on_fail_method is None")
            return validator.on_fail_method(value, results)
        if on_fail_descriptor == OnFailAction.REASK:
            return FieldReAsk(
                incorrect_value=value,
                fail_results=results,
            )
        if on_fail_descriptor == OnFailAction.EXCEPTION:
            raise ValidationError(
                "Validation failed for field with errors: "
                + ", ".join([result.error_message for result in results])
            )
        if on_fail_descriptor == OnFailAction.FILTER:
            return Filter()
        if on_fail_descriptor == OnFailAction.REFRAIN:
            return Refrain()
        if on_fail_descriptor == OnFailAction.NOOP:
            return value
        else:
            raise ValueError(
                f"Invalid on_fail_descriptor {on_fail_descriptor}, "
                f"expected 'fix' or 'exception'."
            )

    def before_run_validator(
        self,
        iteration: Iteration,
        validator: Validator,
        value: Any,
        absolute_property_path: str,
    ) -> ValidatorLogs:
        validator_class_name = validator.__class__.__name__
        validator_logs = ValidatorLogs(
            validator_name=validator_class_name,
            value_before_validation=value,
            registered_name=validator.rail_alias,
            property_path=absolute_property_path,
            # If we ever re-use validator instances across multiple properties,
            #   this will have to change.
            instance_id=id(validator),
        )
        iteration.outputs.validator_logs.append(validator_logs)

        start_time = datetime.now()
        validator_logs.start_time = start_time

        return validator_logs

    def after_run_validator(
        self,
        validator: Validator,
        validator_logs: ValidatorLogs,
        result: Optional[ValidationResult],
    ):
        end_time = datetime.now()
        validator_logs.validation_result = result
        validator_logs.end_time = end_time

        if not self._disable_tracer:
            # Get HubTelemetry singleton and create a new span to
            # log the validator usage
            _hub_telemetry = HubTelemetry()
            _hub_telemetry.create_new_span(
                span_name="/validator_usage",
                attributes=[
                    ("validator_name", validator.rail_alias),
                    ("validator_on_fail", validator.on_fail_descriptor),
                    (
                        "validator_result",
                        result.outcome
                        if isinstance(result, ValidationResult)
                        else None,
                    ),
                ],
                is_parent=False,  # This span will have no children
                has_parent=True,  # This span has a parent
            )

        return validator_logs

    def run_validator(
        self,
        iteration: Iteration,
        validator: Validator,
        value: Any,
        metadata: Dict,
        absolute_property_path: str,
        stream: Optional[bool] = False,
        **kwargs,
    ) -> ValidatorLogs:
        raise NotImplementedError


class SequentialValidatorService(ValidatorServiceBase):
    def run_validator_sync(
        self,
        validator: Validator,
        value: Any,
        metadata: Dict,
        validator_logs: ValidatorLogs,
        stream: Optional[bool] = False,
        *,
        validation_session_id: str,
        **kwargs,
    ) -> Optional[ValidationResult]:
        result = self.execute_validator(
            validator,
            value,
            metadata,
            stream,
            validation_session_id=validation_session_id,
            **kwargs,
        )
        if asyncio.iscoroutine(result):
            raise UserFacingException(
                ValueError(
                    "Cannot use async validators with a synchronous Guard! "
                    f"Either use AsyncGuard or remove {validator_logs.validator_name}."
                )
            )
        if result is None:
            return result
        return cast(ValidationResult, result)

    def run_validator(
        self,
        iteration: Iteration,
        validator: Validator,
        value: Any,
        metadata: Dict,
        property_path: str,
        stream: Optional[bool] = False,
        **kwargs,
    ) -> ValidatorLogs:
        validator_logs = self.before_run_validator(
            iteration, validator, value, property_path
        )

        result = self.run_validator_sync(
            validator,
            value,
            metadata,
            validator_logs,
            stream,
            validation_session_id=iteration.id,
            **kwargs,
        )

        return self.after_run_validator(validator, validator_logs, result)

    def run_validators_stream(
        self,
        iteration: Iteration,
        validator_map: ValidatorMap,
        value_stream: Iterable[Tuple[Any, bool]],
        metadata: Dict[str, Any],
        absolute_property_path: str,
        reference_property_path: str,
        **kwargs,
    ) -> Iterable[StreamValidationResult]:
        validators = validator_map.get(reference_property_path, [])
        for validator in validators:
            if validator.on_fail_descriptor == OnFailAction.FIX:
                return self.run_validators_stream_fix(
                    iteration,
                    validator_map,
                    value_stream,
                    metadata,
                    absolute_property_path,
                    reference_property_path,
                    **kwargs,
                )
        return self.run_validators_stream_noop(
            iteration,
            validator_map,
            value_stream,
            metadata,
            absolute_property_path,
            reference_property_path,
            **kwargs,
        )

    # requires at least 2 validators
    def multi_merge(self, original: str, new_values: list[str]) -> str:
        current = new_values.pop()
        print("Fmerging these:", new_values)
        while len(new_values) > 0:
            nextval = new_values.pop()
            current = merge(current, nextval, original)
        print("\nFmerge result:", current)
        return current

    def run_validators_stream_fix(
        self,
        iteration: Iteration,
        validator_map: ValidatorMap,
        value_stream: Iterable[Tuple[Any, bool]],
        metadata: Dict[str, Any],
        absolute_property_path: str,
        reference_property_path: str,
        **kwargs,
    ) -> Iterable[StreamValidationResult]:
        validators = validator_map.get(reference_property_path, [])
        acc_output = ""
        validator_partial_acc: dict[int, str] = {}
        for validator in validators:
            validator_partial_acc[id(validator)] = ""
        last_chunk = None
        last_chunk_validated = False
        last_chunk_missing_validators = []
        refrain_triggered = False
        for chunk, finished in value_stream:
            original_text = chunk
            acc_output += chunk
            fixed_values = []
            last_chunk = chunk
            last_chunk_missing_validators = []
            if refrain_triggered:
                break
            for validator in validators:
                # reset chunk to original text
                chunk = original_text
                validator_logs = self.run_validator(
                    iteration,
                    validator,
                    chunk,
                    metadata,
                    absolute_property_path,
                    True,
                    remainder=finished,
                    **kwargs,
                )
                result = validator_logs.validation_result
                if result is None:
                    last_chunk_missing_validators.append(validator)
                result = cast(ValidationResult, result)
                # if we have a concrete result, log it in the validation map
                if isinstance(result, FailResult):
                    is_filter = validator.on_fail_descriptor is OnFailAction.FILTER
                    is_refrain = validator.on_fail_descriptor is OnFailAction.REFRAIN
                    if is_filter or is_refrain:
                        refrain_triggered = True
                        break
                    rechecked_value = None
                    chunk = self.perform_correction(
                        [result],
                        chunk,
                        validator,
                        validator.on_fail_descriptor,
                        rechecked_value=rechecked_value,
                    )
                    fixed_values.append(chunk)
                    validator_partial_acc[id(validator)] += chunk  # type: ignore
                elif isinstance(result, PassResult):
                    if (
                        validator.override_value_on_pass
                        and result.value_override is not result.ValueOverrideSentinel
                    ):
                        chunk = result.value_override
                    else:
                        chunk = result.validated_chunk
                    fixed_values.append(chunk)
                    validator_partial_acc[id(validator)] += chunk  # type: ignore
                validator_logs.value_after_validation = chunk
                if result and result.metadata is not None:
                    metadata = result.metadata

            if refrain_triggered:
                # if we have a failresult from a refrain/filter validator, yield empty
                yield StreamValidationResult(
                    chunk="", original_text=acc_output, metadata=metadata
                )
            else:
                # if every validator has yielded a concrete value, merge and yield
                # only merge and yield if all validators have run
                # TODO: check if only 1 validator - then skip merging
                if len(fixed_values) == len(validators):
                    last_chunk_validated = True
                    values_to_merge = []
                    for validator in validators:
                        values_to_merge.append(validator_partial_acc[id(validator)])
                    merged_value = self.multi_merge(acc_output, values_to_merge)
                    # merged_value = self.multi_merge(acc_output, values_to_merge)
                    # reset validator_partial_acc
                    for validator in validators:
                        validator_partial_acc[id(validator)] = ""
                    yield StreamValidationResult(
                        chunk=merged_value, original_text=acc_output, metadata=metadata
                    )
                    acc_output = ""
                else:
                    last_chunk_validated = False
        # handle case where LLM doesn't yield finished flag
        # we need to validate remainder of accumulated chunks
        if not last_chunk_validated and not refrain_triggered:
            original_text = last_chunk
            for validator in last_chunk_missing_validators:
                last_log = self.run_validator(
                    iteration,
                    validator,
                    # use empty chunk
                    # validator has already accumulated the chunk from the first loop
                    "",
                    metadata,
                    absolute_property_path,
                    True,
                    remainder=True,
                    **kwargs,
                )
                result = last_log.validation_result
                if isinstance(result, FailResult):
                    rechecked_value = None
                    last_chunk = self.perform_correction(
                        [result],
                        last_chunk,
                        validator,
                        validator.on_fail_descriptor,
                        rechecked_value=rechecked_value,
                    )
                    validator_partial_acc[id(validator)] += last_chunk  # type: ignore
                elif isinstance(result, PassResult):
                    if (
                        validator.override_value_on_pass
                        and result.value_override is not result.ValueOverrideSentinel
                    ):
                        last_chunk = result.value_override
                    else:
                        last_chunk = result.validated_chunk
                    validator_partial_acc[id(validator)] += last_chunk  # type: ignore
                last_log.value_after_validation = last_chunk
                if result and result.metadata is not None:
                    metadata = result.metadata
            values_to_merge = []
            for validator in validators:
                values_to_merge.append(validator_partial_acc[id(validator)])
            merged_value = self.multi_merge(acc_output, values_to_merge)
            yield StreamValidationResult(
                chunk=merged_value,
                original_text=original_text,  # type: ignore
                metadata=metadata,  # type: ignore
            )
            # yield merged value

    def run_validators_stream_noop(
        self,
        iteration: Iteration,
        validator_map: ValidatorMap,
        value_stream: Iterable[Tuple[Any, bool]],
        metadata: Dict[str, Any],
        absolute_property_path: str,
        reference_property_path: str,
        **kwargs,
    ) -> Iterable[StreamValidationResult]:
        validators = validator_map.get(reference_property_path, [])
        # Validate the field
        # TODO: Under what conditions do we yield?
        # When we have at least one non-None value?
        # When we have all non-None values?
        # Does this depend on whether we are fix or not?
        for chunk, finished in value_stream:
            original_text = chunk
            for validator in validators:
                validator_logs = self.run_validator(
                    iteration,
                    validator,
                    chunk,
                    metadata,
                    absolute_property_path,
                    True,
                    **kwargs,
                )
                result = validator_logs.validation_result
                result = cast(ValidationResult, result)

                if isinstance(result, FailResult):
                    rechecked_value = None
                    chunk = self.perform_correction(
                        [result],
                        chunk,
                        validator,
                        validator.on_fail_descriptor,
                        rechecked_value=rechecked_value,
                    )
                elif isinstance(result, PassResult):
                    if (
                        validator.override_value_on_pass
                        and result.value_override is not result.ValueOverrideSentinel
                    ):
                        chunk = result.value_override

                validator_logs.value_after_validation = chunk
                if result and result.metadata is not None:
                    metadata = result.metadata
                # # TODO: Filter is no longer terminal, so we shouldn't yield, right?
                # if isinstance(chunk, (Refrain, Filter, ReAsk)):
                #     yield chunk, metadata
            yield StreamValidationResult(
                chunk=chunk, original_text=original_text, metadata=metadata
            )

    def run_validators(
        self,
        iteration: Iteration,
        validator_map: ValidatorMap,
        value: Any,
        metadata: Dict[str, Any],
        absolute_property_path: str,
        reference_property_path: str,
        stream: Optional[bool] = False,
        **kwargs,
    ) -> Tuple[Any, Dict[str, Any]]:
        # Validate the field
        validators = validator_map.get(reference_property_path, [])
        for validator in validators:
            if stream:
                if validator.on_fail_descriptor is OnFailAction.REASK:
                    raise ValueError(
                        """Reask is not supported for stream validation, 
                        only noop and exception are supported."""
                    )
                if validator.on_fail_descriptor is OnFailAction.FIX:
                    raise ValueError(
                        """Fix is not supported for stream validation, 
                        only noop and exception are supported."""
                    )
                if validator.on_fail_descriptor is OnFailAction.FIX_REASK:
                    raise ValueError(
                        """Fix reask is not supported for stream validation, 
                        only noop and exception are supported."""
                    )
                if validator.on_fail_descriptor is OnFailAction.FILTER:
                    raise ValueError(
                        """Filter is not supported for stream validation, 
                        only noop and exception are supported."""
                    )
                if validator.on_fail_descriptor is OnFailAction.REFRAIN:
                    raise ValueError(
                        """Refrain is not supported for stream validation, 
                        only noop and exception are supported."""
                    )
            validator_logs = self.run_validator(
                iteration,
                validator,
                value,
                metadata,
                absolute_property_path,
                stream,
                **kwargs,
            )
            result = validator_logs.validation_result

            result = cast(ValidationResult, result)
            if isinstance(result, FailResult):
                rechecked_value = None
                if validator.on_fail_descriptor == OnFailAction.FIX_REASK:
                    fixed_value = result.fix_value
                    rechecked_value = self.run_validator_sync(
                        validator,
                        fixed_value,
                        metadata,
                        validator_logs,
                        stream,
                        **kwargs,
                    )
                value = self.perform_correction(
                    [result],
                    value,
                    validator,
                    validator.on_fail_descriptor,
                    rechecked_value=rechecked_value,
                )
            elif isinstance(result, PassResult):
                if (
                    validator.override_value_on_pass
                    and result.value_override is not result.ValueOverrideSentinel
                ):
                    value = result.value_override
            elif not stream:
                raise RuntimeError(f"Unexpected result type {type(result)}")

            validator_logs.value_after_validation = value
            if result and result.metadata is not None:
                metadata = result.metadata

            if isinstance(value, (Refrain, Filter, ReAsk)):
                return value, metadata
        return value, metadata

    def validate(
        self,
        value: Any,
        metadata: dict,
        validator_map: ValidatorMap,
        iteration: Iteration,
        absolute_path: str,
        reference_path: str,
        stream: Optional[bool] = False,
        **kwargs,
    ) -> Tuple[Any, dict]:
        ###
        # NOTE: The way validation can be executed now is fundamentally wide open.
        #   Since validators are tracked against the JSONPaths for the
        #       properties they should be applied to, we have the following options:
        #       1. Keep performing a Deep-First-Search
        #           - This is useful for backwards compatibility.
        #           - Is there something we gain by validating inside out?
        #       2. Swith to a Breadth-First-Search
        #           - Possible, no obvious advantages
        #       3. Run un-ordered
        #           - This would allow for true parallelism
        #           - Also means we're not unnecessarily iterating down through
        #               the object if there aren't any validations applied there.
        ###

        child_ref_path = reference_path.replace(".*", "")
        # Validate children first
        if isinstance(value, List):
            for index, child in enumerate(value):
                abs_child_path = f"{absolute_path}.{index}"
                ref_child_path = f"{child_ref_path}.*"
                child_value, metadata = self.validate(
                    child,
                    metadata,
                    validator_map,
                    iteration,
                    abs_child_path,
                    ref_child_path,
                )
                value[index] = child_value
        elif isinstance(value, Dict):
            for key in value:
                child = value.get(key)
                abs_child_path = f"{absolute_path}.{key}"
                ref_child_path = f"{child_ref_path}.{key}"
                child_value, metadata = self.validate(
                    child,
                    metadata,
                    validator_map,
                    iteration,
                    abs_child_path,
                    ref_child_path,
                )
                value[key] = child_value

        # Then validate the parent value
        value, metadata = self.run_validators(
            iteration,
            validator_map,
            value,
            metadata,
            absolute_path,
            reference_path,
            stream=stream,
            **kwargs,
        )
        return value, metadata

    def validate_stream(
        self,
        value_stream: Iterable[Tuple[Any, bool]],
        metadata: dict,
        validator_map: ValidatorMap,
        iteration: Iteration,
        absolute_path: str,
        reference_path: str,
        **kwargs,
    ) -> Iterable[StreamValidationResult]:
        # I assume validate stream doesn't need validate_dependents
        # because right now we're only handling StringSchema

        # Validate the field
        gen = self.run_validators_stream(
            iteration,
            validator_map,
            value_stream,
            metadata,
            absolute_path,
            reference_path,
            **kwargs,
        )
        return gen


class MultiprocMixin:
    multiprocessing_executor: Optional[ProcessPoolExecutor] = None
    process_count = int(os.environ.get("GUARDRAILS_PROCESS_COUNT", 10))

    def __init__(self):
        if MultiprocMixin.multiprocessing_executor is None:
            MultiprocMixin.multiprocessing_executor = ProcessPoolExecutor(
                max_workers=MultiprocMixin.process_count
            )


class AsyncValidatorService(ValidatorServiceBase, MultiprocMixin):
    async def run_validator_async(
        self,
        validator: Validator,
        value: Any,
        metadata: Dict,
        stream: Optional[bool] = False,
        *,
        validation_session_id: str,
        **kwargs,
    ) -> ValidationResult:
        result: ValidatorResult = self.execute_validator(
            validator,
            value,
            metadata,
            stream,
            validation_session_id=validation_session_id,
            **kwargs,
        )
        if asyncio.iscoroutine(result):
            result = await result

        if result is None:
            result = PassResult()
        else:
            result = cast(ValidationResult, result)
        return result

    async def run_validator(
        self,
        iteration: Iteration,
        validator: Validator,
        value: Any,
        metadata: Dict,
        absolute_property_path: str,
        stream: Optional[bool] = False,
        **kwargs,
    ) -> ValidatorLogs:
        validator_logs = self.before_run_validator(
            iteration, validator, value, absolute_property_path
        )

        result = await self.run_validator_async(
            validator,
            value,
            metadata,
            stream,
            validation_session_id=iteration.id,
            **kwargs,
        )

        return self.after_run_validator(validator, validator_logs, result)

    def group_validators(self, validators: List[Validator]):
        groups = itertools.groupby(
            validators, key=lambda v: (v.on_fail_descriptor, v.override_value_on_pass)
        )
        # NOTE: This isn't ordering anything.
        #   If we want to yield fix-like valiators first,
        #       then we need to extract them outside of the loop.
        for (on_fail_descriptor, override_on_pass), group in groups:
            if override_on_pass or on_fail_descriptor in [
                OnFailAction.FIX,
                OnFailAction.FIX_REASK,
                "custom",
            ]:
                for validator in group:
                    yield on_fail_descriptor, [validator]
            else:
                yield on_fail_descriptor, list(group)

    async def run_validators(
        self,
        iteration: Iteration,
        validator_map: ValidatorMap,
        value: Any,
        metadata: Dict,
        absolute_property_path: str,
        reference_property_path: str,
        stream: Optional[bool] = False,
        **kwargs,
    ):
        loop = asyncio.get_running_loop()
        validators = validator_map.get(reference_property_path, [])
        for on_fail, validator_group in self.group_validators(validators):
            parallel_tasks = []
            validators_logs: List[ValidatorLogs] = []
            for validator in validator_group:
                if validator.run_in_separate_process:
                    # queue the validators to run in a separate process
                    parallel_tasks.append(
                        loop.run_in_executor(
                            self.multiprocessing_executor,
                            self.run_validator,
                            iteration,
                            validator,
                            value,
                            metadata,
                            absolute_property_path,
                            stream,
                        )
                    )
                else:
                    # run the validators in the current process
                    result = await self.run_validator(
                        iteration,
                        validator,
                        value,
                        metadata,
                        absolute_property_path,
                        stream=stream,
                        **kwargs,
                    )
                    validators_logs.append(result)

            # wait for the parallel tasks to finish
            if parallel_tasks:
                parallel_results = await asyncio.gather(*parallel_tasks)
                awaited_results = []
                for res in parallel_results:
                    if asyncio.iscoroutine(res):
                        res = await res
                    awaited_results.append(res)
                validators_logs.extend(awaited_results)

            # process the results, handle failures
            fails = [
                logs
                for logs in validators_logs
                if isinstance(logs.validation_result, FailResult)
            ]
            if fails:
                # NOTE: Ignoring type bc we know it's a FailResult
                fail_results: List[FailResult] = [
                    logs.validation_result  # type: ignore
                    for logs in fails
                ]
                rechecked_value = None
                validator: Validator = validator_group[0]
                if validator.on_fail_descriptor == OnFailAction.FIX_REASK:
                    fixed_value = fail_results[0].fix_value
                    rechecked_value = await self.run_validator_async(
                        validator,
                        fixed_value,
                        fail_results[0].metadata or {},
                        stream,
                        validation_session_id=iteration.id,
                        **kwargs,
                    )
                value = self.perform_correction(
                    fail_results,
                    value,
                    validator_group[0],
                    on_fail,
                    rechecked_value=rechecked_value,
                )

            # handle overrides
            if (
                len(validator_group) == 1
                and validator_group[0].override_value_on_pass
                and isinstance(validators_logs[0].validation_result, PassResult)
                and validators_logs[0].validation_result.value_override
                is not PassResult.ValueOverrideSentinel
            ):
                value = validators_logs[0].validation_result.value_override

            for logs in validators_logs:
                logs.value_after_validation = value

            # return early if we have a filter, refrain, or reask
            if isinstance(value, (Filter, Refrain, FieldReAsk)):
                return value, metadata

        return value, metadata

    async def validate_children(
        self,
        value: Any,
        metadata: Dict,
        validator_map: ValidatorMap,
        iteration: Iteration,
        abs_parent_path: str,
        ref_parent_path: str,
        stream: Optional[bool] = False,
        **kwargs,
    ):
        async def validate_child(
            child_value: Any, *, key: Optional[str] = None, index: Optional[int] = None
        ):
            child_key = key or index
            abs_child_path = f"{abs_parent_path}.{child_key}"
            ref_child_path = ref_parent_path
            if key is not None:
                ref_child_path = f"{ref_child_path}.{key}"
            elif index is not None:
                ref_child_path = f"{ref_child_path}.*"
            new_child_value, new_metadata = await self.async_validate(
                child_value,
                metadata,
                validator_map,
                iteration,
                abs_child_path,
                ref_child_path,
                stream=stream,
                **kwargs,
            )
            return child_key, new_child_value, new_metadata

        tasks = []
        if isinstance(value, List):
            for index, child in enumerate(value):
                tasks.append(validate_child(child, index=index))
        elif isinstance(value, Dict):
            for key in value:
                child = value.get(key)
                tasks.append(validate_child(child, key=key))

        results = await asyncio.gather(*tasks)

        for key, child_value, child_metadata in results:
            value[key] = child_value
            # TODO address conflicting metadata entries
            metadata = {**metadata, **child_metadata}

        return value, metadata

    async def async_validate(
        self,
        value: Any,
        metadata: dict,
        validator_map: ValidatorMap,
        iteration: Iteration,
        absolute_path: str,
        reference_path: str,
        stream: Optional[bool] = False,
        **kwargs,
    ) -> Tuple[Any, dict]:
        child_ref_path = reference_path.replace(".*", "")
        # Validate children first
        if isinstance(value, List) or isinstance(value, Dict):
            await self.validate_children(
                value,
                metadata,
                validator_map,
                iteration,
                absolute_path,
                child_ref_path,
                stream=stream,
                **kwargs,
            )

        # Then validate the parent value
        value, metadata = await self.run_validators(
            iteration,
            validator_map,
            value,
            metadata,
            absolute_path,
            reference_path,
            stream=stream,
            **kwargs,
        )

        return value, metadata

    def validate(
        self,
        value: Any,
        metadata: dict,
        validator_map: ValidatorMap,
        iteration: Iteration,
        absolute_path: str,
        reference_path: str,
        stream: Optional[bool] = False,
        **kwargs,
    ) -> Tuple[Any, dict]:
        # Run validate_async in an async loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            raise RuntimeError(
                "Async event loop found, please call `validate_async` instead."
            )
        value, metadata = loop.run_until_complete(
            self.async_validate(
                value,
                metadata,
                validator_map,
                iteration,
                absolute_path,
                reference_path,
                stream=stream,
                **kwargs,
            )
        )
        return value, metadata


def validate(
    value: Any,
    metadata: dict,
    validator_map: ValidatorMap,
    iteration: Iteration,
    disable_tracer: Optional[bool] = True,
    path: Optional[str] = None,
    **kwargs,
):
    if path is None:
        path = "$"

    process_count = int(os.environ.get("GUARDRAILS_PROCESS_COUNT", 10))
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = None

    if process_count == 1:
        validator_service = SequentialValidatorService(disable_tracer)
    elif loop is not None and not loop.is_running():
        validator_service = AsyncValidatorService(disable_tracer)
    else:
        validator_service = SequentialValidatorService(disable_tracer)

    return validator_service.validate(
        value, metadata, validator_map, iteration, path, path, **kwargs
    )


def validate_stream(
    value_stream: Iterable[Tuple[Any, bool]],
    metadata: dict,
    validator_map: ValidatorMap,
    iteration: Iteration,
    disable_tracer: Optional[bool] = True,
    path: Optional[str] = None,
    **kwargs,
) -> Iterable[StreamValidationResult]:
    if path is None:
        path = "$"
    sequential_validator_service = SequentialValidatorService(disable_tracer)
    gen = sequential_validator_service.validate_stream(
        value_stream, metadata, validator_map, iteration, path, path, **kwargs
    )
    return gen


async def async_validate(
    value: Any,
    metadata: dict,
    validator_map: ValidatorMap,
    iteration: Iteration,
    disable_tracer: Optional[bool] = True,
    path: Optional[str] = None,
    stream: Optional[bool] = False,
    **kwargs,
) -> Tuple[Any, dict]:
    if path is None:
        path = "$"
    validator_service = AsyncValidatorService(disable_tracer)
    return await validator_service.async_validate(
        value, metadata, validator_map, iteration, path, path, stream, **kwargs
    )


def post_process_validation(
    validation_response: Any,
    attempt_number: int,
    iteration: Iteration,
    output_type: OutputTypes,
) -> Any:
    validated_response = apply_refrain(validation_response, output_type)

    # Remove all keys that have `Filter` values.
    validated_response = apply_filters(validated_response)

    trace_validation_result(
        validation_logs=iteration.validator_logs, attempt_number=attempt_number
    )

    return validated_response
