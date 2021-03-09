from collections import OrderedDict

from fdk_fulltext_search.search.fields import (
    index_description_fields,
    index_fulltext_fields,
    index_suggestion_fields,
    index_title_fields,
)


def _fields(indices: list, index_fields: dict):
    field_list = []
    for index in indices:
        field_list = field_list + index_fields[index]
    field_list = list(OrderedDict.fromkeys(field_list))
    field_list.sort()
    return field_list


def title_fields(indices: list):
    return _fields(indices, index_title_fields)


def description_fields(indices: list):
    return _fields(indices, index_description_fields)


def fulltext_fields(indices: list):
    return _fields(indices, index_fulltext_fields)


def suggestion_fields(indices: list):
    return _fields(indices, index_suggestion_fields)
