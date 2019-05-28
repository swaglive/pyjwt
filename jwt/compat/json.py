# -*- coding: utf-8 -*-

import copy
from rapidjson import (
    DM_ISO8601, DM_NAIVE_IS_UTC, DM_ONLY_SECONDS, DM_UNIX_TIME, NM_NATIVE, DM_SHIFT_TO_UTC,
    dumps as _dumps, loads as _loads
)

def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True,
        cls=None, indent=None, separators=None, default=None, sort_keys=False):
    indent = None
    ensure_ascii = False

    return _dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, indent=indent,
        default=None if not cls else cls(
            skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan,
            indent=indent, separators=separators, default=default, sort_keys=sort_keys).default
        ,
        sort_keys=sort_keys, number_mode=NM_NATIVE,
        datetime_mode=DM_UNIX_TIME | DM_NAIVE_IS_UTC | DM_ONLY_SECONDS,
        uuid_mode=None, allow_nan=allow_nan)


def loads(string, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None,
        parse_constant=None, object_pairs_hook=None, strict=True):
    # In order to prevent kwargs but still allow give the value of 'strict'
    # Add a additional arg 'strict' with default value.

    return _loads(string,
        object_hook=object_hook if not cls else cls(
            object_hook=object_hook, parse_float=parse_float, parse_int=parse_int,
            parse_constant=parse_constant, strict=strict, object_pairs_hook=object_pairs_hook).object_hook,
        number_mode=NM_NATIVE, datetime_mode=DM_ISO8601 | DM_SHIFT_TO_UTC,
        uuid_mode=None, parse_mode=None, allow_nan=False)

