"""Integration checks use frozen, real NRCS products; no invented observations."""
import copy
import json
import unittest
from pathlib import Path
from pipeline.proof import verify

FIXTURES = Path(__file__).resolve().parents[1] / 'evidence' / '2026-09-21'


class SourceProof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = json.loads((FIXTURES / 'state.json').read_text())
        cls.html = (FIXTURES / 'state-chart.html').read_text()

    def test_both_products_match_official_charts(self):
        total = 0
        for key in ['state', 'basin']:
            rows = json.loads((FIXTURES / f'{key}.json').read_text())
            normalized, report = verify(rows, (FIXTURES / f'{key}-chart.html').read_text(), key)
            self.assertEqual(report['latest']['observation_date'], '2026-09-21')
            self.assertIsNone(report['latest']['percent_of_median'])
            self.assertTrue(any(r['swe_inches'] is None for r in normalized))
            total += report['matched_values']
        self.assertEqual(total, 30378)

    def test_corrupt_value_is_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows[120]['2026'] += 1
        with self.assertRaisesRegex(ValueError, 'Value mismatch'):
            verify(rows, self.html, 'state')

    def test_missing_must_not_be_replaced_with_zero(self):
        rows = copy.deepcopy(self.rows)
        row = next(r for r in rows if r['2026'] is None)
        row['2026'] = 0
        with self.assertRaisesRegex(ValueError, 'Null mismatch'):
            verify(rows, self.html, 'state')

    def test_duplicate_date_is_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows[1]['date'] = rows[0]['date']
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            verify(rows, self.html, 'state')

    def test_changed_units_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'units'):
            verify(self.rows, self.html.replace('Snow Water Equivalent (in.)', 'Snow depth (cm)'), 'state')
