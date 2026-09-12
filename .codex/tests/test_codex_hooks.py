"""Offline contract tests: hook payloads only; no Git command is executed."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = Path(os.environ.get('CODEX_HOOK_ADAPTER_PATH', ROOT / '.codex/hooks/claude_adapter.py'))


class CodexHooksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='workspace-codex-hooks-')
        self.addCleanup(self.temp.cleanup)
        self.env = dict(os.environ, TMPDIR=self.temp.name, PYTHONDONTWRITEBYTECODE='1')
        self.sid = self.id()

    def hook(self, event, **fields):
        payload = dict(hook_event_name=event, session_id=self.sid, **fields)
        result = subprocess.run(['python3', str(ADAPTER)], input=json.dumps(payload),
            capture_output=True, text=True, cwd=self.temp.name, env=self.env, timeout=20)
        return result, json.loads(result.stdout)

    def context(self, event='UserPromptSubmit', **fields):
        result, output = self.hook(event, **fields)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn('systemMessage', output)
        return output['hookSpecificOutput']['additionalContext']

    def test_start_reads_shared_instructions_without_lazy_index(self):
        text = self.context('SessionStart', source='compact')
        self.assertIn('Source: CLAUDE.md', text)
        self.assertIn('Source: .claude/rules/response-style.md', text)
        self.assertIn('Source: .codex/instructions.md', text)
        self.assertNotIn('Source: .claude/file-references.md', text)

    def test_pulse_and_full_tenth_turn_from_unrelated_directory(self):
        first = self.context(prompt='continue')
        self.assertIn('PLAN (enforce)', first)
        self.assertNotIn('STYLE RECHARGE (turn', first)
        for _ in range(9):
            tenth = self.context(prompt='continue')
        self.assertIn('STYLE RECHARGE (turn 10', tenth)
        self.assertIn('# Response Style', tenth)

    def test_markers_last_and_quoted_markers_ignored(self):
        text = self.context(prompt='Explain ~how')
        self.assertGreater(text.index('CHAT MARKERS —'), text.index('# Codex adaptations'))
        self.assertIn('`~how` — mechanism', text)
        text = self.context(prompt='```\n~bare\n```\n> ~bare\nUse `~bare` literally.')
        self.assertNotIn('CHAT MARKERS —', text)
        self.assertIn('UNKNOWN CHAT MARKER', self.context(prompt='~not_a_marker'))

    def test_stop_is_json_and_verdict_drains_once(self):
        result, output = self.hook('Stop', last_assistant_message='A short reply.\n' * 12)
        self.assertEqual(0, result.returncode)
        self.assertEqual({}, output)
        text = self.context(prompt='continue')
        self.assertIn('STYLE CHECK —', text)
        self.assertNotIn('STYLE CHECK —', self.context(prompt='continue'))

    def test_valid_plan_queue_clears_verdict(self):
        reply = ('### Plan\n\n- ✅ Audited rules\n- ✅ Ported hooks\n'
                 '- 🔄 Discuss the point\n- ⬜ Implement agreed changes\n\n'
                 '### Queue\n\n- 1 / 1 from walkthrough · open: validation\n\n'
                 'What distinguishes the two inputs?')
        self.hook('Stop', last_assistant_message=reply)
        self.assertNotIn('STYLE CHECK —', self.context(prompt='continue'))

    def test_explicit_bare_marker_does_not_report_missing_blocks(self):
        self.context(prompt='~bare answer briefly')
        self.hook('Stop', last_assistant_message='One answer.\nAnother line.\nThird line.\nFourth line.')
        self.assertNotIn('STYLE CHECK —', self.context(prompt='continue'))

    def test_missing_reply_never_reads_claude_transcript_shape(self):
        transcript = Path(self.temp.name)/'not-a-codex-transcript'
        transcript.write_text(json.dumps({'type':'assistant','message':{'content':[{'type':'text','text':'fake reply'}]}}))
        _, output = self.hook('Stop', transcript_path=str(transcript))
        self.assertIn('unavailable', output['systemMessage'])
        self.assertNotIn('STYLE CHECK —', self.context(prompt='continue'))

    def test_stop_continuation_is_not_blocked(self):
        result, output = self.hook('Stop', stop_hook_active=True, last_assistant_message='short')
        self.assertEqual((0, {}), (result.returncode, output))

    def test_session_state_is_sanitized_and_separate(self):
        self.sid = '../unsafe/~bare'
        self.assertNotIn('CHAT MARKERS —', self.context(prompt='ordinary text'))
        state = [p for p in Path(self.temp.name).iterdir()
                 if p.name.startswith(('claude-style-', 'codex-style-', 'claude-git-lane-'))]
        self.assertGreaterEqual(len(state), 2)
        self.assertTrue(all('codex-' in p.name for p in state))

    def test_git_read_and_staging_payloads_pass(self):
        for cmd in ['git status --short', 'git diff', 'git -C workbench/rma-gkb-contentloader log -1',
                    'gh pr view 123']:
            with self.subTest(cmd=cmd):
                result, _ = self.hook('PreToolUse', tool_name='Bash', tool_input={'command':cmd})
                self.assertEqual(0, result.returncode, result.stderr)

    def test_git_write_payloads_are_blocked_without_running_them(self):
        for cmd in ['git push', 'git reset --hard',
                    'git restore file.txt', 'git clean -fd',
                    'git status; git push', 'gh pr merge 123']:
            with self.subTest(cmd=cmd):
                result, _ = self.hook('PreToolUse', tool_name='Bash', tool_input={'command':cmd})
                self.assertEqual(2, result.returncode)
                self.assertIn('BLOCKED', result.stderr)

    def test_codex_exec_payload_is_normalized(self):
        result, _ = self.hook('PreToolUse', tool_name='exec_command', tool_input={'cmd':'git push'})
        self.assertEqual(2, result.returncode)

    def test_malformed_style_payload_is_advisory(self):
        result = subprocess.run(['python3', str(ADAPTER)], input='not JSON', text=True,
            capture_output=True, env=self.env, cwd=self.temp.name)
        self.assertEqual(0, result.returncode)
        self.assertIn('systemMessage', json.loads(result.stdout))


    def test_no_eis_required_empty_queue(self):
        self.hook('Stop', last_assistant_message='Done.')
        self.assertNotIn('STYLE CHECK —', self.context(prompt='continue'))

    def test_local_branch_and_commit_policy_is_retained(self):
        for command in ['git branch codex/test', 'git commit -m test']:
            result, output = self.hook('PreToolUse', tool_name='Bash',
                                       cwd=self.temp.name, tool_input={'command': command})
            self.assertEqual(0, result.returncode, result.stderr)

    def test_successful_patch_tracks_all_paths_and_rename(self):
        patch = ('*** Begin Patch\n*** Add File: new.txt\n+new\n'
                 '*** Update File: old.txt\n*** Move to: renamed.txt\n@@\n-a\n+b\n'
                 '*** Delete File: deleted.txt\n*** End Patch')
        result, output = self.hook('PostToolUse', tool_name='apply_patch', cwd=self.temp.name,
            tool_input={'command': patch},
            tool_response='Success. Updated the following files:\nA new.txt')
        self.assertEqual((0, {}), (result.returncode, output))
        ledgers = list(Path(self.temp.name).glob('claude-git-lane-codex-*/touched'))
        self.assertEqual(1, len(ledgers))
        paths = set(ledgers[0].read_text().splitlines())
        self.assertEqual({str((Path(self.temp.name)/name).resolve()) for name in
                          ['new.txt', 'old.txt', 'renamed.txt', 'deleted.txt']}, paths)

    def test_failed_patch_does_not_claim_files(self):
        self.hook('PostToolUse', tool_name='apply_patch', cwd=self.temp.name,
            tool_input={'command':'*** Begin Patch\n*** Add File: failed.txt\n+x\n*** End Patch'},
            tool_response={'isError':True, 'output':'failed'})
        self.assertEqual([], list(Path(self.temp.name).glob('claude-git-lane-*')))

    def test_unknown_patch_outcome_is_visible(self):
        _, output = self.hook('PostToolUse', tool_name='apply_patch', tool_input={'command':''})
        self.assertIn('skipped', output['systemMessage'])

    def test_guard_and_tracker_share_session_key(self):
        import importlib.util
        from unittest.mock import patch
        spec = importlib.util.spec_from_file_location('adapter_under_test', ADAPTER)
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        payload = {'session_id':self.sid, 'cwd':self.temp.name, 'tool_name':'exec_command',
                   'tool_input':{'cmd':'git status', 'workdir':self.temp.name}}
        with patch.object(adapter.subprocess, 'run') as run:
            run.return_value.returncode = 0
            adapter.guard(payload)
            forwarded = json.loads(run.call_args.kwargs['input'])
        self.assertEqual(adapter.session_key(payload), forwarded['session_id'])
        self.assertEqual(self.temp.name, forwarded['cwd'])

    def test_scoped_rules_are_deferred(self):
        text = self.context('SessionStart')
        for path in (ROOT/'.claude/rules').rglob('*.md'):
            content = path.read_text()
            if content.startswith('---\n') and 'paths:' in content.split('---', 2)[1]:
                self.assertNotIn('Source: ' + str(path.relative_to(ROOT)), text)
                self.assertIn(str(path.relative_to(ROOT)), text)


if __name__ == '__main__':
    unittest.main()
