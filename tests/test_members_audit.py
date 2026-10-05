from backend.routes import members, audit
import asyncio
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from backend import database, main
from backend.audit import audit_actor
from backend.auth.session import SESSIONS, create_session
from backend.validation import academic_identifier


class MemberAuditTests(unittest.TestCase):
    def tearDown(self):
        SESSIONS.clear()

    def request(self, body):
        async def read_body():
            return body

        return SimpleNamespace(body=read_body)

    def test_identifiers_keep_leading_zeros_and_normalize_case(self):
        self.assertEqual(academic_identifier(" 0012-ab ", "Roll"), "0012-AB")
        self.assertEqual(academic_identifier("2024/001", "Registration"), "2024/001")
        for invalid in ("", "  ", "a b", "A|B", "x" * 41, "???"):
            with self.subTest(invalid=invalid), self.assertRaises(HTTPException):
                academic_identifier(invalid, "Roll")

    def test_new_members_require_both_identifiers(self):
        request = self.request(
            b"name=Test&department=CSE&phone=01700000099&email=test%40example.com"
        )
        with patch.object(members, "run_sql") as run, self.assertRaises(HTTPException) as error:
            asyncio.run(main.add_student(request))
        self.assertEqual(error.exception.status_code, 400)
        run.assert_not_called()

    def test_member_insert_passes_both_identifiers_to_database(self):
        request = self.request(
            b"name=Test&department=CSE&phone=01700000099&email=test%40example.com&roll_no=001-ab&registration_no=reg-001&academic_session=2023-2024"
        )
        with patch.object(members, "run_sql", return_value="0") as run:
            asyncio.run(main.add_student(request))
        sql = run.call_args.args[0]
        self.assertIn("'001-AB'", sql)
        self.assertIn("'REG-001'", sql)

    def test_duplicate_constraint_errors_have_specific_messages(self):
        for index, message in (
            ("UQ_STUDENT_ROLL", "ID/Roll"),
            ("UQ_STUDENT_REGISTRATION", "Registration"),
        ):
            result = SimpleNamespace(
                stdout=f"ORA-00001: unique constraint (CONFIGURED_SCHEMA.{index}) violated",
                stderr="",
                returncode=1,
            )
            with (
                patch.object(database.subprocess, "run", return_value=result),
                self.assertRaises(HTTPException) as error,
            ):
                database.run_sql("UPDATE student SET roll_no='001';")
            self.assertEqual(error.exception.status_code, 409)
            self.assertIn(message, error.exception.detail)

    def test_edit_identifiers_checks_missing_member(self):
        with patch.object(members, "run_sql") as run:
            asyncio.run(
                main.update_student_identity(
                    999, self.request(b"roll_no=001&registration_no=REG-001")
                )
            )
        self.assertIn("SQL%ROWCOUNT = 0", run.call_args.args[0])

    def test_full_member_edit_validates_and_updates_all_fields(self):
        body = b"name=Updated+Name&department=EEE&phone=01700000099&email=updated%40example.com&roll_no=001-ab&registration_no=REG-001&membership_status=ACTIVE&academic_session=2023-2024"
        with patch.object(members, "run_sql") as run:
            asyncio.run(main.edit_student(1, self.request(body)))
        sql = run.call_args.args[0]
        for value in (
            "Updated Name",
            "EEE",
            "01700000099",
            "updated@example.com",
            "001-AB",
            "REG-001",
        ):
            self.assertIn(value, sql)
        self.assertIn("FOR UPDATE", sql)
        self.assertIn("Return all issued books", sql)
        self.assertIn("Pay all fines", sql)

    def test_full_member_edit_rejects_invalid_contact_and_status(self):
        from urllib.parse import urlencode

        data = {
            "name": "Test",
            "department": "CSE",
            "phone": "01700000099",
            "email": "test@example.com",
            "roll_no": "001",
            "registration_no": "REG-001",
            "membership_status": "ACTIVE",
            "academic_session": "2023-2024",
        }
        for field, value in (
            ("phone", "123"),
            ("email", "invalid"),
            ("membership_status", "UNKNOWN"),
        ):
            with (
                self.subTest(field=field),
                patch.object(members, "run_sql") as run,
                self.assertRaises(HTTPException) as error,
            ):
                asyncio.run(
                    main.edit_student(1, self.request(urlencode({**data, field: value}).encode()))
                )
            self.assertEqual(error.exception.status_code, 400)
            run.assert_not_called()

    def test_audit_requires_administrator(self):
        token = create_session({"user_id": 1, "username": "staff", "user_type": "LIBRARIAN"})
        with patch.object(audit, "rows") as query, self.assertRaises(HTTPException) as error:
            main.get_audit(SimpleNamespace(cookies={"library_session": token}))
        self.assertEqual(error.exception.status_code, 403)
        query.assert_not_called()

    def test_audit_decodes_snapshots_and_paginates(self):
        token = create_session({"user_id": 1, "username": "admin", "user_type": "ADMIN"})
        request = SimpleNamespace(cookies={"library_session": token})
        snapshot = {"name": "O'Reilly | Test", "roll_no": "001"}
        encoded = json.dumps(snapshot).encode().hex()
        item = {
            "audit_id": 26,
            "occurred_at": "2026-10-03T12:00:00.000Z",
            "actor": "admin".encode().hex(),
            "action": "UPDATE",
            "entity": "STUDENT",
            "record_id": 1,
            "before": None,
            "after": encoded,
        }
        with patch.object(audit, "rows", side_effect=[[{"total": 26}], [item]]) as query:
            result = main.get_audit(request, entity="STUDENT", page=2)
        self.assertEqual(result["items"][0]["after"], snapshot)
        self.assertEqual(result["items"][0]["actor"], "admin")
        self.assertIn("ROWNUM <= 50", query.call_args.args[0])
        self.assertIn("row_number > 25", query.call_args.args[0])

    def test_request_actor_is_sent_to_oracle_session(self):
        token = audit_actor.set("admin")
        try:
            with patch.object(
                database.subprocess,
                "run",
                return_value=SimpleNamespace(stdout="", stderr="", returncode=0),
            ) as run:
                database.run_sql("SELECT 1 FROM dual;")
            self.assertIn("SET_CLIENT_INFO('admin')", run.call_args.kwargs["input"])
        finally:
            audit_actor.reset(token)


if __name__ == "__main__":
    unittest.main()
