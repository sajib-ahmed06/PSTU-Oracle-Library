import asyncio
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from starlette.requests import Request
from backend import main, reservations
from backend.auth.session import create_session, remove_session, SESSION_COOKIE


class ReservationTests(unittest.TestCase):
    def setUp(self):
        self.token = create_session(
            {"user_id": 500, "username": "studentqa", "user_type": "STUDENT", "student_id": 17}
        )

    def tearDown(self):
        remove_session(self.token)

    def request(self, body=""):
        async def receive():
            return {"type": "http.request", "body": body.encode(), "more_body": False}

        return Request(
            {
                "type": "http",
                "method": "POST",
                "headers": [(b"cookie", f"{SESSION_COOKIE}={self.token}".encode())],
            },
            receive,
        )

    def endpoint(self, path, method=None):
        return next(
            route.endpoint
            for route in main.app.routes
            if getattr(route, "path", None) == path and (method is None or method in route.methods)
        )

    def test_student_cannot_reserve_for_another_member(self):
        with (
            patch.object(reservations, "rows", return_value=[{"membership_status": "ACTIVE"}]),
            patch.object(reservations, "run_sql") as run,
        ):
            asyncio.run(
                self.endpoint("/api/reservations", "POST")(self.request("bookId=4&studentId=99"))
            )
        self.assertIn("reserve_book_proc(17,4)", run.call_args.args[0])

    def test_student_cancellation_checks_owner_in_sql(self):
        with (
            patch.object(reservations, "rows", return_value=[{"membership_status": "ACTIVE"}]),
            patch.object(reservations, "run_sql") as run,
        ):
            asyncio.run(
                self.endpoint("/api/reservations/{reservation_id}/cancel")(88, self.request())
            )
        self.assertEqual(run.call_args.args[0].count("AND student_id=17"), 2)

    def test_student_cannot_collect(self):
        with (
            patch.object(reservations, "rows", return_value=[{"membership_status": "ACTIVE"}]),
            patch.object(reservations, "run_sql") as run,
        ):
            for path, args in (
                ("/api/reservations/{reservation_id}/collect", (88, self.request())),
            ):
                with self.subTest(path=path), self.assertRaises(HTTPException) as error:
                    asyncio.run(self.endpoint(path)(*args))
                self.assertEqual(error.exception.status_code, 403)
        run.assert_not_called()

    def test_disabled_membership_blocks_student_data(self):
        with (
            patch.object(reservations, "rows", return_value=[{"membership_status": "DISABLED"}]),
            self.assertRaises(HTTPException) as error,
        ):
            self.endpoint("/api/student/dashboard")(self.request())
        self.assertEqual(error.exception.status_code, 403)

    def test_dashboard_queries_scope_loans_and_fines_before_execution(self):
        # Keep the real query collector; replace only the Oracle transport.
        with (
            patch.object(reservations, "rows", wraps=reservations.rows) as query,
            patch("backend.database.run_sql", return_value="ACTIVE"),
            patch.object(
                reservations, "read_many", return_value=[[], [{"student_id": 17}], [], [], []]
            ) as batch,
        ):
            self.endpoint("/api/student/dashboard")(self.request())
        queries = batch.call_args.args[0]
        self.assertIn("WHERE i.student_id=17", queries[2][0])
        self.assertIn("WHERE i.student_id=17", queries[3][0])
        self.assertIn("WHERE r.student_id=17", queries[4][0])
