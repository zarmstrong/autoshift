import autoshift_test_env  # noqa: F401  (must stay first: isolates data dir)
import sqlite3
import unittest

import migrations


def redeemed_db(rows):
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE redeemed_keys (key_id INTEGER, platform TEXT, "
        "PRIMARY KEY (key_id, platform))"
    )
    conn.executemany("INSERT INTO redeemed_keys VALUES (?, ?)", rows)
    return conn


class RemoveMisparsedRedeemedPlatformsTest(unittest.TestCase):
    def test_removes_only_platforms_with_spaces_or_colons(self):
        conn = redeemed_db(
            [
                (1, "steam ttw:epic bl3:epic bl2:epic"),
                (2, "steam blps:epic"),
                (3, "steam bl1:steam"),
                (4, "steam"),
                (5, "epic"),
            ]
        )
        self.assertTrue(migrations.migrationFunctions[4](conn))
        rows = conn.execute(
            "SELECT key_id, platform FROM redeemed_keys ORDER BY key_id"
        ).fetchall()
        self.assertEqual(rows, [(4, "steam"), (5, "epic")])
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        self.assertEqual(version, 4)

    def test_no_op_on_clean_table(self):
        conn = redeemed_db([(1, "steam")])
        self.assertTrue(migrations.migrationFunctions[4](conn))
        rows = conn.execute("SELECT key_id, platform FROM redeemed_keys").fetchall()
        self.assertEqual(rows, [(1, "steam")])


if __name__ == "__main__":
    unittest.main()
