import unittest
from datetime import datetime
from unittest.mock import patch

from backend.routes import fines


class FineCollectionTests(unittest.TestCase):
    def test_totals_use_paid_balances_and_dated_receipts(self):
        with patch.object(fines, "datetime") as clock, patch.object(fines, "rows") as read:
            clock.now.return_value = datetime(2026, 10, 5)
            read.return_value = [{"total": 1250.5, "today": 100, "month": 450.5}]
            result = fines.get_collection_summary()
        self.assertEqual(result["total"], 1250.5)
        self.assertEqual(result["date"], "2026-10-05")
        self.assertEqual(result["month_start"], "2026-10-01")
        sql = read.call_args.args[0]
        self.assertIn("SUM(paid_amount)", sql)
        self.assertIn("FROM fine_payment", sql)
        self.assertIn("paid_at<ADD_MONTHS", sql)
        self.assertIn("'2026-10-05'", sql)
        self.assertIn("'2026-10-01'", sql)

    def test_empty_collections_return_zero(self):
        with patch.object(fines, "rows", return_value=[{"total": 0, "today": 0, "month": 0}]):
            result = fines.get_collection_summary()
        self.assertEqual([result[key] for key in ("total", "today", "month")], [0, 0, 0])
