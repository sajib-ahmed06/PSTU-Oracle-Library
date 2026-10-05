import asyncio
import unittest
from unittest.mock import patch
from urllib.parse import urlencode
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import Mock

from fastapi import HTTPException
from starlette.requests import Request
from backend.auth.routes import member_number, register_auth_routes
from backend.auth.passwords import verify_password
from backend.database import quote
from backend.validation import form_data, required


def request(fields):
    async def receive():
        return {"type": "http.request", "body": urlencode(fields).encode(), "more_body": False}

    return Request(
        {
            "type": "http",
            "method": "POST",
            "scheme": "http",
            "path": "/api/auth/login",
            "server": ("localhost", 8091),
            "headers": [],
        },
        receive,
    )


class ActivationTests(unittest.TestCase):
    def setUp(self):
        routes = []
        self.rows = Mock(return_value=[])
        register_auth_routes(
            SimpleNamespace(include_router=lambda router: routes.extend(router.routes)),
            Path("frontend"),
            self.rows,
            Mock(),
            quote,
            form_data,
            required,
        )
        self.activate = next(r.endpoint for r in routes if r.path == "/api/auth/activate")
        self.login = next(r.endpoint for r in routes if r.path == "/api/auth/login")
        self.reset = next(r.endpoint for r in routes if r.path == "/api/auth/reset-password")
        self.fields = {
            "memberId": "pstu-0007",
            "phone": "01700000007",
            "password": "Secret1234",
            "confirmPassword": "Secret1234",
        }

    def test_member_id_parsing_preserves_library_identity(self):
        for value in ("PSTU-0007", "pstu-7", "0007", " 7 "):
            self.assertEqual(member_number(value), 7)
        for value in ("PSTU-0000", "-7", "roll-7", "7 OR 1=1", "7.0", ""):
            with self.subTest(value=value), self.assertRaises(HTTPException):
                member_number(value)

    def test_activation_uses_hash_and_atomic_database_procedure(self):
        from backend.auth.passwords import hash_password

        password_hash = hash_password(self.fields["password"])
        with (
            patch("backend.auth.member_access.run_sql") as run,
            patch("backend.auth.member_access.hash_password", return_value=password_hash),
        ):
            result = asyncio.run(self.activate(request(self.fields)))
        sql = run.call_args.args[0]
        self.assertIn("activate_student_proc(7,'01700000007','pbkdf2$", sql)
        self.assertNotIn("Secret1234", sql)
        self.assertTrue(verify_password(self.fields["password"], password_hash))
        self.assertEqual(result["member_id"], "PSTU-0007")

    def test_invalid_fields_never_reach_database(self):
        for field, value in (
            ("phone", "1700000007"),
            ("phone", "0170000000x"),
            ("memberId", "PSTU-0"),
            ("password", "123"),
            ("confirmPassword", "Different"),
        ):
            data = {**self.fields, field: value}
            with (
                self.subTest(field=field, value=value),
                patch("backend.auth.member_access.run_sql") as run,
                self.assertRaises(HTTPException),
            ):
                asyncio.run(self.activate(request(data)))
            run.assert_not_called()

    def test_member_id_login_queries_linked_student_and_redirect_role(self):
        from backend.auth.passwords import hash_password
        from backend.auth.session import SESSIONS, remove_session

        self.rows.side_effect = [
            [
                {
                    "user_id": 907,
                    "username": "PSTU-0007",
                    "user_type": "STUDENT",
                    "account_status": "ACTIVE",
                    "student_id": 7,
                    "password": hash_password("Secret1234"),
                }
            ],
            [{"membership_status": "ACTIVE"}],
        ]
        try:
            response = asyncio.run(
                self.login(request({"username": "pstu-0007", "password": "Secret1234"}))
            )
            self.assertEqual(response.status_code, 200)
            sql = self.rows.call_args_list[0].args[0]
            self.assertIn("student_id=7 AND user_type='STUDENT'", sql)
        finally:
            for token, session in list(SESSIONS.items()):
                if session["user_id"] == 907:
                    remove_session(token)

    def test_recovery_requires_every_registered_detail_and_hashes_password(self):
        fields = {
            **self.fields,
            "rollNo": " 007 ",
            "registrationNo": "reg-007",
            "email": "Member@Example.com",
        }
        with patch("backend.auth.member_access.run_sql") as run:
            result = asyncio.run(self.reset(request(fields)))
        sql = run.call_args.args[0]
        self.assertIn(
            "reset_student_password_proc(7,'007','REG-007','01700000007','member@example.com','pbkdf2$",
            sql,
        )
        self.assertNotIn("Secret1234", sql)
        self.assertEqual(result["member_id"], "PSTU-0007")
        for key in fields:
            missing = {k: v for k, v in fields.items() if k != key}
            with (
                self.subTest(key=key),
                patch("backend.auth.member_access.run_sql") as run,
                self.assertRaises(HTTPException),
            ):
                asyncio.run(self.reset(request(missing)))
            run.assert_not_called()

    def test_recovery_rejects_staff_username_and_invalid_email(self):
        fields = {
            **self.fields,
            "rollNo": "007",
            "registrationNo": "REG-007",
            "email": "member@example.com",
        }
        for key, value in (
            ("memberId", "admin"),
            ("email", "bad-email"),
            ("confirmPassword", "different"),
        ):
            with (
                self.subTest(key=key),
                patch("backend.auth.member_access.run_sql") as run,
                self.assertRaises(HTTPException),
            ):
                asyncio.run(self.reset(request({**fields, key: value})))
            run.assert_not_called()

    def test_recovery_invalidates_only_the_members_sessions(self):
        from backend.auth.session import create_session, SESSIONS, remove_session

        member_token = create_session(
            {"user_id": 907, "username": "PSTU-0007", "user_type": "STUDENT", "student_id": 7}
        )
        staff_token = create_session({"user_id": 908, "username": "adminqa", "user_type": "ADMIN"})
        self.rows.return_value = [{"user_id": 907}]
        try:
            fields = {
                **self.fields,
                "rollNo": "007",
                "registrationNo": "REG-007",
                "email": "member@example.com",
            }
            with patch("backend.auth.member_access.run_sql"):
                asyncio.run(self.reset(request(fields)))
            self.assertNotIn(member_token, SESSIONS)
            self.assertIn(staff_token, SESSIONS)
        finally:
            remove_session(member_token)
            remove_session(staff_token)
