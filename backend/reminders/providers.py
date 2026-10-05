"""Twilio SMS and authenticated SMTP email adapters."""

import base64
import json
import re
import smtplib
import ssl
from email.message import EmailMessage
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class DeliveryRejected(Exception):
    """Provider explicitly rejected the message; a later retry is safe."""


def ready(channel, config):
    names = (
        ("TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_FROM_NUMBER")
        if channel == "SMS"
        else ("SMTP_HOST", "SMTP_FROM", "SMTP_USERNAME", "SMTP_PASSWORD")
    )
    return config.get(f"{channel}_REMINDERS_ENABLED", "false").lower() == "true" and all(
        config.get(name) for name in names
    )


def send_sms(message, config):
    phone = message["recipient"]
    if re.fullmatch(r"01[0-9]{9}", phone or ""):
        phone = "+88" + phone
    if not re.fullmatch(r"\+[0-9]{8,15}", phone or ""):
        raise DeliveryRejected("Invalid recipient phone")
    sid = config["TWILIO_ACCOUNT_SID"]
    if not re.fullmatch(r"AC[a-fA-F0-9]{32}", sid):
        raise DeliveryRejected("Invalid account configuration")
    authorization = base64.b64encode(f"{sid}:{config['TWILIO_AUTH_TOKEN']}".encode()).decode()
    request = Request(
        f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
        data=urlencode(
            {"To": phone, "From": config["TWILIO_FROM_NUMBER"], "Body": message["body"]}
        ).encode(),
        headers={
            "Authorization": f"Basic {authorization}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)["sid"]
    except HTTPError as error:
        if 400 <= error.code < 500:
            raise DeliveryRejected("SMS provider rejected the message") from None
        raise


def send_email(message, config):
    email = EmailMessage()
    email["From"] = config["SMTP_FROM"]
    email["To"] = message["recipient"]
    email["Subject"] = message["subject"]
    email.set_content(message["body"])
    context = ssl.create_default_context()
    implicit_tls = config.get("SMTP_SECURITY", "starttls").lower() == "ssl"
    client = smtplib.SMTP_SSL if implicit_tls else smtplib.SMTP
    port = int(config.get("SMTP_PORT", "465" if implicit_tls else "587"))
    options = {"context": context} if implicit_tls else {}
    try:
        with client(config["SMTP_HOST"], port, timeout=20, **options) as connection:
            if not implicit_tls:
                connection.starttls(context=context)
            connection.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
            refused = connection.send_message(email)
            if refused:
                raise DeliveryRejected("Email recipient rejected")
    except (
        smtplib.SMTPRecipientsRefused,
        smtplib.SMTPAuthenticationError,
        smtplib.SMTPSenderRefused,
        smtplib.SMTPDataError,
    ) as error:
        raise DeliveryRejected("Email provider rejected the message") from error
    return "smtp-accepted"
