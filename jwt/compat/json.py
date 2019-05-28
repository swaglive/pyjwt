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


def loads(*args, **kwargs):
    kwargs.pop('encoding', None)
    if kwargs.get('cls', None):
        cls_kwargs = copy.copy(kwargs)
        cls_kwargs.pop('cls', None)
        kwargs['object_hook'] = kwargs['cls'](**cls_kwargs).object_hook
    
    kwargs.pop('parse_float', None)
    kwargs.pop('parse_int', None)
    kwargs.pop('parse_constant', None)
    kwargs.pop('object_pairs_hook', None)
    kwargs.update({
        'allow_nan': False,
        'number_mode': NM_NATIVE,
        'datetime_mode': DM_ISO8601 | DM_SHIFT_TO_UTC,
    })

    return _loads(*args, **kwargs)

