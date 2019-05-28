# -*- coding: utf-8 -*-
import os
import sys
import site
import importlib
import pytest
import datetime
import functools
import copy

from .compat import json


ORIG_SYS_PATH = copy.deepcopy(sys.path)
SITE_PACKAGE_PATH = site.getsitepackages()

@pytest.fixture(params=[
    [],
    SITE_PACKAGE_PATH
], ids=['rapidjson-jwt', 'origjson-jwt'])
def jwt_package(request):
    sys.path = copy.deepcopy(ORIG_SYS_PATH)
    sys.path = request.param + sys.path
    for m in [m for m in sys.modules if m.startswith('jwt')]:
        sys.modules.pop(m, None)

    import jwt
    yield jwt


data = {
    'token-1': {
        'jti': 'XCIquGY7XldJ5cPe',
        'iss': 'localhost',
        'aud': 'localhost',
        'exp': datetime.datetime.utcnow(),
        'sub': datetime.datetime.utcnow(),
        'scopes': ['accessToken.create', 'curator', 'signed:personal', 'vip', 'beta']
    }
}

# NOTE, We don't need this when use rapidjson, should I put it in to jwt_package?
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        # if isinstance(obj, bson.ObjectId):
        #     return str(obj)
        # if isinstance(obj, decimal.Decimal):
        #     return str(obj)
        # if isinstance(obj, DottedCollection):
        #     return obj.to_python()
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.timestamp()
            # return utils.to_datetime_string(obj)
        # if isinstance(obj, semantic_version.Version):
        #     return str(obj)
        # if isinstance(obj, typing.re.Pattern):
        #     return obj.pattern
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable")


headers = {
  "typ": "JWT",
  "alg": "HS256",
  "kid": "5915a9f3"
}

secret_key = 'secret'

# @pytest.mark.skip()
@pytest.mark.parametrize('payload', list(data.values()), ids=list(data.keys()))
def test_encode_performance(benchmark, jwt_package, payload):
    benchmark(
        jwt_package.encode,
        payload,
        key=secret_key,
        algorithm='HS256',
        headers=headers,
        # json_encoder=CustomJSONEncoder
    )


@pytest.mark.parametrize('payload', list(data.values()), ids=list(data.keys()))
def test_decode_performance(benchmark, jwt_package, payload):
    token = jwt_package.encode(payload, key=secret_key, headers=headers, json_encoder=CustomJSONEncoder).decode('utf-8')
    benchmark(
        jwt_package.decode,
        token,
        key=secret_key,
        audience='localhost',
        algorithms=['HS256'],
        options={'verify_exp': False}
    )
