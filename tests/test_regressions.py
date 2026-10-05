from backend.routes import fines
import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from backend.auth.routes import register_auth_routes
from backend import database, main
from backend.auth.passwords import hash_password, verify_password
from backend.auth.session import SESSIONS, create_session, current_session, invalidate_user_sessions
from backend.validation import form_data, required


class RegressionTests(unittest.TestCase):
    def tearDown(self):
        SESSIONS.clear()

    def test_password_hash_and_legacy_compatibility(self):
        stored = hash_password("test-password")
        self.assertLessEqual(len(stored), 100)
        self.assertTrue(verify_password("test-password", stored))
        self.assertFalse(verify_password("wrong", stored))
        self.assertTrue(verify_password("legacy", "legacy"))
        self.assertFalse(verify_password("test", "pbkdf2$broken"))

    def test_sqlplus_control_input_rejected(self):
        self.assertEqual(database.quote("O'Reilly & Co"), "'O''Reilly & Co'")
        self.assertEqual(database.quote(0), "'0'")
        with self.assertRaises(HTTPException):
            database.quote("value\n/\nHOST command")

    def test_form_blank_and_invalid_utf8(self):
        async def body():
            return b"publisher=&title=Clean+Code"

        request = SimpleNamespace(body=body)
        data = asyncio.run(form_data(request))
        self.assertEqual(data["publisher"], "")
        with self.assertRaises(HTTPException):
            required({"title": "   "}, "title")

    def test_login_upgrades_legacy_password(self):
        app = FastAPI()
        writes = []

        def users(*args):
            return [
                {
                    "user_id": 1,
                    "username": "admin",
                    "user_type": "ADMIN",
                    "account_status": "ACTIVE",
                    "password": "fixture-password",
                }
            ]

        with patch.object(app, "include_router") as include:
            register_auth_routes(
                app, None, users, writes.append, database.quote, form_data, required
            )
        router = include.call_args.args[0]
        endpoint = next(
            route.endpoint for route in router.routes if route.path == "/api/auth/login"
        )

        async def receive():
            return {
                "type": "http.request",
                "body": b"username=admin&password=fixture-password",
                "more_body": False,
            }

        request = Request(
            {
                "type": "http",
                "method": "POST",
                "path": "/api/auth/login",
                "scheme": "http",
                "headers": [],
                "server": ("localhost", 8091),
                "query_string": b"",
            },
            receive,
        )
        response = asyncio.run(endpoint(request))
        self.assertEqual(response.status_code, 200)
        self.assertIn("HttpOnly", response.headers["set-cookie"])
        self.assertIn("pbkdf2$", writes[0])
        self.assertNotIn("password='fixture-password'", writes[0])

    def test_invalid_utf8_form_rejected(self):
        async def body():
            return b"name=\xff"

        with self.assertRaises(HTTPException) as error:
            asyncio.run(form_data(SimpleNamespace(body=body)))
        self.assertEqual(error.exception.status_code, 400)

    def test_sessions_expire_and_invalidate(self):
        token = create_session({"user_id": 1, "username": "admin", "user_type": "ADMIN"})
        request = SimpleNamespace(cookies={"library_session": token})
        self.assertIsNotNone(current_session(request))
        invalidate_user_sessions(1)
        self.assertIsNone(current_session(request))
        token = create_session({"user_id": 1, "username": "admin", "user_type": "ADMIN"})
        SESSIONS[token]["expires"] = 0
        self.assertIsNone(current_session(SimpleNamespace(cookies={"library_session": token})))

    def test_row_parser_fails_on_corrupt_records(self):
        with patch.object(database, "run_sql", return_value="1|Clean Code|5"):
            self.assertEqual(
                database.rows("SELECT", ["id", "title", "stock"], {"id", "stock"})[0]["stock"], 5
            )
        with patch.object(database, "run_sql", return_value="1|unexpected|delimiter"):
            with self.assertRaises(HTTPException):
                database.rows("SELECT", ["id", "title"])

    def test_missing_fine_is_checked_in_transaction(self):
        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        request = Request({"type": "http", "method": "POST", "headers": []}, receive)
        with patch.object(fines, "run_sql") as run:
            asyncio.run(main.pay_fine(123, request))
            self.assertIn("pay_fine_proc(123, NULL", run.call_args.args[0])
            self.assertIn("COMMIT", run.call_args.args[0])
        with self.assertRaises(HTTPException):
            asyncio.run(main.pay_fine(-1, request))

    def test_sqlplus_errors_are_mapped_and_rollback_enabled(self):
        result = SimpleNamespace(stdout="ORA-20001: Book is not available", stderr="", returncode=1)
        with patch.object(database.subprocess, "run", return_value=result) as run:
            with self.assertRaises(HTTPException) as error:
                database.run_sql("SELECT 1 FROM dual;")
            self.assertEqual(error.exception.status_code, 409)
            self.assertIn("ROLLBACK", run.call_args.kwargs["input"])
            self.assertIn("SET DEFINE OFF", run.call_args.kwargs["input"])
            self.assertEqual(run.call_args.args[0][-1], "/nolog")


if __name__ == "__main__":
    unittest.main()
