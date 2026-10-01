import os
import unittest
from unittest import mock

os.environ["AUTOSHIFT_PROFILE"] = "test_shift"

import shift  # noqa: E402


class ShiftClientUserAgentTest(unittest.TestCase):
    def test_session_does_not_send_python_requests_user_agent(self):
        with mock.patch.object(
            shift.ShiftClient, "_ShiftClient__load_cookie", return_value=True
        ):
            client = shift.ShiftClient()
        user_agent = client.client.headers["User-Agent"]
        self.assertEqual(user_agent, shift.USER_AGENT)
        self.assertNotIn("python-requests", user_agent)
