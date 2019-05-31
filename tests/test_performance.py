# -*- coding: utf-8 -*-
import sys
import site
import pytest
import datetime
import copy


ORIG_SYS_PATH = copy.copy(sys.path)
SITE_PACKAGE_PATH = site.getsitepackages()


@pytest.fixture(params=[
    [],
    SITE_PACKAGE_PATH
], ids=['rapid-wrapper-jwt', 'origjson-jwt'])
def jwt_package(request):
    sys.path = copy.copy(ORIG_SYS_PATH)
    sys.path = request.param + sys.path

    jwt_modules = [m for m in sys.modules if m.startswith('jwt')]
    for m in jwt_modules:
        sys.modules.pop(m, None)

    import jwt
    yield jwt


data = {
    'token': {
        'jti': 'XCIquGY7XldJ5cPe',
        'iss': 'localhost',
        'aud': 'localhost',
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        'sub': '5c222ab8663b5e5749e5c3de',
        'scopes': ['accessToken.create', 'curator', 'signed:personal', 'vip', 'beta'],
    }
}


headers = {
  "typ": "JWT",
  "alg": "HS256",
  "kid": "5915a9f3"
}

secret_key = 'secret'


@pytest.mark.parametrize('payload', list(data.values()), ids=list(data.keys()))
def test_encode_performance(benchmark, jwt_package, payload):
    benchmark(
        jwt_package.encode,
        payload,
        key=secret_key,
        algorithm='HS256',
        headers=headers
    )


@pytest.mark.parametrize('payload', list(data.values()), ids=list(data.keys()))
def test_decode_performance(benchmark, jwt_package, payload):
    token = jwt_package.encode(payload, key=secret_key, headers=headers).decode('utf-8')
    benchmark(
        jwt_package.decode,
        token,
        key=secret_key,
        audience='localhost',
        algorithms=['HS256'],
    )
