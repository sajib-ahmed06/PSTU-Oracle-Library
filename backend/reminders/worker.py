"""Scheduled delivery while the app runs; a CLI supports an external scheduler."""

import argparse
import asyncio
import logging
import threading
from contextlib import asynccontextmanager
from datetime import datetime

from backend.database import config
from . import providers, store
from .messages import DHAKA, reminder_for

logger = logging.getLogger(__name__)


def prepare_message(loan, today=None, settings=None):
    settings = settings or config
    message = reminder_for(loan, today)
    if message and message["channel"] == "SMS":
        channel = settings.get("DUE_REMINDER_CHANNEL", "email").upper()
        if channel not in {"SMS", "EMAIL"}:
            raise ValueError("DUE_REMINDER_CHANNEL must be sms or email")
        message["channel"] = channel
        if channel == "EMAIL":
            message["recipient"] = loan["email"]
    return message


def run_once(settings=None, stop=None):
    settings = settings or config
    if settings.get("REMINDERS_ENABLED", "false").lower() != "true":
        return
    if not any(providers.ready(channel, settings) for channel in ("SMS", "EMAIL")):
        return
    now = datetime.now(DHAKA)
    if now.hour < int(settings.get("REMINDER_SEND_HOUR", "9")):
        return
    store.recover_abandoned()
    for loan in store.loans():
        if stop and stop.is_set():
            break
        message = prepare_message(loan, now.date(), settings)
        if not message or not providers.ready(message["channel"], settings):
            continue
        # Refresh just before claiming: a returned book/paid fine must not get an obsolete reminder.
        current = store.loans(loan["issue_id"])
        latest = prepare_message(current[0], now.date(), settings) if current else None
        if not latest or latest["key"] != message["key"]:
            continue
        if not store.claim(latest):
            continue
        try:
            send = providers.send_sms if latest["channel"] == "SMS" else providers.send_email
            provider_id = send(latest, settings)
        except providers.DeliveryRejected:
            store.finish(latest["key"], "FAILED")
        except Exception:
            store.finish(latest["key"], "UNKNOWN")
            logger.warning("Reminder outcome requires review: %s", latest["key"])
        else:
            store.finish(latest["key"], "ACCEPTED", provider_id)


def loop(stop):
    interval = max(60, int(config.get("REMINDER_CHECK_SECONDS", "300")))
    while not stop.is_set():
        try:
            run_once(stop=stop)
        except Exception as error:
            # Do not log provider responses, contact details or credentials.
            logger.warning("Reminder check failed (%s)", type(error).__name__)
        stop.wait(interval)


@asynccontextmanager
async def lifespan(app):
    stop = threading.Event()
    thread = None
    if config.get("REMINDERS_ENABLED", "false").lower() == "true":
        thread = threading.Thread(target=loop, args=(stop,), name="library-reminders", daemon=True)
        thread.start()
    try:
        yield
    finally:
        stop.set()
        if thread:
            await asyncio.to_thread(thread.join, 30)


def main():
    parser = argparse.ArgumentParser(description="Library SMS/email reminders")
    parser.add_argument("--check", action="store_true", help="Check configuration without sending")
    parser.add_argument(
        "--preview", action="store_true", help="Preview due messages without sending"
    )
    parser.add_argument("--once", action="store_true", help="Send enabled scheduled reminders once")
    args = parser.parse_args()
    if args.check:
        print("Scheduler enabled:", config.get("REMINDERS_ENABLED", "false"))
        for channel in ("SMS", "EMAIL"):
            print(channel, "ready:", providers.ready(channel, config))
    elif args.preview:
        for loan in store.loans():
            message = prepare_message(loan)
            if message:
                print(message["key"], message["channel"], message["body"])
    elif args.once:
        run_once()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
