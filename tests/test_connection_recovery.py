import subprocess
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from backend import database


class ConnectionRecoveryTests(unittest.TestCase):
    def result(self, text="1", code=0):
        return SimpleNamespace(stdout=text, stderr="", returncode=code)

    def test_listener_rejection_retries_before_sql_execution(self):
        error = self.result("ORA-12520: listener has no available handler", 1)
        with (
            patch.object(database.subprocess, "run", side_effect=[error, self.result()]) as run,
            patch.object(database.time, "sleep"),
        ):
            self.assertEqual(database.run_sql("SELECT 1 FROM dual;"), "1")
        self.assertEqual(run.call_count, 2)
        script = run.call_args.kwargs["input"]
        self.assertLess(script.index("WHENEVER SQLERROR"), script.index("CONNECT "))

    def test_read_disconnect_retries_but_mutation_never_replays(self):
        error = self.result("ORA-03113: end-of-file on communication channel", 1)
        with (
            patch.object(database.subprocess, "run", side_effect=[error, self.result()]) as run,
            patch.object(database.time, "sleep"),
        ):
            database.run_sql("SELECT 1 FROM dual;")
            self.assertEqual(run.call_count, 2)
        with (
            patch.object(database.subprocess, "run", return_value=error) as run,
            patch.object(database.time, "sleep"),
            self.assertRaises(HTTPException),
        ):
            database.run_sql("UPDATE fine SET payment_status='PAID'; COMMIT;")
        self.assertEqual(run.call_count, 1)

    def test_timeout_does_not_replay_mutation_and_releases_slot(self):
        with (
            patch.object(
                database.subprocess, "run", side_effect=subprocess.TimeoutExpired("sqlplus", 20)
            ) as run,
            patch.object(database.time, "sleep"),
            self.assertRaises(HTTPException) as error,
        ):
            database.run_sql("UPDATE fine SET payment_status='PAID'; COMMIT;")
        self.assertEqual(error.exception.status_code, 504)
        self.assertEqual(run.call_count, 1)
        self.assertTrue(database.SQL_SLOTS.acquire(blocking=False))
        database.SQL_SLOTS.release()

    def test_normal_data_containing_oracle_error_text_is_not_an_error(self):
        with (
            patch.object(
                database.subprocess, "run", return_value=self.result("1|A book about ORA-12520")
            ),
            patch.object(database.time, "sleep"),
        ):
            self.assertEqual(
                database.run_sql("SELECT title FROM book;"), "1|A book about ORA-12520"
            )

    def test_batch_uses_one_connection_and_keeps_sections_separate(self):
        output = "__LIBRARY_READ_0__\n1|First\n__LIBRARY_READ_1__\n__LIBRARY_READ_2__\n2|Second"
        queries = [
            ("SELECT 1 FROM dual", ["id", "name"], {"id"}),
            ("SELECT 2 FROM dual", ["id"], {"id"}),
            ("SELECT 3 FROM dual", ["id", "name"], {"id"}),
        ]
        with patch.object(database, "run_sql", return_value=output) as run:
            result = database.read_many(queries)
        self.assertEqual(result, [[{"id": 1, "name": "First"}], [], [{"id": 2, "name": "Second"}]])
        run.assert_called_once()
        self.assertTrue(run.call_args.kwargs["read_batch"])

    def test_collect_reads_is_scoped_and_does_not_execute_queries(self):
        with patch.object(database, "run_sql") as run:
            with database.collect_reads() as queries:
                self.assertEqual(database.rows("SELECT 1 FROM dual", ["id"], {"id"}), [])
            run.assert_not_called()
        self.assertEqual(len(queries), 1)
        self.assertIsNone(database.PENDING_READS.get())

    def test_batch_rejects_incomplete_output_and_writes(self):
        with patch.object(database, "run_sql", return_value=""):
            with self.assertRaises(HTTPException):
                database.read_many([("SELECT 1 FROM dual", ["id"], {"id"})])
        with patch.object(database, "run_sql") as run:
            with self.assertRaises(ValueError):
                database.read_many([("UPDATE book SET quantity=1", ["id"], set())])
            run.assert_not_called()
