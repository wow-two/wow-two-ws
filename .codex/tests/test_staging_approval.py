"""Staging approval contracts; never executes a Git write."""
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
ROOT = Path(__file__).resolve().parents[2]
class StagingApprovalTests(unittest.TestCase):
    def invoke(self, command, escalation=False):
        args = {'cmd': command}
        if escalation:
            args['sandbox_permissions'] = 'require_escalated'
        payload = {'hook_event_name': 'PreToolUse', 'session_id': 'offline-staging-test',
                   'cwd': str(ROOT), 'tool_name': 'exec_command', 'tool_input': args}
        return subprocess.run(['python3', str(ROOT / '.codex/hooks/claude_adapter.py')],
                              input=json.dumps(payload), capture_output=True, text=True)
    def test_unapproved_index_writes_block(self):
        for cmd in ['git add -- f', 'git -C /repo add -A', '/usr/bin/git add .',
                    'git status; git add f', 'bash -lc "git add f"',
                    'git update-index --add f', 'git read-tree HEAD',
                    'git apply --cached p', 'git restore --staged f',
                    'git commit -am message', 'git rm f', 'git mv a b']:
            with self.subTest(cmd=cmd):
                result = self.invoke(cmd)
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn('STAGING BLOCKED', result.stderr)
    def test_native_approval_request_is_not_blocked_by_staging_gate(self):
        result = self.invoke('git add -- f', True)
        self.assertEqual(0, result.returncode, result.stderr)
    def test_read_only_passes(self):
        for cmd in ['git status --short', 'git diff --cached', 'git log -1', 'echo git add f', 'codex execpolicy check --rules staging.rules -- git add f']:
            self.assertEqual(0, self.invoke(cmd).returncode)
    def test_loader_includes_shared_style_and_local_rules(self):
        result = subprocess.run(['python3', str(ROOT / '.codex/hooks/claude_adapter.py')],
            input=json.dumps({'hook_event_name':'SessionStart','cwd':str(ROOT)}),
            capture_output=True,text=True,check=True)
        text = json.loads(result.stdout)['hookSpecificOutput']['additionalContext']
        self.assertIn('Source: /Users/max/.codex/conventions/response-style.md', text)
        self.assertIn('Source: .claude/rules/response-style.md', text)
        self.assertNotIn('Source: .claude/rules/templates/', text)
if __name__ == '__main__':
    unittest.main()
