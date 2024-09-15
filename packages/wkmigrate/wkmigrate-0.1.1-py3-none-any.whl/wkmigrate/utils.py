""" This module defines shared utilities for translating data pipelines."""
from typing import Any, Optional


def identity(item: Any) -> Any:
    return item


def translate(items: dict, mapping: dict) -> dict:
    output = {}
    for key, value in mapping.items():
        source_key = mapping[key]['key']
        parser = mapping[key]['parser']
        output[key] = parser(items.get(source_key))
    return output


def append_system_tags(tags: Optional[dict]) -> dict:
    """ Appends system tags for attributing clusters to the Tributary library.
        :parameter tags: Optional set of user-defined tags as a ``dict``
        :return: Set of tags with 'CREATED_BY_WKMIGRATE' appended.
    """
    if tags is None:
        return {'CREATED_BY_WKMIGRATE': ''}
    else:
        tags['CREATED_BY_WKMIGRATE'] = ''
        return tags
