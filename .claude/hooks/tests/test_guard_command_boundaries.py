"""Synthetic hook checks; command strings never execute as Git or build commands."""
import json
from pathlib import Path
import subprocess
import unittest


GUARD = Path(__file__).resolve().parents[1] / "guard-git.py"


class CommandBoundaryTests(unittest.TestCase):
    def verdict(self, command):
        return subprocess.run(
            ["python3", str(GUARD)],
            input=json.dumps({"tool_name": "Bash", "tool_input": {"command": command}}),
            text=True, capture_output=True,
        ).returncode

    def test_read_only_config_commands_remain_independent(self):
        for separator in [";", "&&", "||", "|"]:
            command = f"git config --get commit.gpgsign {separator} git config --get gpg.program"
            with self.subTest(command=command):
                self.assertEqual(self.verdict(command), 0)

    def test_development_commands_are_not_locally_gated(self):
        for command in ["pnpm build", "pnpm test", "pnpm dev", "npm install",
                        "pnpm exec playwright test", "dotnet build", "dotnet test"]:
            with self.subTest(command=command):
                self.assertEqual(self.verdict(command), 0)

    def test_each_chained_write_retains_its_policy(self):
        for command in ["git status; git push", "git push; git status",
                        "git config --get user.name && git config user.name changed",
                        "git add -- file; git reset --hard", "git status || git clean -fd"]:
            with self.subTest(command=command):
                self.assertEqual(self.verdict(command), 2)


if __name__ == "__main__":
    unittest.main()
