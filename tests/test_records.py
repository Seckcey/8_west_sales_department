import copy
import json
import unittest
from pathlib import Path
from scripts.validate_records import validate, campaign_eligible, production_records

ROOT = Path(__file__).resolve().parents[1]


class RecordSafetyTests(unittest.TestCase):
    def setUp(self):
        self.records = json.loads((ROOT / "fixtures/prospects.json").read_text())
        self.record = copy.deepcopy(self.records[0])

    def test_fixtures_cover_three_regions_and_are_excluded(self):
        self.assertEqual(validate(self.records), [])
        self.assertEqual(len({r['territory'] for r in self.records}), 3)
        self.assertEqual(production_records(self.records), [])

    def test_duplicate_is_case_insensitive(self):
        dupe = copy.deepcopy(self.record)
        dupe['id'] = 'another-id'
        dupe['email'] = '  ' + dupe['email'].upper() + '  '
        self.assertTrue(any('duplicate email' in e for e in validate([self.record, dupe])))

    def test_approval_never_makes_synthetic_sendable(self):
        self.record.update(stage='approved_for_outreach', outreach_approval='approved')
        self.assertFalse(campaign_eligible(self.record, campaign_enabled=True))

    def test_suppression_wins_over_approval(self):
        self.record.update(suppressed=True, stage='approved_for_outreach', outreach_approval='approved')
        self.assertTrue(validate([self.record]))
        self.assertFalse(campaign_eligible(self.record, campaign_enabled=True))

    def test_unknown_price_is_null_not_zero(self):
        self.assertIsNone(self.record['price'])
        self.record['price'] = 49
        self.assertTrue(any('approved quote' in e for e in validate([self.record])))

    def test_missing_boolean_fails_closed(self):
        del self.record['synthetic']
        self.assertTrue(validate([self.record]))
        with self.assertRaises(ValueError):
            production_records([self.record])

    def test_invalid_structure_is_reported(self):
        self.assertTrue(validate({}))
        self.assertTrue(validate([None]))
        self.record['territory'] = []
        self.assertTrue(validate([self.record]))

    def test_dates_need_timezone(self):
        self.record['next_action_at'] = '2026-09-25'
        self.assertTrue(any('timezone' in e for e in validate([self.record])))

    def test_malformed_source_fails_closed(self):
        for source in ('https://[broken', 'https://user:password@example.com', 'https://exa mple.com'):
            self.record['source_url'] = source
            self.assertTrue(validate([self.record]))
            self.assertFalse(campaign_eligible(self.record, campaign_enabled=True))

    def test_campaign_is_off_by_default_even_for_an_approved_record(self):
        self.record.update(synthetic=False, email='sales@fictional.invalid',
                           stage='approved_for_outreach', outreach_approval='approved')
        self.assertFalse(campaign_eligible(self.record))
        self.assertTrue(campaign_eligible(self.record, campaign_enabled=True))
        self.record.update(suppressed=True, stage='suppressed')
        self.assertFalse(campaign_eligible(self.record, campaign_enabled=True))


if __name__ == '__main__':
    unittest.main()
