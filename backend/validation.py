"""Validation shared by form endpoints."""

import re
from decimal import Decimal, InvalidOperation
from urllib.parse import parse_qs

from fastapi import HTTPException


async def form_data(request):
    body = await request.body()
    if len(body) > 16384:
        raise HTTPException(413, "Form is too large")
    try:
        encoded = body.decode("utf-8")
        if re.search(r"%(?![0-9A-Fa-f]{2})", encoded):
            raise ValueError("Malformed percent encoding")
        parsed = parse_qs(encoded, keep_blank_values=True, max_num_fields=30, errors="strict")
        if any(len(values) != 1 for values in parsed.values()):
            raise ValueError("Duplicate form fields")
    except (UnicodeDecodeError, ValueError):
        raise HTTPException(400, "Invalid form data")
    return {key: value[0] for key, value in parsed.items()}


def required(data, *keys):
    missing = [key for key in keys if data.get(key) is None or not str(data[key]).strip()]
    if missing:
        raise HTTPException(400, "Missing fields: " + ", ".join(missing))


def positive_number(value, field):
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise HTTPException(400, f"{field} must be a number")
    if number < 1:
        raise HTTPException(400, f"{field} must be greater than zero")
    return number


def payment_amount(value):
    try:
        amount = Decimal(str(value))
        if (
            not amount.is_finite()
            or amount <= 0
            or amount > Decimal("9999999999.99")
            or amount != amount.quantize(Decimal("0.01"))
        ):
            raise ValueError()
    except (InvalidOperation, ValueError):
        raise HTTPException(400, "Enter a positive payment with at most 2 decimal places")
    return format(amount, ".2f")


def text_field(value, field, maximum):
    text = str(value or "").strip()
    if not text or len(text.encode("utf-8")) > maximum:
        raise HTTPException(400, f"{field} must contain 1-{maximum} bytes")
    if any(ord(character) < 32 for character in text):
        raise HTTPException(400, f"{field} cannot contain control characters")
    return text


def academic_identifier(value, field):
    identifier = text_field(value, field, 40).upper()
    if not re.fullmatch(r"[A-Z0-9][A-Z0-9./_-]{0,39}", identifier):
        raise HTTPException(
            400, f"{field} must use letters, numbers, dots, slashes, underscores or hyphens"
        )
    return identifier


def academic_session(value):
    value = str(value).strip()
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}", value):
        next_year = int(value[:4]) + 1
        if next_year > 9999 or int(value[5:]) != next_year % 100:
            raise HTTPException(400, "Academic session must cover consecutive years")
        value = f"{value[:4]}-{next_year:04d}"
    if not re.fullmatch(r"[0-9]{4}-[0-9]{4}", value):
        raise HTTPException(400, "Enter an academic session such as 2023-24 or 2023-2024")
    if int(value[5:]) != int(value[:4]) + 1:
        raise HTTPException(400, "Academic session must cover consecutive years")
    return value


def member_details(data):
    required(
        data,
        "name",
        "department",
        "phone",
        "email",
        "roll_no",
        "registration_no",
        "academic_session",
    )
    details = {
        "academic_session": academic_session(data["academic_session"]),
        "name": text_field(data["name"], "name", 100),
        "department": text_field(data["department"], "department", 100),
        "email": text_field(data["email"], "email", 100).lower(),
        "phone": str(data["phone"]).strip(),
        "roll_no": academic_identifier(data["roll_no"], "ID/Roll number"),
        "registration_no": academic_identifier(data["registration_no"], "Registration number"),
    }
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", details["email"]):
        raise HTTPException(400, "Enter a valid email address")
    if not re.fullmatch(r"[0-9]{11}", details["phone"]):
        raise HTTPException(400, "Phone number must contain exactly 11 digits")
    return details
