import autoshift_test_env  # noqa: F401  (must stay first: isolates data dir)
import contextlib
import io
import unittest

import auto


def parse(*argv):
    return auto.setup_argparser().parse_args(list(argv))


class ParseRedeemMappingTest(unittest.TestCase):
    def test_maps_each_game_to_its_platforms(self):
        args = parse("--redeem", "bl3:steam,epic", "bl2:epic")
        self.assertEqual(
            auto.parse_redeem_mapping(args),
            {"bl3": ["steam", "epic"], "bl2": ["epic"]},
        )

    def test_ignores_blank_platforms_and_entries_without_colon(self):
        args = parse("--redeem", "bl3:steam,,epic ", "bl2")
        with self.assertLogs(auto._L, level="ERROR") as logs:
            mapping = auto.parse_redeem_mapping(args)
        self.assertEqual(mapping, {"bl3": ["steam", "epic"]})
        self.assertIn("Invalid --redeem entry: bl2", logs.output[0])

    def test_returns_none_without_redeem(self):
        args = parse("--games", "bl3", "--platforms", "steam")
        self.assertIsNone(auto.parse_redeem_mapping(args))


class ArgparserTest(unittest.TestCase):
    def test_legacy_games_and_platforms(self):
        args = parse("--games", "bl4", "bl3", "--platforms", "epic", "steam")
        self.assertEqual(args.games, ["bl4", "bl3"])
        self.assertEqual(args.platforms, ["epic", "steam"])

    def test_rejects_unknown_platform(self):
        stderr = io.StringIO()
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(stderr):
            parse("--games", "bl3", "--platforms", "pc")
        self.assertIn("invalid choice: 'pc'", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
