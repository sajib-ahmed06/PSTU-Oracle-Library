from backend.routes import circulation, fines
import asyncio
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from starlette.requests import Request
from backend import main
from backend.validation import payment_amount


def request(body):
    async def receive():
        return {"type": "http.request", "body": body.encode(), "more_body": False}

    return Request({"type": "http", "method": "POST", "headers": []}, receive)


class CirculationTests(unittest.TestCase):
    def test_batch_has_one_commit_and_preserves_copy_selection(self):
        with patch.object(circulation, "run_sql") as run:
            result = asyncio.run(
                main.add_issue(
                    request(
                        "studentId=2&bookId=1&copyId=11&bookId2=1&copyId2=12&bookId3=3&copyId3=31"
                    )
                )
            )
        sql = run.call_args.args[0]
        self.assertEqual(sql.count("COMMIT"), 1)
        self.assertIn("issue_book_proc(2, 1, 11)", sql)
        self.assertIn("issue_book_proc(2, 1, 12)", sql)
        self.assertIn("issue_book_proc(2, 3, 31)", sql)
        self.assertEqual(result["message"], "3 book copies issued")

    def test_invalid_copy_never_executes_sql(self):
        with patch.object(circulation, "run_sql") as run, self.assertRaises(HTTPException):
            asyncio.run(main.add_issue(request("studentId=2&bookId=1&copyId=-1")))
        run.assert_not_called()

    def test_money_uses_decimal_and_rejects_invalid_values(self):
        self.assertEqual(payment_amount("0.10"), "0.10")
        self.assertEqual(payment_amount("35.25"), "35.25")
        for value in ("0", "-1", "NaN", "Infinity", "1.001", "abc", "10000000000"):
            with self.subTest(value=value), self.assertRaises(HTTPException):
                payment_amount(value)

    def test_payment_rejects_custom_amount_and_invalid_note(self):
        for body in ("amount=35.25", "amount=0", "note=%00"):
            with (
                self.subTest(body=body),
                patch.object(fines, "run_sql") as run,
                self.assertRaises(HTTPException),
            ):
                asyncio.run(main.pay_fine(1, request(body)))
            run.assert_not_called()

    def test_payment_uses_locked_database_balance(self):
        with patch.object(fines, "run_sql") as run:
            result = asyncio.run(main.pay_fine(1, request("note=Full+payment")))
        self.assertIn("pay_fine_proc(1, NULL, 'Full payment')", run.call_args.args[0])
        self.assertEqual(result["message"], "Fine paid in full")
