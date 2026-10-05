"""Exercise the login API over HTTP without changing real Oracle records."""

import http.cookiejar
import json
import socket
import threading
import time
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener

import uvicorn
from fastapi import FastAPI
from backend.auth.routes import register_auth_routes
from backend.auth.session import SESSIONS, install_authentication
from backend.database import quote
from backend.validation import form_data, required


class LoginApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = FastAPI()
        install_authentication(cls.app)
        cls.writes = []
        cls.block_database = False
        cls.query_started = threading.Event()
        cls.release_query = threading.Event()

        def rows(sql, *args):
            if "SELECT membership_status FROM student" in sql:
                return [{"membership_status": "ACTIVE"}]
            if cls.block_database:
                cls.query_started.set()
                cls.release_query.wait(3)
            for name, role, status in (
                ("admin", "ADMIN", "ACTIVE"),
                ("disabled", "LIBRARIAN", "DISABLED"),
                ("student", "STUDENT", "ACTIVE"),
                ("linkedstudent", "STUDENT", "ACTIVE"),
            ):
                if f"LOWER('{name}')" in sql:
                    return [
                        {
                            "user_id": 1,
                            "username": name,
                            "user_type": role,
                            "account_status": status,
                            "password": "test1234",
                            "student_id": 17 if name == "linkedstudent" else None,
                        }
                    ]
            return []

        register_auth_routes(
            cls.app, Path("frontend"), rows, cls.writes.append, quote, form_data, required
        )

        @cls.app.get("/api/private")
        def private():
            return {"ok": True}

        @cls.app.get("/api/health")
        def health():
            return {"ok": True}

        listener = socket.socket()
        listener.bind(("127.0.0.1", 0))
        cls.base = f"http://127.0.0.1:{listener.getsockname()[1]}"
        cls.server = uvicorn.Server(uvicorn.Config(cls.app, log_level="critical", lifespan="off"))
        cls.thread = threading.Thread(
            target=cls.server.run, kwargs={"sockets": [listener]}, daemon=True
        )
        cls.thread.start()
        deadline = time.monotonic() + 5
        while not cls.server.started and time.monotonic() < deadline:
            time.sleep(0.01)
        if not cls.server.started:
            raise RuntimeError("Test server did not start")

    @classmethod
    def tearDownClass(cls):
        cls.release_query.set()
        cls.server.should_exit = True
        cls.thread.join(5)
        SESSIONS.clear()

    def setUp(self):
        SESSIONS.clear()
        self.client = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def request(self, path, data=None, headers=None):
        body = urlencode(data).encode() if isinstance(data, dict) else data
        request = Request(self.base + path, data=body, headers=headers or {})
        try:
            response = self.client.open(request, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            return response.status, json.loads(response.read()), response.headers

    def test_login_session_and_logout(self):
        self.assertEqual(self.request("/api/private")[0], 401)
        status, data, headers = self.request(
            "/api/auth/login", {"username": " admin ", "password": "test1234"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(data["user_type"], "ADMIN")
        self.assertIn("HttpOnly", headers["Set-Cookie"])
        self.assertIn("SameSite=strict", headers["Set-Cookie"])
        self.assertEqual(self.request("/api/auth/session")[0], 200)
        self.assertEqual(self.request("/api/private")[0], 200)
        self.assertEqual(self.request("/api/auth/logout", b"")[0], 200)
        self.assertEqual(self.request("/api/private")[0], 401)

    def test_wrong_password_disabled_and_student(self):
        for username, password, status in (
            ("admin", "wrong", 401),
            ("missing", "test1234", 401),
            ("disabled", "test1234", 403),
            ("student", "test1234", 403),
        ):
            with self.subTest(username=username):
                self.assertEqual(
                    self.request("/api/auth/login", {"username": username, "password": password})[
                        0
                    ],
                    status,
                )

    def test_linked_student_can_login_but_cannot_access_management(self):
        status, data, _ = self.request(
            "/api/auth/login", {"username": "linkedstudent", "password": "test1234"}
        )
        self.assertEqual(status, 200)
        self.assertEqual(data["user_type"], "STUDENT")
        self.assertEqual(self.request("/api/auth/session")[0], 200)
        for path, body in (
            ("/api/private", None),
            ("/api/snapshot", None),
            ("/api/students", None),
            ("/api/student-access", b""),
            ("/api/reservations/1/collect", b""),
            ("/api/books", b""),
        ):
            with self.subTest(path=path):
                self.assertEqual(self.request(path, body)[0], 403)

    def test_invalid_and_duplicate_form_fields(self):
        for body in (
            b"username=admin&username=student&password=test1234",
            b"username=%FF&password=test1234",
            b"username=%ZZ&password=test1234",
            b"username=%20&password=test1234",
        ):
            with self.subTest(body=body):
                self.assertEqual(self.request("/api/auth/login", body)[0], 400)
        self.assertEqual(
            self.request("/api/auth/login", {"username": "admin", "password": "x" * 129})[0], 400
        )

    def test_cross_origin_login_blocked(self):
        self.assertEqual(
            self.request(
                "/api/auth/login",
                {"username": "admin", "password": "test1234"},
                {"Origin": "https://example.invalid"},
            )[0],
            403,
        )

    def test_activation_is_public_and_cross_origin_changes_are_blocked(self):
        self.assertEqual(self.request("/api/auth/activate", {"memberId": "bad"})[0], 400)
        self.assertEqual(
            self.request("/api/auth/activate", {}, {"Origin": "https://example.invalid"})[0], 403
        )
        self.assertEqual(self.request("/api/auth/reset-password", {"memberId": "admin"})[0], 400)
        self.assertEqual(
            self.request("/api/auth/reset-password", {}, {"Origin": "https://example.invalid"})[0],
            403,
        )

    def test_slow_database_does_not_block_health(self):
        cls = type(self)
        cls.query_started.clear()
        cls.release_query.clear()
        cls.block_database = True
        worker = threading.Thread(
            target=lambda: self.request(
                "/api/auth/login", {"username": "admin", "password": "test1234"}
            )
        )
        try:
            worker.start()
            self.assertTrue(cls.query_started.wait(2))
            started = time.monotonic()
            response = build_opener().open(cls.base + "/api/health", timeout=1)
            with response:
                self.assertEqual(response.status, 200)
            self.assertLess(time.monotonic() - started, 1)
        finally:
            cls.block_database = False
            cls.release_query.set()
            worker.join(5)


if __name__ == "__main__":
    unittest.main()
