# -*- coding: utf-8 -*-

import functools
from rapidjson import (
    DM_IGNORE_TZ, DM_ISO8601, DM_NAIVE_IS_UTC, DM_NONE, DM_ONLY_SECONDS, DM_SHIFT_TO_UTC, DM_UNIX_TIME,
    NM_DECIMAL, NM_NAN, NM_NATIVE, NM_NONE,
    PM_COMMENTS, PM_NONE, PM_TRAILING_COMMAS,
    UM_CANONICAL, UM_HEX, UM_NONE,
    ValidationError, Validator,
    __author__, __doc__, __file__, __loader__, __name__, __package__, __rapidjson_version__, __spec__, __version__,
    dump, load, RawJSON, Decoder, Encoder,
    dumps, loads,
)

from json import (
    JSONDecoder, JSONEncoder
)


dumps = functools.partial(
    dumps,
    indent=None,
    ensure_ascii=False,
    number_mode=NM_NATIVE,
    datetime_mode=DM_UNIX_TIME | DM_NAIVE_IS_UTC | DM_ONLY_SECONDS,
)


loads = functools.partial(
    loads,
    number_mode=NM_NATIVE, allow_nan=False,
    datetime_mode=DM_ISO8601 | DM_SHIFT_TO_UTC,
)
