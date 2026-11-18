import os
import unittest
from unittest import mock

os.environ["AUTOSHIFT_PROFILE"] = "test_redeem_status"

import shift  # noqa: E402

BASE = shift.base_url
LOGIN_URL = (
    f"{BASE}/home?redirect_to=https%3A%2F%2Fshift.gearboxsoftware.com"
    "%2Fcode_redemptions%2Fnew"
)
NEW_PAGE = '<html><head><meta name="csrf-token" content="tok" /></head></html>'
EXPIRED_TEXT = "This SHiFT code has expired"


def response(url, text="", status=200):
    r = mock.Mock(spec=shift.requests.Response)
    r.url = url
    r.text = text
    r.status_code = status
    r.reason = "OK"
    r.request = mock.Mock(method="GET")
    return r


def make_client(user="user@example.invalid", pw="secret"):
    with mock.patch.object(
        shift.ShiftClient, "_ShiftClient__load_cookie", return_value=True
    ):
        return shift.ShiftClient(user, pw)


class IsLoginPageTest(unittest.TestCase):
    def test_detects_sign_in_redirect(self):
        self.assertTrue(shift.is_login_page(response(LOGIN_URL)))

    def test_ignores_authenticated_pages(self):
        self.assertFalse(
            shift.is_login_page(response(f"{BASE}/code_redemptions/new", NEW_PAGE))
        )
        self.assertFalse(shift.is_login_page(response(f"{BASE}/home")))


class SessionExpiryTest(unittest.TestCase):
    def test_logged_out_session_is_not_reported_as_expired_code(self):
        client = make_client(user=None, pw=None)
        client.client.get = mock.Mock(return_value=response(LOGIN_URL))
        status = client.redeem("X", "Borderlands 4", "steam")
        self.assertEqual(status, shift.Status.LOGGEDOUT)
        self.assertNotEqual(status, shift.Status.EXPIRED)

    def test_relogs_in_once_and_retries(self):
        client = make_client()
        client.client.get = mock.Mock(
            side_effect=[
                response(LOGIN_URL),  # stale session bounced to sign-in
                response(f"{BASE}/code_redemptions/new", NEW_PAGE),
                response(f"{BASE}/entitlement_offer_codes?code=X", EXPIRED_TEXT),
            ]
        )
        with mock.patch.object(
            client, "_ShiftClient__login"
        ) as login, mock.patch.object(
            client, "_ShiftClient__save_cookie", return_value=True
        ):
            status = client.redeem("X", "Borderlands 4", "steam")
        login.assert_called_once_with("user@example.invalid", "secret")
        self.assertEqual(status, shift.Status.EXPIRED)

    def test_gives_up_when_relogin_fails(self):
        client = make_client()
        client.client.get = mock.Mock(return_value=response(LOGIN_URL))
        with mock.patch.object(client, "_ShiftClient__login"), mock.patch.object(
            client, "_ShiftClient__save_cookie", return_value=False
        ):
            status = client.redeem("X", "Borderlands 4", "steam")
        self.assertEqual(status, shift.Status.LOGGEDOUT)


class LookupStatusMappingTest(unittest.TestCase):
    def lookup(self, status_code, text):
        client = make_client()
        client.client.get = mock.Mock(
            side_effect=[
                response(f"{BASE}/code_redemptions/new", NEW_PAGE),
                response(
                    f"{BASE}/entitlement_offer_codes?code=X", text, status_code
                ),
            ]
        )
        return client.redeem("X", "Borderlands 4", "steam")

    def test_server_error_is_not_reported_as_invalid(self):
        status = self.lookup(502, "Bad Gateway")
        self.assertEqual(status, shift.Status.SERVERERROR)
        self.assertNotEqual(status, shift.Status.INVALID)

    def test_unknown_code_is_invalid(self):
        status = self.lookup(200, "This SHiFT code does not exist")
        self.assertEqual(status, shift.Status.INVALID)

    def test_expired_code_is_expired(self):
        self.assertEqual(self.lookup(200, EXPIRED_TEXT), shift.Status.EXPIRED)


class MarkRedeemedTest(unittest.TestCase):
    """auto.redeem must only mark a key as done for final answers about the code."""

    def run_redeem(self, status):
        import auto
        import query

        key = query.Key(
            id=1, reward="5 Golden Keys", code="X", game="bl4", platform="steam"
        )
        client = mock.Mock()
        client.redeem.return_value = status
        with mock.patch.object(auto, "client", client), mock.patch.object(
            query.db, "set_redeemed"
        ) as set_redeemed:
            auto.redeem(key)
        return set_redeemed.called

    def test_transient_failures_are_not_marked(self):
        for status in (
            shift.Status.SERVERERROR,
            shift.Status.LOGGEDOUT,
            shift.Status.SLOWDOWN,
            shift.Status.UNKNOWN,
        ):
            with self.subTest(status=status.name):
                self.assertFalse(self.run_redeem(status))

    def test_final_answers_are_marked(self):
        for status in (
            shift.Status.SUCCESS,
            shift.Status.REDEEMED,
            shift.Status.EXPIRED,
            shift.Status.INVALID,
        ):
            with self.subTest(status=status.name):
                self.assertTrue(self.run_redeem(status))


if __name__ == "__main__":
    unittest.main()
