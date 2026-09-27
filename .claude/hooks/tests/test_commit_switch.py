"""Claude Code side of the repository commit switch, run against a throwaway workspace; nothing commits.

The hooks are copied into a temporary `<workspace>/.claude/hooks` + `.codex/hooks` layout, so the switch
module resolves that workspace as its root and every flag record lives in a temporary Git directory.
"""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

HOOKS = Path(__file__).resolve().parents[1]
WORKSPACE = HOOKS.parents[1]


class CommitSwitchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="claude-commit-switch-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / ".claude/hooks").mkdir(parents=True)
        (self.root / ".codex/hooks").mkdir(parents=True)
        for name in ("guard-git.py", "commit-switch.py"):
            shutil.copy(HOOKS / name, self.root / ".claude/hooks" / name)
        shutil.copy(WORKSPACE / ".codex/hooks/commit_permission.py", self.root / ".codex/hooks/commit_permission.py")
        self.repo = self.root / "workbench/product"
        subprocess.run(["git", "init", "--quiet", str(self.repo)], check=True)
        self.commit = 'git -C {} commit -m "feat: added a thing"'.format(self.repo)

    def say(self, prompt, session="chat-a"):
        payload = {"hook_event_name": "UserPromptSubmit", "session_id": session, "prompt": prompt, "cwd": str(self.root)}
        result = subprocess.run(["python3", "-B", str(self.root / ".claude/hooks/commit-switch.py")],
                                input=json.dumps(payload), capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout

    def guard(self, command, session="chat-a"):
        payload = {"tool_name": "Bash", "tool_input": {"command": command}, "session_id": session,
                   "tool_use_id": "toolu_1", "cwd": str(self.root)}
        return subprocess.run(["python3", "-B", str(self.root / ".claude/hooks/guard-git.py")],
                              input=json.dumps(payload), capture_output=True, text=True)

    def test_off_by_default_and_only_an_exact_directive_turns_it_on(self):
        self.assertEqual(2, self.guard(self.commit).returncode)
        self.assertEqual("", self.say("please ~commit_on workbench/product"))
        self.assertEqual(2, self.guard(self.commit).returncode)
        self.assertIn("ON for", self.say("~commit_on workbench/product"))
        self.assertEqual(0, self.guard(self.commit).returncode)

    def test_the_flag_applies_to_every_chat_until_off(self):
        self.say("~commit_on workbench/product")
        self.assertEqual(0, self.guard(self.commit, session="chat-b").returncode)
        self.say("~commit_off workbench/product", session="chat-b")
        self.assertEqual(2, self.guard(self.commit).returncode)

    def test_only_the_ordinary_form_passes_while_on(self):
        self.say("~commit_on workbench/product")
        for command in ["git -C {} commit -am x".format(self.repo),
                        "git -C {} commit --amend -m x".format(self.repo),
                        self.commit + " && git push",
                        "git -C {} push --force".format(self.repo),
                        "git -C {} push origin +main".format(self.repo),
                        "git -C {} push --delete origin main".format(self.repo),
                        "git -C {} push origin main && echo done".format(self.repo)]:
            with self.subTest(command=command):
                self.assertEqual(2, self.guard(command).returncode)

    def test_an_ordinary_push_follows_the_push_flag(self):
        push = "git -C {} push origin main".format(self.repo)
        self.say("~commit_on workbench/product")
        blocked = self.guard(push)
        self.assertEqual(2, blocked.returncode)
        self.assertIn("PUSH PERMISSION: OFF", blocked.stderr)
        self.assertIn("PUSH PERMISSION: ON", self.say("~push_on workbench/product"))
        self.assertEqual(0, self.guard(push).returncode)
        upstream = "git -C {} push -u origin feature/x".format(self.repo)
        self.assertEqual(0, self.guard(upstream, session="chat-b").returncode)
        self.say("~push_off workbench/product", session="chat-b")
        self.assertEqual(2, self.guard(push).returncode)
        self.assertEqual(0, self.guard(self.commit).returncode)

    def test_the_push_flag_never_permits_a_commit(self):
        self.say("~push_on workbench/product")
        self.assertEqual(2, self.guard(self.commit).returncode)
        self.assertEqual(0, self.guard("git -C {} push".format(self.repo)).returncode)

    def test_session_start_surfaces_each_on_flag(self):
        self.say("~push_on workbench/product")
        payload = {"hook_event_name": "SessionStart", "session_id": "chat-c", "cwd": str(self.repo)}
        result = subprocess.run(["python3", "-B", str(self.root / ".claude/hooks/commit-switch.py")],
                                input=json.dumps(payload), capture_output=True, text=True)
        self.assertIn("PUSH PERMISSION: ON", result.stdout)
        self.assertNotIn("COMMIT PERMISSION", result.stdout)

    def test_off_revokes_and_status_changes_nothing(self):
        self.say("~commit_on workbench/product")
        self.assertIn("ON for", self.say("~commit_status workbench/product"))
        self.say("~commit_off workbench/product")
        self.assertEqual(2, self.guard(self.commit).returncode)

    def test_a_broken_switch_never_permits_a_commit(self):
        self.say("~commit_on workbench/product")
        (self.root / ".codex/hooks/commit_permission.py").write_text("def broken(:\n")
        result = self.guard(self.commit)
        self.assertEqual(2, result.returncode)
        self.assertIn("commit switch failed", result.stderr)
        self.assertEqual(0, self.guard("git status").returncode)


if __name__ == "__main__":
    unittest.main()
