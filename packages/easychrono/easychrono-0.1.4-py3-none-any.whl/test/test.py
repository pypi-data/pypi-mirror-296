import unittest
from datetime import datetime, timedelta
from easychrono.parser import parse_delta, parse_relative_date
from easychrono.formatter import format_timedelta
from easychrono.operations import add_timedelta, subtract_timedelta
from easychrono.utils import create_timedelta, validate_timedelta_input, duration_from_now

class TestEasyDelta(unittest.TestCase):
    def test_parse_delta(self):
        self.assertEqual(parse_delta("5d3h30m45s"), timedelta(days=5, hours=3, minutes=30, seconds=45))

    def test_format_timedelta(self):
        self.assertEqual(format_timedelta(timedelta(days=5, hours=3, minutes=30, seconds=45)), "5 days, 3 hours, 30 minutes, 45 seconds")

    def test_add_timedelta(self):
        td1 = timedelta(days=5)
        td2 = timedelta(days=3)
        self.assertEqual(add_timedelta(td1, td2), timedelta(days=8))

    def test_subtract_timedelta(self):
        td1 = timedelta(days=5)
        td2 = timedelta(days=3)
        self.assertEqual(subtract_timedelta(td1, td2), timedelta(days=2))

    def test_create_timedelta(self):
        self.assertEqual(create_timedelta(days=1, hours=2, minutes=30), timedelta(days=1, hours=2, minutes=30))

    def test_validate_timedelta_input(self):
        self.assertTrue(validate_timedelta_input("5d3h30m45s"))
        self.assertFalse(validate_timedelta_input("invalid"))

    def test_duration_from_now(self):
        now = datetime.now()
        future_time = now + timedelta(days=1, hours=5, minutes=30)
        self.assertEqual(duration_from_now(future_time), "1 days, 5 hours, 30 minutes")

    def test_parse_relative_date(self):
        # Test "tomorrow"
        self.assertEqual(parse_relative_date("tomorrow").date(), (datetime.now() + timedelta(days=1)).date())
        
        # Test "next Monday"
        today_weekday = datetime.now().weekday()
        days_until_next_monday = (0 - today_weekday + 7) % 7 or 7
        expected_next_monday = datetime.now() + timedelta(days=days_until_next_monday)
        self.assertEqual(parse_relative_date("next Monday").date(), expected_next_monday.date())
        
        # Test "in 3 weeks"
        expected_in_3_weeks = datetime.now() + timedelta(weeks=3)
        self.assertEqual(parse_relative_date("in 3 weeks").date(), expected_in_3_weeks.date())

        # Test "in 5 days"
        expected_in_5_days = datetime.now() + timedelta(days=5)
        self.assertEqual(parse_relative_date("in 5 days").date(), expected_in_5_days.date())

if __name__ == '__main__':
    unittest.main()
