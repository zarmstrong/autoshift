import autoshift_test_env  # noqa: F401  (must stay first: isolates data dir)
import unittest
from unittest import mock

import shift


class ShiftClientUserAgentTest(unittest.TestCase):
    def test_session_does_not_send_python_requests_user_agent(self):
        with mock.patch.object(
            shift.ShiftClient, "_ShiftClient__load_cookie", return_value=True
        ):
            client = shift.ShiftClient()
        user_agent = client.client.headers["User-Agent"]
        self.assertEqual(user_agent, shift.USER_AGENT)
        self.assertNotIn("python-requests", user_agent)
