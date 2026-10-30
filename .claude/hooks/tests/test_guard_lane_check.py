"""The lane check on `pull`: a dirty tree this session never wrote asks first, unless the pull cannot touch it."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


GUARD = Path(__file__).resolve().parents[1] / "guard-git.py"


class PullLaneCheckTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.repo = Path(self.scratch.name) / "repo"
        self.repo.mkdir()
        for args in (["init", "-q"], ["config", "user.email", "t@example.com"], ["config", "user.name", "t"]):
            subprocess.run(["git", "-C", str(self.repo)] + args, check=True)
        (self.repo / "other-lane.md").write_text("one\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "other-lane.md"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-q", "-m", "seed"], check=True)
        (self.repo / "other-lane.md").write_text("another lane's edit\n")
        self.sessions = 0

    def tearDown(self):
        self.scratch.cleanup()

    def verdict(self, command):
        self.sessions += 1  # a fresh session each time, since the check asks once per file set
        payload = {"tool_name": "Bash", "tool_input": {"command": command},
                   "session_id": "lane-test-{}".format(self.sessions), "cwd": str(self.repo)}
        env = dict(os.environ, TMPDIR=self.scratch.name)
        return subprocess.run(["python3", "-B", str(GUARD)], input=json.dumps(payload), text=True,
                              capture_output=True, env=env).returncode

    def test_fast_forward_only_pull_skips_the_check(self):
        self.assertEqual(self.verdict("git pull --ff-only"), 0)
        self.assertEqual(self.verdict("git -C {} pull --ff-only".format(self.repo)), 0)

    def test_pull_that_may_merge_or_stash_asks_first(self):
        for command in ["git pull", "git pull --rebase", "git pull --ff-only --autostash"]:
            with self.subTest(command=command):
                self.assertEqual(self.verdict(command), 2)

    def test_configured_autostash_keeps_the_check(self):
        for key in ("merge.autoStash", "rebase.autoStash"):
            with self.subTest(key=key):
                subprocess.run(["git", "-C", str(self.repo), "config", key, "true"], check=True)
                self.assertEqual(self.verdict("git pull --ff-only"), 2)
                subprocess.run(["git", "-C", str(self.repo), "config", "--unset", key], check=True)

    def test_clean_tree_pull_runs(self):
        subprocess.run(["git", "-C", str(self.repo), "checkout", "-q", "--", "other-lane.md"], check=True)
        self.assertEqual(self.verdict("git pull"), 0)


if __name__ == "__main__":
    unittest.main()
