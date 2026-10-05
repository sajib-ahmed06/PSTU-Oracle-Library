# Member SMS/email reminders

Dashboard reminders are active without a messaging provider. The member dashboard shows return
reminders from three days before the due date through the due day. Once overdue, it shows today's
Oracle-calculated fine, Tk 10 per overdue day, the return deadline and the action to return the book.
It refreshes each minute while open. Fine growth stops after return; unpaid recorded fines remain
visible until paid.

## Scheduled messages

| Event | Timing | Content |
| --- | --- | --- |
| Upcoming return | Once per loan, starting three days before due | Member ID, book/copy, return date, days remaining, Tk 10/day rate and first fine date. |
| Overdue fine | Overdue days 1, 11, 21, 31, … | Book, due date, current total estimate, daily fine rate and request to return/pay in full. |
| Returned but unpaid | Same ten-day milestones | Outstanding recorded balance and request for payment; explicitly states that the fine has stopped increasing. |

Dates use Asia/Dhaka. The scheduler checks every five minutes and starts delivery at 09:00 by
default. If the app was offline, it sends the current eligible reminder rather than a backlog of
old messages. A missed pre-due reminder can catch up during the remaining three-day window;
an overdue reminder uses the latest ten-day milestone and today's actual amount.

Messages go to the phone/email registered on the member record. A student account does not need
to remain logged in. Contact and loan/payment status are refreshed immediately before claiming
each message. The sender must remain running with database and internet access. An external
scheduler may run `python -m backend.reminders.worker --once` if the web app is not kept running.

Example pre-due message (sample member):

> PSTU Library: Test Member (PSTU-0002), book: Clean Code (Copy #3). Return by 2026-10-10
> (3 days left). Late fine: Tk 10/day from 2026-10-11. Please return the book to the library
> by the due date to avoid a fine.

On overdue day 11, the email shows Tk 110 estimated fine, the original return deadline and
the instruction to return the book and pay the final fine in full. A returned book with a
remaining Tk 80 balance instead receives a payment reminder for Tk 80 and no daily-growth claim.

## Provider setup

Delivery is disabled until configured. No credit card is needed to use your existing Gmail account
for SMTP, but Gmail has sending limits. For a free setup, use email for the pre-due reminder as well
as overdue reminders; the dashboard alerts continue independently. SMS requires a configured
provider. The current SMS adapter uses Twilio; a Twilio trial has limits and is not an unlimited
free SMS service.

1. Run `python -m backend.upgrade_reminders` to add Oracle delivery tracking. This preserves
   existing library records and does not send messages.
2. Add the reminder variables from `.env.example` to your private `.env`.
3. For Gmail, enable two-step verification and create a Google App Password. Use the App Password
   as `SMTP_PASSWORD`, not your regular Gmail password. Set `SMTP_USERNAME` and `SMTP_FROM` to
   your Gmail address, `SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`, `SMTP_SECURITY=starttls`.
4. Set `EMAIL_REMINDERS_ENABLED=true`, `DUE_REMINDER_CHANNEL=email` and
   `REMINDERS_ENABLED=true`. Leave `SMS_REMINDERS_ENABLED=false` for the free email setup.
5. Restart the server. Check configuration without sending with
   `python -m backend.reminders.worker --check`. Preview message content without sending with
   `python -m backend.reminders.worker --preview`.

To use SMS later, configure `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`,
enable `SMS_REMINDERS_ENABLED`, and set `DUE_REMINDER_CHANNEL=sms`. Registered Bangladeshi
`01…` numbers are converted to `+8801…` for the provider. Actual carrier delivery depends on
the provider account and destination permissions.

## Delivery status and duplicate protection

Oracle `reminder_delivery` records one claim per event key. `ACCEPTED` means the provider accepted
the message, not that a student read it or that final carrier delivery was confirmed. Known provider
rejections become `FAILED`, with at most three attempts separated by 30 minutes. Network timeouts
and interrupted sends become `UNKNOWN`; they are not automatically resent because the original
send may already have succeeded. Stale `SENDING` records are moved to `UNKNOWN` after 15 minutes.

Review delivery metadata with:

```sql
SELECT event_key, channel, status, attempts, updated_at, provider_id
FROM reminder_delivery ORDER BY updated_at DESC;
```

For an `UNKNOWN` record, check the provider's log before any manual resend. Do not delete accepted
records as a routine cleanup: that would allow the same reminder to be sent again. The app stores
event identifiers and provider IDs in this table, not message bodies or passwords. Separate leases
prevent simultaneous workers from sending the same event.

Provider references: [Twilio message API](https://www.twilio.com/docs/messaging/api/message-resource),
[Twilio trial](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account),
[Gmail sending limits](https://support.google.com/mail/answer/22839?hl=en),
[Google App Passwords](https://support.google.com/mail/answer/185833).
