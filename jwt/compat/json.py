# -*- coding: utf-8 -*-

import copy
import rapidjson


def dumps(*args, **kwargs):
    kwargs.update({
        'indent': None,
        'ensure_ascii': False
    })
    if kwargs.get('cls', None):
        cls_kwargs = copy.copy(kwargs)
        cls_kwargs.pop('cls', None)
        kwargs['default'] = kwargs['cls'](**cls_kwargs).default

    kwargs.pop('check_circular', None)
    kwargs.pop('cls', None)
    kwargs.pop('separators', None)
    kwargs.update({
        'number_mode': rapidjson.NM_NATIVE,
        'datetime_mode': rapidjson.DM_UNIX_TIME | rapidjson.DM_NAIVE_IS_UTC | rapidjson.DM_ONLY_SECONDS
    })

    return rapidjson.dumps(*args, **kwargs)


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
        'number_mode': rapidjson.NM_NATIVE,
        'datetime_mode': rapidjson.DM_ISO8601 | rapidjson.DM_SHIFT_TO_UTC,
    })

    return rapidjson.loads(*args, **kwargs)

