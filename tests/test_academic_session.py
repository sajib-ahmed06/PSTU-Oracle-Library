import unittest

from fastapi import HTTPException
from backend.validation import academic_session


class AcademicSessionTests(unittest.TestCase):
    def test_accepts_consecutive_years_and_trims(self):
        self.assertEqual(academic_session(" 2023-2024 "), "2023-2024")

    def test_rejects_invalid_formats_and_year_ranges(self):
        for value in (
            "",
            "2023",
            "2023/2024",
            "2023-2025",
            "2024-2023",
            "２０２３-２０２４",
            "2023-25",
            "9999-00",
        ):
            with self.subTest(value=value), self.assertRaises(HTTPException):
                academic_session(value)

    def test_short_format_normalizes_and_handles_century_boundary(self):
        self.assertEqual(academic_session(" 2023-24 "), "2023-2024")
        self.assertEqual(academic_session("1999-00"), "1999-2000")
