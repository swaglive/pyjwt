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
    [],
    SITE_PACKAGE_PATH
], ids=['rapid-partial-jwt', 'rapid-wrapper-jwt', 'origjson-jwt'])
def jwt_package(request, mocker):
    sys.path = copy.copy(ORIG_SYS_PATH)
    sys.path = request.param + sys.path

    jwt_modules = [m for m in sys.modules if m.startswith('jwt')]
    for m in jwt_modules:
        sys.modules.pop(m, None)

    import jwt
    if request.param_index == 0:
        mocker.patch.object(jwt.json, 'dumps', jwt.json.partial_dumps)
        mocker.patch.object(jwt.json, 'loads', jwt.json.partial_loads)
    yield jwt


data = {
    'token-1': {
        'jti': 'XCIquGY7XldJ5cPe',
        'iss': 'localhost',
        'aud': 'localhost',
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        'sub': '5c222ab8663b5e5749e5c3de',
        'scopes': ['accessToken.create', 'curator', 'signed:personal', 'vip', 'beta'],
        'meta': [{
            "caption": "被幹到淫叫出汁的女警露臉",
            "id": "5c30db783a4ce665e4338a5c",
            "sender": "58a4443f94ab56f9125c5a40",
            "unlock_price": 240
        },
        {
            "caption": "⚠️露臉 顏射 口爆 高清⚠️\n完戰💯🤙🏻",
            "id": "5c308ee14c2ab9b7126e8ca4",
            "sender": "5c1f7ccdd07f3566ffdbcc9a",
            "unlock_price": 240
        },
        {
            "caption": "🔥[露臉實戰]🔥🎉假日福利🎉\n🈵💯顏射 射好射滿💯🈵",
            "id": "5c3120570923c104457aea28",
            "sender": "5c1f7ccdd07f3566ffdbcc9a",
            "unlock_price": 240
        },
        {
            "caption": "🈲表妹3P✨實戰初體驗🈲\n表妹正面被幹到高潮了🔞\n第一次看到悶騷的表妹如此淫蕩🔥🔥🔥",
            "id": "5c30d31fd7d0240022f511be",
            "sender": "5bc434dbd8f9b139c89172ce",
            "unlock_price": 240
        },
        {
            "caption": "在摩天輪👆\n😳太刺激了啦😳",
            "id": "5c30b18a4c2ab96d266e8d8e",
            "sender": "5c1f7ccdd07f3566ffdbcc9a",
            "unlock_price": 240
        },
        {
            "caption": "5大主播多人粉絲混戰🔥有看過5個女主播跪一排一超幫男生舔肉棒嗎？超難得一見的畫面❤錯過就沒囉😘",
            "id": "5c309b704c2ab917a06e8c90",
            "sender": "5a9d299cb197e9695b3390c0",
            "unlock_price": 240
        },
        {
            "caption": "G奶女警被吸乳吸到好濕",
            "id": "5c30d9f2ad7d9952fe34bce5",
            "sender": "58a4443f94ab56f9125c5a40",
            "unlock_price": 240
        },
        {
            "caption": "在機場廁所脫到全裸露點❤️",
            "id": "5c3200b8ad7d995a7834bd9a",
            "sender": "58a4443f94ab56f9125c5a40",
            "unlock_price": 240
        },
        {
            "caption": "在摩天輪👆\n哥哥好硬還不射但太多人在排隊要搭乘只好做最後衝刺🏃‍♀️",
            "id": "5c30b1383a4ce6aeaf5d5b88",
            "sender": "5c1f7ccdd07f3566ffdbcc9a",
            "unlock_price": 240
        },
        {
            "caption": "🈲表妹3P✨實戰初體驗🈲\n傳教式被幹\n跟表妹一起三點全露",
            "id": "5c30d0cd0923c100157ae9d2",
            "sender": "5bc434dbd8f9b139c89172ce",
            "unlock_price": 240
        }]
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
    json_mod = getattr(jwt_package, 'json', None)
    json_func = getattr(json_mod, 'dumps', None) if json_mod else None
    print('\nCurrent JWT Lib: %s, dumps: %s' % (jwt_package, json_func))
    benchmark(
        jwt_package.encode,
        payload,
        key=secret_key,
        algorithm='HS256',
        headers=headers
    )


@pytest.mark.parametrize('payload', list(data.values()), ids=list(data.keys()))
def test_decode_performance(benchmark, jwt_package, payload):
    json_mod = getattr(jwt_package, 'json', None)
    json_func = getattr(json_mod, 'loads', None) if json_mod else None
    print('\nCurrent JWT Lib: %s, loads: %s' % (jwt_package, json_func))
    token = jwt_package.encode(payload, key=secret_key, headers=headers).decode('utf-8')
    benchmark(
        jwt_package.decode,
        token,
        key=secret_key,
        audience='localhost',
        algorithms=['HS256'],
    )
