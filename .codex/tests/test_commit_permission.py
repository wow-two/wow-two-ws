"""Exercise repository consent using isolated Git metadata; never run a commit.

Set COMMIT_PERMISSION_MODULE to the candidate module being reviewed. Every test
uses new temporary repositories, so production permission records are untouched.
"""
import contextlib
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


WORKSPACE_ROOT = Path(os.environ.get('COMMIT_PERMISSION_WORKSPACE', Path(__file__).resolve().parents[2]))
DEFAULT_MODULE = WORKSPACE_ROOT / '.codex/hooks/commit_permission.py'
MODULE_PATH = Path(os.environ.get('COMMIT_PERMISSION_MODULE', DEFAULT_MODULE))
ADAPTER_PATH = Path(os.environ.get('COMMIT_PERMISSION_ADAPTER', WORKSPACE_ROOT / '.codex/hooks/claude_adapter.py'))
spec = importlib.util.spec_from_file_location('repository_commit_permission_under_test', MODULE_PATH)
consent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(consent)


class RepositoryCommitPermissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='commit-permission-tests-')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name).resolve()
        self.repo_a = self.workspace / 'repository-a'
        self.repo_b = self.workspace / 'repository-b'
        for repo in (self.repo_a, self.repo_b):
            subprocess.run(['git', 'init', '--quiet', str(repo)], check=True,
                           capture_output=True, text=True)
            (repo / 'nested').mkdir()
        root_patch = patch.object(consent, 'ROOT', self.workspace)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        self.payload = {'hook_event_name': 'UserPromptSubmit', 'session_id': 'chat-a',
                        'turn_id': 'turn-1', 'cwd': str(self.repo_a)}
        self.next_user_turn = 1
        self.command = 'git commit -m "fix: corrected repository commit permission"'

    def directive(self, text, payload=None):
        if payload is None:
            payload = dict(self.payload, turn_id='turn-' + str(self.next_user_turn))
            self.next_user_turn += 1
        return consent.prompt(dict(payload, prompt=text))

    def enable(self, repo=None, payload=None):
        return self.directive('~commit_on ' + str(repo or self.repo_a), payload)

    def disable(self, repo=None, payload=None):
        return self.directive('~commit_off ' + str(repo or self.repo_a), payload)

    def enable_push(self, repo=None, payload=None):
        return self.directive('~push_on ' + str(repo or self.repo_a), payload)

    def disable_push(self, repo=None, payload=None):
        return self.directive('~push_off ' + str(repo or self.repo_a), payload)

    def permits(self, command=None, payload=None, cwd=None):
        return consent.permits(payload or self.payload, command or self.command,
                               str(cwd or self.repo_a))

    def state_bytes(self, repo=None):
        path = Path(consent.state_path(str(repo or self.repo_a)))
        return path.read_bytes() if path.exists() else None

    def load_adapter(self):
        spec = importlib.util.spec_from_file_location('repository_commit_adapter_under_test', ADAPTER_PATH)
        adapter = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {'commit_permission': consent}):
            spec.loader.exec_module(adapter)
        adapter.commit_permission = consent
        adapter.ROOT = self.workspace
        adapter.SHARED = WORKSPACE_ROOT / '.claude/hooks'
        self.assertTrue((adapter.SHARED / 'guard-git.py').is_file())
        return adapter

    def adapter_guard(self, adapter, command=None, payload=None, tool_input=None):
        payload = dict(payload or self.payload, hook_event_name='PreToolUse', tool_name='exec_command',
                       tool_input=tool_input if tool_input is not None else {'cmd': command or self.command})
        with contextlib.redirect_stderr(io.StringIO()) as stderr:
            output, code = adapter.guard(payload)
        return output, code, stderr.getvalue()


    def test_escaped_on_records_original_text_in_isolated_repository(self):
        message = r'\~commit\_on ' + str(self.repo_a)
        self.directive(message)
        self.assertTrue(self.permits())
        state = consent.read_state(str(self.repo_a))
        self.assertEqual(message, state['last_change']['prompt'])
        self.assertTrue(consent.valid_state(state, str(self.repo_a), str(self.repo_a / '.git')))

    def test_escaped_off_and_status_preserve_scope(self):
        self.enable()
        original = self.state_bytes()
        self.assertIn('ON', self.directive(r'\~commit\_status ' + str(self.repo_a)))
        self.assertEqual(original, self.state_bytes())
        self.directive(r'\~commit\_off ' + str(self.repo_a))
        self.assertFalse(self.permits())
        self.assertIsNone(self.state_bytes(self.repo_b))

    def test_escaped_on_applies_to_every_chat(self):
        self.enable()
        original = self.state_bytes()
        new_chat = dict(self.payload, session_id='chat-b', turn_id='new-turn')
        self.assertTrue(self.permits(payload=new_chat))
        self.directive(r'\~commit\_on ' + str(self.repo_a), new_chat)
        self.assertIs(consent.read_state(str(self.repo_a))['enabled'], True)
        self.assertNotEqual(original, self.state_bytes())
        self.assertTrue(self.permits(payload=new_chat))
        self.assertTrue(self.permits())

    def test_escaped_directive_rejects_wrappers_prose_partial_and_extra_escapes(self):
        message = r'\~commit\_on ' + str(self.repo_a)
        for invalid in ['`' + message + '`', '"' + message + '"', '```\n' + message + '\n```',
                        '<quote>' + message + '</quote>', 'Please ' + message,
                        message + ' please', message + '\nthanks',
                        r'\~commit_on ' + str(self.repo_a), r'~commit\_on ' + str(self.repo_a),
                        '\\' + message, r'\~commit\_only ' + str(self.repo_a)]:
            with self.subTest(message=invalid):
                self.assertIsNone(consent.directive(invalid))
                self.directive(invalid)
                self.assertIsNone(self.state_bytes())

    def test_escaped_directive_still_requires_native_user_event(self):
        message = r'\~commit\_on ' + str(self.repo_a)
        for event in ['PreToolUse', 'SessionStart', 'Stop', None]:
            self.directive(message, dict(self.payload, hook_event_name=event))
            self.assertIsNone(self.state_bytes())

    def test_escaped_old_on_cannot_replay_after_off(self):
        old = dict(self.payload, turn_id='old')
        message = r'\~commit\_on ' + str(self.repo_a)
        self.directive(message, old)
        self.disable()
        disabled = self.state_bytes()
        self.directive(message, old)
        self.assertFalse(self.permits())
        self.assertEqual(disabled, self.state_bytes())


    def test_adapter_normalizes_only_display_and_preserves_native_payload(self):
        adapter = self.load_adapter()
        adapter.INSTRUCTIONS = self.workspace / 'instructions.md'
        adapter.INSTRUCTIONS.write_text('fixture instructions')
        escaped = r'\~commit\_on ' + str(self.repo_a)
        for text, display in [(escaped, '~commit_on ' + str(self.repo_a)),
                              ('Please ' + escaped, 'Please ' + escaped),
                              ('`' + escaped + '`', '`' + escaped + '`')]:
            native_payload = dict(self.payload, prompt=text)
            with self.subTest(text=text), patch.object(adapter, 'checker') as checker, \
                    patch.object(adapter, 'run_shared') as shared, \
                    patch.object(adapter, 'routing_pulse', return_value='fixture routing'), \
                    patch.object(adapter.tempfile, 'gettempdir', return_value=str(self.workspace)), \
                    patch.object(consent, 'prompt', return_value='fixture permission') as native_prompt:
                checker.return_value.load_config.return_value = {}
                shared.return_value = subprocess.CompletedProcess([], 0, '', '')
                adapter.prompt(native_payload)
                expanded = [call.args[1]['prompt'] for call in shared.call_args_list
                            if call.args[0] == 'expand-markers.sh']
                self.assertEqual([display], expanded)
                native_prompt.assert_called_once_with(native_payload)
                self.assertIsNone(self.state_bytes())

    def test_off_is_default_without_creating_a_record(self):
        self.assertFalse(self.permits())
        self.assertIn('OFF', consent.status(str(self.repo_a), 'chat-a'))
        self.assertIsNone(self.state_bytes())

    def test_on_is_persisted_in_the_repository_git_directory(self):
        self.enable()
        self.assertTrue(self.permits())
        path = Path(consent.state_path(str(self.repo_a)))
        self.assertEqual(self.repo_a / '.git' / 'codex-commit-permission.json', path)
        state = consent.read_state(str(self.repo_a))
        self.assertIs(state['enabled'], True)
        self.assertNotIn('confirmed_session_id', state)
        self.assertGreaterEqual(state['revision'], 1)
        self.assertEqual(2, state['schema_version'])
        self.assertEqual(str(self.repo_a), state['repository'])
        self.assertEqual(str(self.repo_a / '.git'), state['git_directory'])
        self.assertEqual('on', state['last_change']['action'])
        self.assertEqual('chat-a', state['last_change']['session_id'])
        self.assertEqual('turn-1', state['last_change']['turn_id'])
        self.assertEqual('~commit_on ' + str(self.repo_a), state['last_change']['prompt'])
        self.assertEqual(0o600, path.stat().st_mode & 0o777)

    def test_same_chat_keeps_permission_across_turns_and_stop(self):
        self.enable()
        original = self.state_bytes()
        new_turn = dict(self.payload, turn_id='turn-2')
        self.assertTrue(self.permits(payload=new_turn))
        consent.close(new_turn)
        self.assertTrue(self.permits(payload=new_turn))
        self.assertEqual(original, self.state_bytes())

    def test_child_turn_and_late_parent_events_cannot_erase_grant(self):
        self.enable()
        original = self.state_bytes()
        for turn in ['child-one', 'parent-old-turn', 'child-two', 'turn-1']:
            payload = dict(self.payload, turn_id=turn, hook_event_name='PreToolUse')
            self.assertTrue(self.permits(payload=payload))
            consent.close(payload)
        self.assertEqual(original, self.state_bytes())
        self.assertTrue(self.permits())

    def test_on_applies_to_new_chats_without_confirmation(self):
        self.enable()
        original = self.state_bytes()
        new_chat = dict(self.payload, session_id='chat-b', turn_id='new-turn')
        self.assertTrue(self.permits(payload=new_chat))
        status = consent.status(str(self.repo_a), 'chat-b')
        self.assertIn('ON', status)
        self.assertNotIn('confirm', status.lower())
        self.directive('Continue working on this repository.', new_chat)
        self.assertEqual(original, self.state_bytes())

    def test_repeated_on_from_another_chat_records_it_and_stays_on(self):
        self.enable()
        original = consent.read_state(str(self.repo_a))
        new_chat = dict(self.payload, session_id='chat-b', turn_id='new-turn')
        self.enable(payload=new_chat)
        current = consent.read_state(str(self.repo_a))
        self.assertIs(current['enabled'], True)
        self.assertEqual(original['revision'] + 1, current['revision'])
        self.assertEqual('chat-b', current['last_change']['session_id'])
        self.assertTrue(self.permits(payload=new_chat))
        self.assertTrue(self.permits())

    def test_off_persists_across_chats_without_confirmation(self):
        self.enable()
        self.disable()
        original = self.state_bytes()
        new_chat = dict(self.payload, session_id='chat-b', turn_id='new-turn')
        self.assertFalse(self.permits(payload=new_chat))
        status = consent.status(str(self.repo_a), 'chat-b')
        self.assertIn('OFF', status)
        self.assertNotIn('confirmation required', status.lower())
        self.directive('Continue working.', new_chat)
        consent.close(new_chat)
        self.assertEqual(original, self.state_bytes())

    def test_repo_flags_are_independent(self):
        self.enable(self.repo_a)
        self.assertFalse(self.permits(cwd=self.repo_b))
        self.enable(self.repo_b)
        self.assertTrue(self.permits(cwd=self.repo_a))
        self.assertTrue(self.permits(cwd=self.repo_b))
        self.disable(self.repo_a)
        self.assertFalse(self.permits(cwd=self.repo_a))
        self.assertTrue(self.permits(cwd=self.repo_b))

    def test_subdirectories_and_symlinks_resolve_the_same_repository(self):
        self.enable()
        self.assertTrue(self.permits(cwd=self.repo_a / 'nested'))
        link = self.workspace / 'repository-alias'
        link.symlink_to(self.repo_a, target_is_directory=True)
        self.assertTrue(self.permits(cwd=link))
        self.assertEqual(consent.state_path(str(self.repo_a)),
                         consent.state_path(str(self.repo_a / 'nested')))
        self.assertEqual(consent.state_path(str(self.repo_a)), consent.state_path(str(link)))

    def test_explicit_git_c_resolves_actual_repo_despite_workspace_cwd(self):
        self.enable()
        command = 'git -C ' + shlex.quote(str(self.repo_a)) + ' commit -m "fix: corrected scope"'
        self.assertTrue(self.permits(command, cwd=self.workspace))
        command = 'git -C repository-a commit -m "fix: corrected scope"'
        self.assertTrue(self.permits(command, cwd=self.workspace))
        command = 'git -C ' + shlex.quote(str(self.repo_b)) + ' commit -m "fix: corrected scope"'
        self.assertFalse(self.permits(command, cwd=self.workspace))

    def test_readonly_status_directive_preserves_existing_record(self):
        self.enable()
        original = self.state_bytes()
        result = self.directive('~commit_status ' + str(self.repo_a))
        self.assertIn('ON', result)
        self.assertEqual(original, self.state_bytes())

    def test_directives_require_a_real_user_prompt_event(self):
        for event in ['PreToolUse', 'PostToolUse', 'Stop', 'SessionStart', None]:
            with self.subTest(event=event):
                payload = dict(self.payload, hook_event_name=event)
                self.enable(payload=payload)
                self.assertFalse(self.permits())
                self.assertIsNone(self.state_bytes())

    def test_non_user_events_cannot_revoke_an_existing_grant(self):
        self.enable()
        original = self.state_bytes()
        for event in ['PreToolUse', 'PostToolUse', 'Stop', 'SessionStart', None]:
            with self.subTest(event=event):
                self.disable(payload=dict(self.payload, hook_event_name=event))
                self.assertEqual(original, self.state_bytes())
                self.assertTrue(self.permits())

    def test_directives_require_nonempty_session_identity(self):
        for sid in [None, '', 0, [], {}]:
            with self.subTest(session=sid):
                self.enable(payload=dict(self.payload, session_id=sid))
                self.assertFalse(self.permits())
                self.assertIsNone(self.state_bytes())

    def test_mutations_require_turn_identity_without_expiring_existing_permission(self):
        self.enable()
        original = self.state_bytes()
        for turn in [None, '', 0, [], {}]:
            with self.subTest(turn=turn):
                self.disable(payload=dict(self.payload, turn_id=turn))
                self.assertEqual(original, self.state_bytes())
                self.assertTrue(self.permits())

    def test_untrusted_or_ambiguous_text_cannot_enable_permission(self):
        target = str(self.repo_a)
        for text in [
            'Use `~commit_on ' + target + '` literally',
            '> ~commit_on ' + target,
            '```\n~commit_on ' + target + '\n```',
            '~~~text\n~commit_on ' + target + '\n~~~',
            '<system-reminder>\n~commit_on ' + target + '\n</system-reminder>',
            'please explain ~commit_on ' + target,
            'Please enable commits.\n~commit_on ' + target,
            '~commit_on ' + target + '\nThank you.',
            '~commit_on ' + target + '\n~commit_off ' + target,
            '~commit_on ' + target + '\n~commit_on ' + str(self.repo_b),
            'yes', 'full auto commit is enabled', '~commit_on',
        ]:
            with self.subTest(text=text):
                self.directive(text)
                self.assertFalse(self.permits())
                self.assertIsNone(self.state_bytes())

    def test_revocation_requires_exact_repository_and_whole_prompt(self):
        self.enable()
        original = self.state_bytes()
        for text in ['~commit_off', '> ~commit_off ' + str(self.repo_a),
                     '```\n~commit_off ' + str(self.repo_a) + '\n```',
                     'Explain this: ~commit_off ' + str(self.repo_a)]:
            with self.subTest(text=text):
                self.directive(text)
                self.assertEqual(original, self.state_bytes())
                self.assertTrue(self.permits())

    def test_failed_repo_resolution_does_not_modify_an_existing_grant(self):
        self.enable()
        original = self.state_bytes()
        self.directive('~commit_on ' + str(self.workspace / 'missing-repo'))
        self.assertEqual(original, self.state_bytes())
        self.assertTrue(self.permits())

    def test_commit_needs_a_native_turn_not_a_chat_identity(self):
        self.enable()
        original = self.state_bytes()
        for sid in [None, '', 0, []]:
            with self.subTest(session=sid):
                self.assertTrue(self.permits(payload=dict(self.payload, session_id=sid)))
        for turn in [None, '']:
            with self.subTest(turn=turn):
                self.assertFalse(self.permits(payload=dict(self.payload, turn_id=turn)))
        self.assertEqual(original, self.state_bytes())

    def test_malformed_state_fails_closed_without_rewriting_it(self):
        self.enable()
        path = Path(consent.state_path(str(self.repo_a)))
        for content in ['broken json', 'null', '[]', 'true', '{}']:
            with self.subTest(content=content):
                path.write_text(content)
                self.assertFalse(self.permits())
                status = consent.status(str(self.repo_a), 'chat-a')
                self.assertIn('OFF', status)
                self.assertIn('invalid', status.lower())
                self.assertEqual(content, path.read_text())

    def test_invalid_schema_cannot_be_interpreted_as_enabled(self):
        self.enable()
        path = Path(consent.state_path(str(self.repo_a)))
        original = consent.read_state(str(self.repo_a))
        for field, value in [('enabled', 'true'), ('enabled', 1),
                             ('revision', -1), ('revision', 0), ('revision', True),
                             ('schema_version', True), ('schema_version', 3),
                             ('seen_consents', 'not-a-list')]:
            with self.subTest(field=field, value=value):
                invalid = dict(original, **{field: value})
                path.write_text(json.dumps(invalid))
                self.assertFalse(self.permits())

    def test_copying_another_repository_record_never_grants_permission(self):
        self.enable(self.repo_a)
        state_a = self.state_bytes(self.repo_a)
        path_b = Path(consent.state_path(str(self.repo_b)))
        path_b.write_bytes(state_a)
        self.assertFalse(self.permits(cwd=self.repo_b))
        self.assertIn('invalid', consent.status(str(self.repo_b), 'chat-a').lower())

    def test_corrupt_state_requires_explicit_off_before_reenabling(self):
        self.enable()
        path = Path(consent.state_path(str(self.repo_a)))
        path.write_text('corrupt permission state')
        self.enable()
        self.assertFalse(self.permits())
        self.assertEqual('corrupt permission state', path.read_text())
        self.disable()
        self.assertIs(consent.read_state(str(self.repo_a))['enabled'], False)
        self.enable()
        self.assertTrue(self.permits())

    def test_symbolic_permission_file_is_not_trusted_or_written_through(self):
        self.enable()
        path = Path(consent.state_path(str(self.repo_a)))
        destination = self.workspace / 'external-state.json'
        destination.write_bytes(path.read_bytes())
        original = destination.read_bytes()
        path.unlink()
        path.symlink_to(destination)
        self.assertFalse(self.permits())
        self.disable()
        self.assertEqual(original, destination.read_bytes())
        self.assertTrue(path.is_symlink())

    def test_git_reads_carry_no_permission_notice(self):
        self.enable()
        original = self.state_bytes()
        for session in ['new-chat', 'chat-a']:
            with self.subTest(session=session):
                payload = dict(self.payload, session_id=session)
                self.assertEqual('', consent.notice(payload, 'git status --short', str(self.repo_a)))
        self.assertEqual(original, self.state_bytes())

    def test_plain_commit_assessment_distinguishes_denial_from_other_commands(self):
        verdict = consent.assess(self.payload, self.command, str(self.repo_a))
        self.assertEqual(False, verdict[0])
        self.assertIn('OFF', verdict[1])
        self.assertIsNone(consent.assess(self.payload, 'git status --short', str(self.repo_a)))
        self.assertIsNone(consent.assess(self.payload, 'git push --force', str(self.repo_a)))
        self.enable()
        self.assertEqual(True, consent.assess(self.payload, self.command, str(self.repo_a))[0])

    def test_ordinary_push_follows_the_push_flag_alone(self):
        pushes = ['git push', 'git push origin main', 'git push -u origin feature/x',
                  'git push --set-upstream origin main', 'git push --follow-tags origin main',
                  'git -C {} push origin main'.format(self.repo_a)]
        self.enable()  # the commit flag never permits a push
        for command in pushes:
            with self.subTest(command=command):
                verdict = consent.assess(self.payload, command, str(self.repo_a))
                self.assertEqual(False, verdict[0])
                self.assertIn('PUSH PERMISSION: OFF', verdict[1])
        self.enable_push()
        for command in pushes:
            with self.subTest(command=command):
                self.assertTrue(self.permits(command=command))
        self.disable_push()
        self.assertFalse(self.permits(command='git push origin main'))
        self.assertTrue(self.permits())

    def test_push_flag_never_permits_a_commit_and_keeps_its_own_record(self):
        self.enable_push()
        self.assertFalse(self.permits())
        self.assertTrue(self.permits(command='git push origin main'))
        self.assertIsNone(self.state_bytes())
        push_record = json.loads(Path(consent.state_path(str(self.repo_a), 'push')).read_text())
        self.assertIs(True, push_record['enabled'])
        self.assertEqual('on', push_record['last_change']['action'])

    def test_push_flag_applies_to_every_chat_until_off(self):
        self.enable_push()
        new_chat = dict(self.payload, session_id='chat-b', turn_id='new-turn')
        self.assertTrue(self.permits(command='git push origin main', payload=new_chat))
        self.disable_push(payload=dict(new_chat, hook_event_name='UserPromptSubmit'))
        self.assertFalse(self.permits(command='git push origin main'))

    def test_push_directives_parse_escape_and_report_status(self):
        repo = str(self.repo_a)
        self.assertEqual(('on', repo, 'push'), consent.directive('~push_on ' + repo))
        self.assertEqual(('status', repo, 'push'), consent.directive('\\~push\\_status ' + repo))
        for invalid in ['~push_on', '~push_onx ' + repo, 'please ~push_on ' + repo, '~push_on a b',
                        '~pull_on ' + repo, '~push_on ' + repo + '\n~push_off ' + repo]:
            with self.subTest(invalid=invalid):
                self.assertIsNone(consent.directive(invalid))
        self.assertIn('PUSH PERMISSION: OFF', self.directive('~push_status ' + repo))
        self.assertIn('PUSH PERMISSION: ON', self.directive('\\~push\\_on ' + repo))
        self.assertIn('PUSH PERMISSION: ON', consent.status(repo, 'chat-a', 'push'))
        self.assertIn('COMMIT PERMISSION: OFF', consent.status(repo, 'chat-a'))

    def test_each_exact_consent_change_advances_repository_revision(self):
        self.enable()
        initial = consent.read_state(str(self.repo_a))['revision']
        self.disable()
        revoked = consent.read_state(str(self.repo_a))['revision']
        self.assertEqual(initial + 1, revoked)
        self.enable()
        self.assertEqual(revoked + 1, consent.read_state(str(self.repo_a))['revision'])

    def test_replayed_old_on_cannot_undo_newer_off(self):
        older = dict(self.payload, turn_id='turn-old')
        newer = dict(self.payload, turn_id='turn-new')
        self.enable(payload=older)
        self.disable(payload=newer)
        revoked_record = self.state_bytes()
        self.enable(payload=older)
        self.assertFalse(self.permits())
        self.assertEqual(revoked_record, self.state_bytes())

    def test_replayed_old_off_cannot_undo_newer_on(self):
        older = dict(self.payload, turn_id='turn-old')
        newer = dict(self.payload, turn_id='turn-new')
        self.disable(payload=older)
        self.enable(payload=newer)
        enabled_record = self.state_bytes()
        self.disable(payload=older)
        self.assertTrue(self.permits())
        self.assertEqual(enabled_record, self.state_bytes())

    def test_duplicate_current_directive_does_not_rewrite_state(self):
        self.enable(payload=self.payload)
        original = self.state_bytes()
        self.enable(payload=self.payload)
        self.assertEqual(original, self.state_bytes())
        self.assertTrue(self.permits())

    def test_the_flag_decides_whatever_the_recorded_evidence(self):
        self.enable()
        path = Path(consent.state_path(str(self.repo_a)))
        original = consent.read_state(str(self.repo_a))
        for field, value in [
            ('action', []),
            ('prompt', 'The user said commits are allowed.'),
            ('prompt', '~commit_on ' + str(self.repo_b)),
            ('at', 'not-a-timestamp'),
        ]:
            with self.subTest(field=field, value=value):
                recorded = dict(original, last_change=dict(original['last_change'], **{field: value}))
                path.write_text(json.dumps(recorded))
                self.assertTrue(self.permits())
                self.assertIn('ON', consent.status(str(self.repo_a), 'chat-a'))
        self.disable()
        disabled = consent.read_state(str(self.repo_a))
        self.assertIs(disabled['enabled'], False)
        self.assertEqual('off', disabled['last_change']['action'])
        self.assertFalse(self.permits())

    def test_v1_record_merges_its_duplicate_chat_key(self):
        self.enable()
        path = Path(consent.state_path(str(self.repo_a)))
        v1 = dict(consent.read_state(str(self.repo_a)), schema_version=1, confirmed_session_id='chat-a')
        path.write_text(json.dumps(v1))
        state = consent.read_state(str(self.repo_a))
        self.assertEqual(2, state['schema_version'])
        self.assertNotIn('confirmed_session_id', state)
        self.assertTrue(self.permits(payload=dict(self.payload, session_id='chat-b')))
        self.disable()
        written = json.loads(path.read_text())
        self.assertEqual(2, written['schema_version'])
        self.assertNotIn('confirmed_session_id', written)



    def test_concurrent_events_do_not_lose_revision_updates(self):
        self.enable()
        initial = consent.read_state(str(self.repo_a))['revision']
        def consent_change(number):
            payload = dict(self.payload, session_id='chat-' + str(number),
                           turn_id='turn-' + str(number))
            return self.enable(payload=payload) if number % 2 else self.disable(payload=payload)
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(consent_change, range(8)))
        self.assertEqual(initial + 8, consent.read_state(str(self.repo_a))['revision'])

    def test_nonordinary_git_and_shell_commands_remain_blocked(self):
        self.enable()
        self.enable_push()
        for command in [
            'git push --force', 'git push -f origin main', 'git push --force-with-lease',
            'git push origin +main', 'git push origin :main', 'git push --delete origin main',
            'git push --mirror', 'git push --no-verify', 'git push && echo done', 'git push | cat',
            'git push origin main; git status', 'git push >/tmp/no',
            'git commit --amend -m test', 'git commit -am test',
            'git commit --no-verify -m test', 'git commit -m test -- file',
            'git -c core.hooksPath=/tmp commit -m test',
            'GIT_INDEX_FILE=/tmp/index git commit -m test',
            'git commit -m test; git push', 'git commit -m test && git push',
            'git commit -m "$(touch /tmp/no)"', 'git commit -m "`touch /tmp/no`"',
            'git commit -m test\ngit push', 'git commit-tree HEAD',
            'git commit -m test>/tmp/no', 'git commit -m test&',
            'env git commit -m test', '/usr/bin/git commit -m test',
            'git commit -m ""', 'git commit -m "   "', 'git commit -m "unterminated',
            'git commit -m test | cat', 'git commit -m test || true',
        ]:
            with self.subTest(command=command):
                self.assertFalse(self.permits(command=command))

    def test_cli_exposes_status_without_mutation_commands(self):
        self.enable()
        original = self.state_bytes()
        for action in ['on', 'off']:
            with self.subTest(action=action):
                with patch.object(sys, 'argv', ['commit_permission.py', action,
                                              '--repo', str(self.repo_a)]):
                    with contextlib.redirect_stderr(io.StringIO()):
                        with self.assertRaises(SystemExit) as error:
                            consent.main()
                self.assertNotEqual(0, error.exception.code)
                self.assertEqual(original, self.state_bytes())

    def test_cli_status_reads_existing_record_without_modification(self):
        self.enable()
        original = self.state_bytes()
        with patch.object(sys, 'argv', ['commit_permission.py', 'status',
                                      '--repo', str(self.repo_a)]):
            with patch.dict(os.environ, {'CODEX_THREAD_ID': 'chat-a'}):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    consent.main()
        self.assertIn('ON', output.getvalue())
        self.assertEqual(original, self.state_bytes())

    def test_cli_session_identity_cannot_be_overridden(self):
        self.enable()
        original = self.state_bytes()
        with patch.object(sys, 'argv', ['commit_permission.py', 'status',
                                      '--repo', str(self.repo_a), '--session', 'chat-a']):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    consent.main()
        self.assertNotEqual(0, error.exception.code)
        self.assertEqual(original, self.state_bytes())

    def test_adapter_approved_parent_and_child_commits_return_context_without_state_changes(self):
        adapter = self.load_adapter()
        self.enable()
        original = self.state_bytes()
        for turn in ['turn-1', 'child-turn-2', 'parent-turn-3']:
            with self.subTest(turn=turn):
                output, code, error = self.adapter_guard(adapter, payload=dict(self.payload, turn_id=turn))
                self.assertEqual(0, code, error)
                context = output['hookSpecificOutput']
                self.assertEqual('PreToolUse', context['hookEventName'])
                self.assertIn('ON', context['additionalContext'])
                self.assertIn('every chat', context['additionalContext'])
                self.assertEqual(original, self.state_bytes())

    def test_adapter_denies_only_while_off_and_never_changes_state(self):
        adapter = self.load_adapter()
        output, code, error = self.adapter_guard(adapter)
        self.assertEqual(2, code)
        self.assertIn('OFF', error)
        self.assertIsNone(self.state_bytes())
        self.enable()
        original = self.state_bytes()
        output, code, error = self.adapter_guard(adapter, payload=dict(self.payload, session_id='new-chat'))
        self.assertEqual(0, code, error)
        self.assertIn('ON', output['hookSpecificOutput']['additionalContext'])
        self.assertEqual(original, self.state_bytes())

    def test_adapter_git_read_remains_allowed_without_permission_context(self):
        adapter = self.load_adapter()
        self.enable()
        original = self.state_bytes()
        output, code, error = self.adapter_guard(adapter, 'git status --short',
                                                payload=dict(self.payload, session_id='new-chat'))
        self.assertEqual(0, code, error)
        self.assertEqual({}, output)
        self.assertEqual(original, self.state_bytes())

    def test_adapter_on_preserves_force_push_history_destructive_and_compound_restrictions(self):
        adapter = self.load_adapter()
        self.enable()
        self.enable_push()
        original = self.state_bytes()
        for command in [
            'git push --force', 'git push --force-with-lease', 'git push origin :main',
            'git commit --amend -m test',
            'git reset --hard', 'git clean -fd', 'git restore file.txt',
            self.command + ' && git push', self.command + '; git status --short',
            'git -c core.hooksPath=/tmp commit -m test',
        ]:
            with self.subTest(command=command):
                output, code, error = self.adapter_guard(adapter, command)
                self.assertEqual(2, code, error)
                self.assertIn('BLOCKED', error)
                self.assertEqual(original, self.state_bytes())

    def test_adapter_allows_an_ordinary_push_only_while_the_push_flag_is_on(self):
        adapter = self.load_adapter()
        self.enable()
        output, code, error = self.adapter_guard(adapter, 'git push origin main')
        self.assertEqual(2, code)
        self.assertIn('PUSH PERMISSION: OFF', error)
        self.enable_push()
        output, code, error = self.adapter_guard(adapter, 'git push origin main')
        self.assertEqual(0, code, error)
        self.assertIn('PUSH PERMISSION: ON', output['hookSpecificOutput']['additionalContext'])

    def test_cli_status_lists_both_flags(self):
        self.enable_push()
        with patch.object(sys, 'argv', ['commit_permission.py', 'status', '--repo', str(self.repo_a)]):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                consent.main()
        self.assertIn('COMMIT PERMISSION: OFF', output.getvalue())
        self.assertIn('PUSH PERMISSION: ON', output.getvalue())

    def test_adapter_normalizes_supported_shell_argv_without_losing_repo_scope(self):
        adapter = self.load_adapter()
        self.enable()
        original = self.state_bytes()
        for shell, switch in [('/bin/sh', '-c'), ('/bin/zsh', '-lc'), ('bash', '-c')]:
            with self.subTest(shell=shell, switch=switch):
                command = 'git -C ' + shlex.quote(str(self.repo_a)) + ' commit -m "fix: corrected scope"'
                output, code, error = self.adapter_guard(adapter, tool_input={'command': [shell, switch, command],
                                                                             'workdir': str(self.workspace)})
                self.assertEqual(0, code, error)
                self.assertIn('ON', output['hookSpecificOutput']['additionalContext'])
                self.assertEqual(original, self.state_bytes())

    def test_adapter_rejects_malformed_shell_argv_instead_of_inspecting_the_wrong_script(self):
        adapter = self.load_adapter()
        self.enable()
        original = self.state_bytes()
        for command in [
            ['/bin/sh', '-c', 'git push', 'ignored', '-c', self.command],
            ['/bin/sh', '-c', 'git push', '-c', self.command],
            ['python3', '-c', self.command],
            [None, '-c', self.command],
            ['/bin/sh', '-c'],
            ['/bin/sh', '-c', None],
            ['/bin/sh', '--unexpected', '-c', self.command],
            ['/bin/sh', '-c', self.command, 'extra'],
        ]:
            with self.subTest(command=command):
                output, code, error = self.adapter_guard(adapter, tool_input={'command': command})
                self.assertEqual(2, code, error)
                self.assertEqual(original, self.state_bytes())

    def test_adapter_rejects_conflicting_shell_command_fields(self):
        adapter = self.load_adapter()
        self.enable()
        original = self.state_bytes()
        for args in [{'command': self.command, 'cmd': 'git push'},
                     {'command': 'git status --short', 'cmd': self.command}]:
            with self.subTest(args=args):
                output, code, error = self.adapter_guard(adapter, tool_input=args)
                self.assertEqual(2, code, error)
                self.assertEqual(original, self.state_bytes())


if __name__ == '__main__':
    unittest.main()
