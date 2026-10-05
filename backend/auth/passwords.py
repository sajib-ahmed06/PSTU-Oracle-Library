"""Salted password storage with compatibility for existing demo accounts."""

import base64
import hashlib
import hmac
import secrets

ITERATIONS = 260000


def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    encode = lambda value: base64.b64encode(value).decode("ascii")
    return f"pbkdf2${ITERATIONS}${encode(salt)}${encode(digest)}"


def verify_password(password, stored):
    if not stored.startswith("pbkdf2$"):
        return hmac.compare_digest(password.encode("utf-8"), stored.encode("utf-8"))
    try:
        _, iterations, salt, expected = stored.split("$")
        rounds = int(iterations)
        if not 100000 <= rounds <= 1000000:
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), base64.b64decode(salt, validate=True), rounds
        )
        return hmac.compare_digest(actual, base64.b64decode(expected, validate=True))
    except (ValueError, TypeError):
        return False
