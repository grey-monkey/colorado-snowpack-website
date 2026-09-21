import unittest
from datetime import date
from pipeline.proof import observation_date, percentage, number


class DataRules(unittest.TestCase):
    def test_rollover(self):
        self.assertEqual(observation_date(2026, '10-01'), date(2025, 10, 1))
        self.assertEqual(observation_date(2026, '09-30'), date(2026, 9, 30))

    def test_leap_day_is_not_shifted(self):
        self.assertIsNone(observation_date(2025, '02-29'))
        self.assertEqual(observation_date(2024, '02-29'), date(2024, 2, 29))

    def test_missing_is_not_zero(self):
        self.assertIsNone(percentage(None, 2))
        self.assertEqual(percentage(0, 2), 0)

    def test_reference_threshold(self):
        for median in (None, 0, 0.099):
            self.assertIsNone(percentage(1, median))
        self.assertEqual(percentage(0.08, 0.1), 80)

    def test_invalid_values_rejected(self):
        for value in (float('nan'), float('inf'), -1, '0', True):
            with self.assertRaises(ValueError):
                number(value)


if __name__ == '__main__':
    unittest.main()
