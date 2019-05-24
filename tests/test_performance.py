# -*- coding: utf-8 -*-
import os
import sys
import importlib
import pytest
import datetime
import functools
import json


# !NOTE! Below method of 'Import two packages with the same name' is incorrect
# After below 4 lines, although jwt_rapidjson.__file__ and jwt_orig.__file__ is different.
# But, the internal behavior will be both implement by rapidjson
# TODO, we need find a good way to modify the name in sys.modules
jwt_rapidjson = importlib.import_module('jwt')
sys.path = list(filter(lambda p: p != os.getcwd(), sys.path))
orig_module = sys.modules.pop('jwt')
jwt_orig = importlib.import_module('jwt')


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
@pytest.mark.parametrize('jwt', [
    jwt_rapidjson,
    jwt_orig
], ids=['jwt_rapidjson.encode', 'jwt_orig.encode'])
@pytest.mark.parametrize('payload', list(data.values()), ids=list(data.keys()))
def test_jwt_encode_performance(benchmark, jwt, payload):
    benchmark(
        jwt.encode,
        payload,
        key=secret_key,
        algorithm='HS256',
        headers=headers,
        json_encoder=CustomJSONEncoder
    )


@pytest.mark.parametrize('jwt', [
    jwt_rapidjson,
    jwt_orig
], ids=['jwt_rapidjson.decode', 'jwt_orig.decode'])
@pytest.mark.parametrize('payload', list(data.values()), ids=list(data.keys()))
def test_decode(benchmark, jwt, payload):
    token = jwt_orig.encode(payload, key=secret_key, headers=headers, json_encoder=CustomJSONEncoder).decode('utf-8')
    benchmark(
        jwt.decode,
        token,
        key=secret_key,
        audience='localhost',
        algorithms=['HS256'],
        options={'verify_exp': False}
    )
