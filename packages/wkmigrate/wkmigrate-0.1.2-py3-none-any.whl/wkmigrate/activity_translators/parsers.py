import re
import warnings
from datetime import datetime, timedelta
from typing import Optional
from wkmigrate.enums.condition_operation_pattern import ConditionOperationPattern


def parse_policy(policy: Optional[dict]) -> dict:
    """ Parses a data factory pipeline activity policy to a common object model.
        :parameter policy: Dictionary definition of the source pipeline activity policy
        :return: Dictionary definition of the policy settings
    """
    if policy is None:
        return {}
    # Warn about secure input/output logging:
    if 'secure_input' in policy:
        warnings.warn('Secure input logging not applicable to Databricks workflows.', stacklevel=2)
    if 'secure_output' in policy:
        warnings.warn('Secure output logging not applicable to Databricks workflows.', stacklevel=2)
    # Parse the policy attributes:
    parsed_policy = {}
    # Parse the timeout seconds:
    if 'timeout' in policy:
        parsed_policy['timeout_seconds'] = _parse_timeout_string(policy.get('timeout'))
    # Parse the number of retry attempts:
    if 'retry' in policy:
        parsed_policy['max_retries'] = int(policy.get('retry'))
    # Parse the retry wait time in milliseconds:
    if 'retry_interval_in_seconds' in policy:
        parsed_policy['min_retry_interval_millis'] = 1000 * int(policy.get('retry_interval_in_seconds', 0))
    return parsed_policy


def parse_dependencies(dependencies: Optional[list[dict]]) -> Optional[list[dict]]:
    """ Parses a data factory pipeline activity's dependencies to a common object model.
        :parameter dependencies: Dictionary definition of the source pipeline activity's dependencies
        :return: Dictionary definition of the task-level parameter definitions
    """
    if dependencies is None:
        return None
    # Parse the dependencies from the list:
    parsed_dependencies = []
    for dependency in dependencies:
        # Get the dependency condition:
        conditions = dependency.get('dependencyConditions')
        # Validate the dependency conditions:
        if conditions is not None and len(conditions) > 1:
            raise ValueError('Dependencies with multiple conditions are not supported.')
        # Append the dependency:
        parsed_dependencies.append({
            'task_key': dependency.get('activity', None),
            'outcome': dependency.get('outcome', None)
        })
    return parsed_dependencies


def parse_notebook_parameters(parameters: Optional[dict]) -> Optional[dict]:
    """ Parses task parameters in a Databricks notebook activity definition from Data Factory's object model to a
        set of key/value pairs in the Databricks SDK object model.
        :parameter parameters: Set of task parameters in Data Factory as a ``dict[str, Any]``
        :return: Set of task parameters as a ``dict[str, str]``
    """
    if parameters is None:
        return None
    # Parse the parameters:
    parsed_parameters = {}
    for name, value in parameters.items():
        if not isinstance(value, str):
            warnings.warn(f'Could not resolve default value for parameter {name}, setting to ""', stacklevel=2)
            value = ""
        parsed_parameters[name] = value
    return parsed_parameters


def parse_condition_expression(condition: dict) -> dict:
    """ Parses a condition expression in an If Condition activity definition from Data Factory's object model to the
        Databricks SDK object model.
        :parameter condition: Condition expression in Data Factory as a ``dict[str, Any]``
        :return: Condition expression as a ``dict[str, str]``
    """
    # Validate the condition:
    if 'value' not in condition:
        raise ValueError('Condition expression must include a valid conditional value')
    # Match a boolean operator:
    for op in ConditionOperationPattern:
        match = re.match(string=condition.get('value'), pattern=op.value)
        if match is not None:
            return {
                'op': op.name,
                'left': match.group(1),
                'right': match.group(2)
            }
    raise ValueError('Condition expression must include "equals", "greaterThan", "greaterThanOrEquals", "lessThan", or '
                     '"lessThanOrEquals" operation.')


def _parse_timeout_string(timeout_string: str) -> int:
    """ Parses a timeout string in the format ``d.hh:mm:ss`` into an integer number of seconds.
        :parameter timeout_string: Timeout string in the format ``d.hh:mm:ss``
        :return: Integer number of seconds
    """
    if timeout_string[:2] == '0.':
        # Parse the timeout string to HH:MM:SS format:
        timeout_string = timeout_string[2:]
        time_format = '%H:%M:%S'
        date_time = datetime.strptime(timeout_string, time_format)
        time_delta = timedelta(hours=date_time.hour, minutes=date_time.minute, seconds=date_time.second)
    else:
        # Parse the timeout string to DD.HH:MM:SS format:
        timeout_string = timeout_string.zfill(11)
        time_format = '%d.%H:%M:%S'
        date_time = datetime.strptime(timeout_string, time_format)
        time_delta = timedelta(days=date_time.day, hours=date_time.hour,
                               minutes=date_time.minute, seconds=date_time.second)
    return int(time_delta.total_seconds())
