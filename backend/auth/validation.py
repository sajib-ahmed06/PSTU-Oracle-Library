"""Member ID, staff username, and password validation."""

import re
from fastapi import HTTPException

USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_]{2,29}")


def member_number(value):
    match = re.fullmatch(r"(?:PSTU-)?([0-9]{1,20})", value.strip(), re.I)
    if not match or int(match[1]) < 1:
        raise HTTPException(400, "Enter a valid Member ID, for example PSTU-0001")
    return int(match[1])


def validate_password(password):
    if not 4 <= len(password) <= 128:
        raise HTTPException(400, "Password must contain 4-128 characters")


def validate_credentials(username, password):
    if not USERNAME_PATTERN.fullmatch(username):
        raise HTTPException(400, "Username must be 3-30 letters, numbers or underscores")
    validate_password(password)
