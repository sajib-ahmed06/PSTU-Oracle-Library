"""Reminder rules and message content, independent of providers and scheduling."""

from datetime import date, datetime, timedelta, timezone

DAILY_FINE = 10
DHAKA = timezone(timedelta(hours=6), "Asia/Dhaka")


def reminder_for(loan, today=None):
    today = today or datetime.now(DHAKA).date()
    due = date.fromisoformat(loan["due_date"])
    overdue = (today - due).days
    active = loan["status"] == "ISSUED"
    member = f"PSTU-{int(loan['student_id']):04d}"
    book = f"{loan['title']} (Copy #{loan['copy_no']})" if loan.get("copy_no") else loan["title"]
    prefix = f"PSTU Library: {loan['name']} ({member}), book: {book}. "
    if active and -3 <= overdue <= 0:
        return {
            "key": f"due:{loan['issue_id']}:{due.isoformat()}",
            "issue_id": loan["issue_id"],
            "channel": "SMS",
            "recipient": loan["phone"],
            "subject": "Library return reminder",
            "body": prefix + f"Return by {due.isoformat()} ({-overdue} day(s) left). "
            f"Late fine: Tk {DAILY_FINE}/day from {(due + timedelta(days=1)).isoformat()}. "
            "Please return the book to the library by the due date to avoid a fine.",
        }
    amount = float(loan.get("balance") or 0) if not active else overdue * DAILY_FINE
    if overdue >= 1 and amount > 0:
        # First overdue day, then every ten days: 1, 11, 21, ...
        milestone = 1 + ((overdue - 1) // 10) * 10
        note = (
            f"The book is {overdue} day(s) overdue. Current estimated fine: Tk {amount:g}. "
            f"The fine increases by Tk {DAILY_FINE} each overdue day until return. "
            "Please return the book as soon as possible and pay the final fine in full at the library."
            if active
            else f"Your book has been returned. Outstanding recorded fine: Tk {amount:g}. "
            "The fine no longer increases after return. Please pay the outstanding fine in full at the library."
        )
        return {
            "key": f"fine:{loan['issue_id']}:{due.isoformat()}:{milestone}",
            "issue_id": loan["issue_id"],
            "channel": "EMAIL",
            "recipient": loan["email"],
            "subject": f"Library fine reminder: {book} — Tk {amount:g}",
            "body": prefix
            + f"Return was due on {due.isoformat()}. "
            + note
            + f"\nAs of {today.isoformat()} (Asia/Dhaka).",
        }
    return None
