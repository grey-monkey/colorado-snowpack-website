import contextlib
import io
import json
import os
import unittest
from unittest.mock import patch, MagicMock
from urllib.error import URLError
from ops.send_weekly import main


class WeeklyEntry(unittest.TestCase):
    def test_dry_run_never_contacts_backend_and_live_retains_edition(self):
        edition = {'key': 'snowpack-weekly:2026-W43', 'content': '<p>Test</p>'}
        for enabled in ('false', 'true'):
            with self.subTest(enabled=enabled), patch.dict(os.environ, {
                'WEEKLY_ENABLED': enabled, 'SIGNUP_SERVICE_URL': 'https://backend.invalid',
                'AUTOMATION_SECRET': 'fake-test-secret'
            }, clear=True), patch('ops.send_weekly.connect', return_value=MagicMock()), \
                patch('ops.send_weekly.read_release', return_value={}), \
                patch('ops.send_weekly.edition', return_value=edition), \
                patch('ops.send_weekly.urlopen') as send, contextlib.redirect_stdout(io.StringIO()):
                send.return_value.__enter__.return_value = io.StringIO(json.dumps({'status': 'sending', 'broadcast_id': 123, 'edition': edition['key']}))
                main()
                if enabled == 'false':
                    send.assert_not_called()
                else:
                    send.assert_called_once()
                    request = send.call_args.args[0]
                    self.assertEqual(request.full_url, 'https://backend.invalid/internal/weekly')
                    self.assertEqual(json.loads(request.data), edition)
                    self.assertEqual(request.get_header('Authorization'), 'Bearer fake-test-secret')
                    send.reset_mock()
                    send.side_effect = URLError('uncertain')
                    with self.assertRaisesRegex(SystemExit, 'do not blindly resend'):
                        main()
                    send.assert_called_once()
