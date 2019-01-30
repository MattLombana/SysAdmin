#!/usr/bin/env python
import pprint
import hashlib
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer

pp = pprint.PrettyPrinter(indent=1)
secret_key = raw_input("Enter the secret key:\n")
cookie_str = raw_input("Enter the cookie:\n")


def decode_flask_cookie(secret_key, cookie_str):
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, serializer=serializer, salt=salt, signer_kwargs=signer_kwargs)
    return s.loads(cookie_str)

pp.pprint(decode_flask_cookie(secret_key, cookie_str))
