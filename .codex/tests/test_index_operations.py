"""Index-operation policy tests; hook payloads never execute Git writes."""
import json
from pathlib import Path
import subprocess
import unittest
ROOT = Path(__file__).resolve().parents[2]
class IndexOperationTests(unittest.TestCase):
    def invoke(self, command, tool='exec_command', escalation=None):
        args = {'command' if tool == 'Bash' else 'cmd': command}
        if escalation is not None:
            args['sandbox_permissions'] = escalation
        payload = {'hook_event_name': 'PreToolUse', 'session_id': 'offline-index-test',
                   'cwd': str(ROOT), 'tool_name': tool, 'tool_input': args}
        return subprocess.run(['python3', str(ROOT / '.codex/hooks/claude_adapter.py')],
                              input=json.dumps(payload), capture_output=True, text=True)
    def test_index_operations_pass_without_escalation_metadata(self):
        commands = ['git add -- f', 'git -C /repo add -A', '/usr/bin/git add .',
                    'git restore --staged -- f', 'git restore -S -- f',
                    'git restore --staged -- -W', 'git reset HEAD -- f',
                    'git reset -- f', 'git apply --cached p', 'git rm --cached -- f']
        for tool in ['Bash', 'exec_command', 'shell_command', 'shell']:
            for cmd in commands:
                with self.subTest(tool=tool, cmd=cmd):
                    result = self.invoke(cmd, tool)
                    self.assertEqual(0, result.returncode, result.stderr)
    def test_runtime_escalation_metadata_does_not_change_local_verdict(self):
        for escalation in [None, 'use_default', 'require_escalated']:
            self.assertEqual(0, self.invoke('git add -- f', escalation=escalation).returncode)
    def test_worktree_and_publishing_restrictions_remain(self):
        for cmd in ['git restore f', 'git restore --staged --worktree f',
                    'git restore --staged -SW f', 'git reset --hard',
                    'git reset --hard HEAD -- f', 'git clean -fd', 'git push',
                    'git apply p', 'git apply --index p', 'git rm f',
                    'git add f; git push', 'gh pr merge 1']:
            with self.subTest(cmd=cmd):
                self.assertEqual(2, self.invoke(cmd).returncode)
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
