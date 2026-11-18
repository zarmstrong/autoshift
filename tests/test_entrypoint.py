import os
import stat
import subprocess
import tempfile
import unittest

import auto

ENTRYPOINT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "docker-entrypoint.sh",
)
IMAGE_REDEEM = (
    "bl4:steam ttw:epic bl3:epic bl2:epic,steam blps:epic,steam bl1:steam"
)


def entrypoint_args(**env):
    """Run docker-entrypoint.sh with a fake python and return its argv."""
    with tempfile.TemporaryDirectory() as tmp:
        fake = os.path.join(tmp, "python")
        with open(fake, "w") as f:
            f.write('#!/bin/sh\nprintf "%s\\0" "$@"\n')
        os.chmod(fake, os.stat(fake).st_mode | stat.S_IEXEC)
        run_env = {"PATH": tmp + os.pathsep + os.environ["PATH"]}
        run_env.update(env)
        out = subprocess.run(
            ["sh", ENTRYPOINT], env=run_env, capture_output=True, check=True
        ).stdout.decode()
    args = out.split("\0")[:-1]
    assert args[0] == "./autoshift/auto.py"
    return args[1:]


def redeem_mapping(args):
    return auto.parse_redeem_mapping(auto.setup_argparser().parse_args(args))


class EntrypointTest(unittest.TestCase):
    def test_image_default_redeem_maps_every_game(self):
        args = entrypoint_args(SHIFT_REDEEM=IMAGE_REDEEM)
        self.assertEqual(
            redeem_mapping(args),
            {
                "bl4": ["steam"],
                "ttw": ["epic"],
                "bl3": ["epic"],
                "bl2": ["epic", "steam"],
                "blps": ["epic", "steam"],
                "bl1": ["steam"],
            },
        )

    def test_legacy_games_and_platforms_are_split(self):
        args = entrypoint_args(
            SHIFT_REDEEM="",
            SHIFT_GAMES="bl4 bl3",
            SHIFT_PLATFORMS="epic steam",
        )
        parsed = auto.setup_argparser().parse_args(args)
        self.assertEqual(parsed.games, ["bl4", "bl3"])
        self.assertEqual(parsed.platforms, ["epic", "steam"])

    def test_shift_args_still_appended(self):
        args = entrypoint_args(
            SHIFT_REDEEM="bl3:steam", SHIFT_ARGS="--schedule"
        )
        self.assertEqual(args[-3:], ["--redeem", "bl3:steam", "--schedule"])

    def test_credentials_with_spaces_stay_one_argument(self):
        args = entrypoint_args(
            SHIFT_REDEEM="bl3:steam",
            SHIFT_USER="user name",
            SHIFT_PASS="pass word",
        )
        self.assertEqual(
            args[:4], ["--user", "user name", "--pass", "pass word"]
        )


if __name__ == "__main__":
    unittest.main()
