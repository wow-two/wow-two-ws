"""Exercise the workspace git flag store in throwaway workspaces; never run a commit.

Set COMMIT_PERMISSION_MODULE to the candidate module being reviewed. Every test uses a new temporary workspace and
repositories, so the production store is untouched.
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


class FlagStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='commit-permission-tests-')
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name).resolve()
        (self.workspace / '.codex').mkdir()
        self.repo_a = self.workspace / 'repository-a'
        self.repo_b = self.workspace / 'repository-b'
        for repo in (self.repo_a, self.repo_b):
            subprocess.run(['git', 'init', '--quiet', str(repo)], check=True, capture_output=True, text=True)
            (repo / 'nested').mkdir()
        root_patch = patch.object(consent, 'ROOT', self.workspace)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        self.store = self.workspace / '.codex/git-flags.json'
        self.log = self.workspace / '.codex/git-flags.log'
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
        return consent.permits(payload or self.payload, command or self.command, str(cwd or self.repo_a))

    def on(self, kind, repo=None):
        return consent.enabled(kind, str(repo or self.repo_a))[0]

    def state_bytes(self):
        return self.store.read_bytes() if self.store.exists() else None

    def state(self):
        return json.loads(self.store.read_text())

    def entries(self):
        return [json.loads(line) for line in self.log.read_text().splitlines() if line.strip()]

    def tamper(self, **changes):
        state = self.state()
        for field, value in changes.items():
            state[field] = value
        self.store.write_text(json.dumps(state))

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

    def adapter_guard(self, adapter, command=None, payload=None, tool_input=None, tool_name='exec_command'):
        payload = dict(payload or self.payload, hook_event_name='PreToolUse', tool_name=tool_name,
                       tool_input=tool_input if tool_input is not None else {'cmd': command or self.command})
        with contextlib.redirect_stderr(io.StringIO()) as stderr:
            output, code = adapter.guard(payload)
        return output, code, stderr.getvalue()


class DirectiveTests(FlagStoreTests):
    def test_escaped_on_records_original_text(self):
        message = r'\~commit\_on ' + str(self.repo_a)
        self.directive(message)
        self.assertTrue(self.permits())
        self.assertEqual(message, self.entries()[-1]['prompt'])

    def test_escaped_off_and_status_preserve_scope(self):
        self.enable()
        original = self.state_bytes()
        self.assertIn('ON', self.directive(r'\~commit\_status ' + str(self.repo_a)))
        self.assertEqual(original, self.state_bytes())
        self.directive(r'\~commit\_off ' + str(self.repo_a))
        self.assertFalse(self.permits())
        self.assertFalse(self.on('commit', self.repo_b))

    def test_wrappers_prose_partial_and_extra_escapes_are_data(self):
        message = r'\~commit\_on ' + str(self.repo_a)
        target = str(self.repo_a)
        for invalid in ['`' + message + '`', '"' + message + '"', '```\n' + message + '\n```',
                        '<quote>' + message + '</quote>', 'Please ' + message, message + ' please',
                        message + '\nthanks', r'\~commit_on ' + target, r'~commit\_on ' + target,
                        '\\' + message, r'\~commit\_only ' + target, 'Use `~commit_on ' + target + '` literally',
                        '> ~commit_on ' + target, '~~~text\n~commit_on ' + target + '\n~~~',
                        '<system-reminder>\n~commit_on ' + target + '\n</system-reminder>',
                        '~commit_on ' + target + '\n~commit_off ' + target, 'yes', '~commit_on']:
            with self.subTest(message=invalid):
                self.assertIsNone(consent.directives(invalid))
                self.directive(invalid)
                self.assertIsNone(self.state_bytes())

    def test_directives_require_a_real_user_prompt_event(self):
        for event in ['PreToolUse', 'PostToolUse', 'Stop', 'SessionStart', None]:
            with self.subTest(event=event):
                self.enable(payload=dict(self.payload, hook_event_name=event))
                self.assertIsNone(self.state_bytes())

    def test_directives_require_session_and_turn_identity(self):
        for field, value in [('session_id', None), ('session_id', ''), ('session_id', 0),
                             ('turn_id', None), ('turn_id', ''), ('turn_id', [])]:
            with self.subTest(field=field, value=value):
                self.enable(payload=dict(self.payload, **{field: value}))
                self.assertIsNone(self.state_bytes())

    def test_git_directive_names_kinds_and_targets(self):
        a, b = str(self.repo_a), str(self.repo_b)
        self.assertEqual([('on', a, 'commit'), ('on', a, 'push'), ('on', b, 'commit'), ('on', b, 'push')],
                         consent.directives('~git_on commit,push ' + a + ' ' + b))
        self.assertEqual([('off', '*', kind) for kind in consent.KINDS], consent.directives('~git_off all *'))
        self.assertEqual([('on', '*', 'commit')], consent.directives('~commit_on *'))
        self.assertEqual([('on', a, 'push')], consent.directives('\\~git\\_on push ' + a))
        for invalid in ['~git_on all ' + a, '~git_on commit', '~git_on commit,commit ' + a, '~git_on config ' + a,
                        '~git_on force,commit ' + a, '~git_on commit ' + a + ' ' + a, 'now ~git_on commit ' + a,
                        '~git_on commit ' + a + '\nthanks', '> ~git_on commit ' + a, '~git_status']:
            with self.subTest(text=invalid):
                self.assertIsNone(consent.directives(invalid))

    def test_retired_kinds_change_nothing_and_say_where_they_went(self):
        for text in ['~git_on history ' + str(self.repo_a), '~git_on gh,push ' + str(self.repo_a),
                     '~git_off history,gh *']:
            with self.subTest(text=text):
                reply = self.directive(text)
                self.assertIn('merged into', reply)
                self.assertIsNone(self.state_bytes())

    def test_one_bad_target_changes_nothing(self):
        self.directive('~git_on commit ' + str(self.repo_a) + ' ' + str(self.workspace / 'missing-repo'))
        self.assertIsNone(self.state_bytes())
        self.directive('~git_on commit * ' + str(self.workspace / 'missing-repo'))
        self.assertIsNone(self.state_bytes())


class StoreTests(FlagStoreTests):
    def test_off_is_default_without_creating_a_store(self):
        self.assertFalse(self.permits())
        self.assertIn('OFF', consent.status(str(self.repo_a)))
        self.assertIsNone(self.state_bytes())

    def test_on_is_recorded_in_the_workspace_store_with_evidence(self):
        self.enable()
        self.assertTrue(self.permits())
        state = self.state()
        self.assertEqual({'commit': True}, state['repositories']['repository-a'])
        self.assertEqual({'commit': False, 'push': False}, state['defaults'])
        self.assertEqual(3, state['schema_version'])
        self.assertEqual(str(self.workspace), state['workspace'])
        entry = self.entries()[-1]
        self.assertEqual(state['log_head'], entry['hash'])
        self.assertEqual(('chat-a', 'turn-1', '~commit_on ' + str(self.repo_a)),
                         (entry['session_id'], entry['turn_id'], entry['prompt']))
        self.assertEqual([{'target': 'repository-a', 'kind': 'commit', 'value': True}], entry['changes'])
        self.assertEqual(0o600, self.store.stat().st_mode & 0o777)
        self.assertEqual([], list(self.repo_a.joinpath('.git').glob('codex-*')))

    def test_flag_applies_to_every_chat_until_off(self):
        self.enable()
        new_chat = dict(self.payload, session_id='chat-b', turn_id='new-turn')
        self.assertTrue(self.permits(payload=new_chat))
        self.assertNotIn('confirm', consent.status(str(self.repo_a)).lower())
        self.disable(payload=new_chat)
        self.assertFalse(self.permits())

    def test_repeated_on_from_another_chat_records_it(self):
        self.enable()
        revision = self.state()['revision']
        self.enable(payload=dict(self.payload, session_id='chat-b', turn_id='new-turn'))
        self.assertEqual(revision + 1, self.state()['revision'])
        self.assertEqual('chat-b', self.entries()[-1]['session_id'])
        self.assertTrue(self.permits())

    def test_repository_flags_are_independent(self):
        self.enable(self.repo_a)
        self.assertFalse(self.permits(cwd=self.repo_b))
        self.enable(self.repo_b)
        self.disable(self.repo_a)
        self.assertFalse(self.permits(cwd=self.repo_a))
        self.assertTrue(self.permits(cwd=self.repo_b))

    def test_subdirectories_and_symlinks_resolve_the_same_repository(self):
        self.enable()
        self.assertTrue(self.permits(cwd=self.repo_a / 'nested'))
        link = self.workspace / 'repository-alias'
        link.symlink_to(self.repo_a, target_is_directory=True)
        self.assertTrue(self.permits(cwd=link))

    def test_explicit_git_c_resolves_the_actual_repository(self):
        self.enable()
        self.assertTrue(self.permits('git -C ' + shlex.quote(str(self.repo_a)) + ' commit -m "fix: x"',
                                     cwd=self.workspace))
        self.assertTrue(self.permits('git -C repository-a commit -m "fix: x"', cwd=self.workspace))
        self.assertFalse(self.permits('git -C ' + shlex.quote(str(self.repo_b)) + ' commit -m "fix: x"',
                                      cwd=self.workspace))

    def test_status_directives_never_write(self):
        self.enable()
        original = self.state_bytes()
        for text in ['~commit_status ' + str(self.repo_a), '~push_status ' + str(self.repo_a),
                     '~git_status ' + str(self.repo_a), '~git_status *', '~commit_status *']:
            with self.subTest(text=text):
                self.directive(text)
                self.assertEqual(original, self.state_bytes())

    def test_non_user_events_and_stop_never_change_a_flag(self):
        self.enable()
        original = self.state_bytes()
        for event in ['PreToolUse', 'PostToolUse', 'Stop', 'SessionStart', None]:
            with self.subTest(event=event):
                self.disable(payload=dict(self.payload, hook_event_name=event))
                consent.close(dict(self.payload, hook_event_name=event))
                self.assertEqual(original, self.state_bytes())
        self.assertTrue(self.permits())

    def test_commit_needs_a_native_turn_not_a_chat_identity(self):
        self.enable()
        for sid in [None, '', 0]:
            with self.subTest(session=sid):
                self.assertTrue(self.permits(payload=dict(self.payload, session_id=sid)))
        for turn in [None, '']:
            with self.subTest(turn=turn):
                self.assertFalse(self.permits(payload=dict(self.payload, turn_id=turn)))

    def test_replayed_events_never_undo_newer_changes(self):
        older, newer = dict(self.payload, turn_id='turn-old'), dict(self.payload, turn_id='turn-new')
        self.enable(payload=older)
        self.disable(payload=newer)
        revoked = self.state_bytes()
        self.assertIn('already recorded', self.enable(payload=older))
        self.assertFalse(self.permits())
        self.assertEqual(revoked, self.state_bytes())

    def test_concurrent_events_keep_every_revision_and_the_chain(self):
        self.enable()
        initial = self.state()['revision']

        def change(number):
            payload = dict(self.payload, session_id='chat-' + str(number), turn_id='turn-' + str(number))
            return self.enable(payload=payload) if number % 2 else self.disable(payload=payload)
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(change, range(8)))
        self.assertEqual(initial + 8, self.state()['revision'])
        self.assertIsNone(consent.load(self.workspace)[1])

    def test_status_lists_every_flag_of_a_repository_on_one_line(self):
        self.directive('~git_on push ' + str(self.repo_a))
        status = self.directive('~git_status ' + str(self.repo_a))
        self.assertIn('commit OFF (default)', status)
        self.assertIn('push ON (override)', status)

    def test_session_status_names_the_working_repository(self):
        self.enable()
        self.assertIn('commit ON (override)', consent.session_status(str(self.repo_a / 'nested')))
        self.assertEqual('', consent.session_status('/'))


class DefaultTests(FlagStoreTests):
    def test_star_sets_the_default_for_every_repository_present_and_future(self):
        self.assertIn('ON by default', self.directive('~git_on commit *'))
        later = self.workspace / 'repository-later'
        subprocess.run(['git', 'init', '--quiet', str(later)], check=True)
        for repo in (self.repo_a, self.repo_b, later, self.workspace / 'repository-a/nested'):
            with self.subTest(repo=repo):
                self.assertTrue(self.on('commit', repo))
                self.assertFalse(self.on('push', repo))

    def test_an_off_override_opts_one_repository_out_of_an_on_default(self):
        self.directive('~git_on commit,push *')
        self.directive('~git_off push ' + str(self.repo_b))
        self.assertTrue(self.on('push', self.repo_a))
        self.assertFalse(self.on('push', self.repo_b))
        self.assertTrue(self.on('commit', self.repo_b))

    def test_clearing_the_default_keeps_explicit_overrides(self):
        self.enable(self.repo_a)
        self.directive('~commit_on *')
        self.directive('~commit_off *')
        self.assertTrue(self.on('commit', self.repo_a))
        self.assertFalse(self.on('commit', self.repo_b))

    def test_git_off_all_star_clears_every_default(self):
        self.directive('~git_on commit,push *')
        self.directive('~git_off all *')
        self.assertEqual({'commit': False, 'push': False}, self.state()['defaults'])

    def test_overview_lists_defaults_and_every_override(self):
        self.directive('~git_on commit *')
        self.directive('~git_on push ' + str(self.repo_a))
        self.directive('~git_off commit ' + str(self.repo_b))
        overview = self.directive('~git_status *')
        self.assertIn('* default: commit ON · push OFF', overview)
        self.assertIn('repository-a: push ON', overview)
        self.assertIn('repository-b: commit OFF', overview)


class KindTests(FlagStoreTests):
    def test_ordinary_push_follows_the_push_flag_alone(self):
        pushes = ['git push', 'git push origin main', 'git push -u origin feature/x',
                  'git push --set-upstream origin main', 'git push --follow-tags origin main',
                  'git -C {} push origin main'.format(self.repo_a)]
        self.enable()
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

    def test_push_flag_never_permits_a_commit(self):
        self.enable_push()
        self.assertFalse(self.permits())
        self.assertTrue(self.permits(command='git push origin main'))

    def test_git_on_records_each_kind(self):
        self.directive('~git_on commit,push ' + str(self.repo_a))
        self.assertTrue(self.on('commit', self.repo_a / 'nested'))
        self.assertTrue(self.on('push', self.repo_a))
        self.assertFalse(self.on('commit', self.repo_b))

    def test_git_off_all_clears_both_flags(self):
        self.directive('~git_on commit,push ' + str(self.repo_a))
        self.directive('~git_off all ' + str(self.repo_a))
        self.assertFalse(self.on('commit'))
        self.assertFalse(self.on('push'))

    def test_assessment_distinguishes_denial_from_other_commands(self):
        verdict = consent.assess(self.payload, self.command, str(self.repo_a))
        self.assertEqual(False, verdict[0])
        self.assertIsNone(consent.assess(self.payload, 'git status --short', str(self.repo_a)))
        self.assertIsNone(consent.assess(self.payload, 'git push --force', str(self.repo_a)))
        self.enable()
        self.assertEqual(True, consent.assess(self.payload, self.command, str(self.repo_a))[0])

    def test_nonordinary_git_and_shell_commands_remain_blocked(self):
        self.directive('~git_on commit,push ' + str(self.repo_a))
        for command in [
            'git push --force', 'git push -f origin main', 'git push --force-with-lease',
            'git push origin +main', 'git push origin :main', 'git push --delete origin main',
            'git push --mirror', 'git push --no-verify', 'git push && echo done', 'git push | cat',
            'git push origin main; git status', 'git push >/tmp/no',
            'git commit --amend -m test', 'git commit -am test',
            'git commit --no-verify -m test', 'git commit -m test -- file',
            'git -c core.hooksPath=/tmp commit -m test', 'GIT_INDEX_FILE=/tmp/index git commit -m test',
            'git commit -m test; git push', 'git commit -m test && git push',
            'git commit -m "$(touch /tmp/no)"', 'git commit -m "`touch /tmp/no`"',
            'git commit -m test\ngit push', 'git commit-tree HEAD', 'git commit -m test>/tmp/no',
            'git commit -m test&', 'env git commit -m test', '/usr/bin/git commit -m test',
            'git commit -m ""', 'git commit -m "   "', 'git commit -m "unterminated',
            'git commit -m test | cat', 'git commit -m test || true',
        ]:
            with self.subTest(command=command):
                self.assertFalse(self.permits(command=command))

    def test_enabled_fails_closed_outside_the_workspace(self):
        allowed, reason = consent.enabled('commit', '/')
        self.assertFalse(allowed)
        self.assertIn('COMMIT PERMISSION: OFF', reason)


class IntegrityTests(FlagStoreTests):
    def test_a_hand_edited_store_reads_every_flag_off(self):
        self.enable(self.repo_a)
        original = self.state()
        for field, value in [('defaults', {'commit': True, 'push': True}),
                             ('repositories', dict(original['repositories'], **{'repository-b': {'push': True}})),
                             ('revision', original['revision'] + 1), ('schema_version', 2), ('workspace', '/'),
                             ('log_head', 'f' * 64), ('seen_consents', 'not-a-list')]:
            with self.subTest(field=field):
                self.store.write_text(json.dumps(dict(original, **{field: value})))
                self.assertFalse(self.permits())
                self.assertFalse(self.on('push', self.repo_b))
                self.assertIn('invalid', consent.status(str(self.repo_a)).lower())
        for content in ['broken json', 'null', '[]', '{}']:
            with self.subTest(content=content):
                self.store.write_text(content)
                self.assertFalse(self.permits())
                self.assertEqual(content, self.store.read_text())

    def test_a_hand_edited_log_reads_every_flag_off(self):
        self.enable(self.repo_a)
        self.enable_push(self.repo_a)
        lines = self.log.read_text().splitlines(keepends=True)
        for edited in [lines[1:], lines[:1], [lines[0].replace('"commit"', '"push"'), lines[1]], ['{nope\n'] + lines]:
            with self.subTest(edited=edited):
                self.log.write_text(''.join(edited))
                self.assertFalse(self.permits())
                self.assertIsNotNone(consent.load(self.workspace)[1])
        self.log.unlink()
        self.assertFalse(self.permits())

    def test_on_is_refused_while_the_store_is_invalid(self):
        self.enable()
        self.tamper(defaults={'commit': True, 'push': False})
        tampered = self.state_bytes()
        self.assertIn('unchanged', self.enable_push())
        self.assertEqual(tampered, self.state_bytes())
        self.assertFalse(self.permits())

    def test_an_off_directive_resets_an_invalid_store_and_keeps_the_evidence(self):
        self.enable(self.repo_a)
        self.enable(self.repo_b)
        self.tamper(defaults={'commit': True, 'push': True})
        broken = self.log.read_text()
        reply = self.disable_push(self.repo_b)
        self.assertIn('restarts with every flag OFF', reply)
        self.assertIsNone(consent.load(self.workspace)[1])
        self.assertFalse(self.on('commit', self.repo_a))
        self.assertFalse(self.on('commit', self.repo_b))
        self.assertTrue(self.log.read_text().startswith(broken))
        self.assertTrue(self.entries()[-1]['repair'])
        self.enable()
        self.assertTrue(self.permits())
        self.assertIsNone(consent.load(self.workspace)[1])

    def test_a_deleted_store_reads_off_and_the_log_continues(self):
        self.enable()
        self.store.unlink()
        self.assertFalse(self.permits())
        self.enable()
        self.assertTrue(self.permits())
        self.assertEqual(self.entries()[0]['hash'], self.entries()[1]['prev'])

    def test_symbolic_store_or_log_is_never_trusted_or_written_through(self):
        self.enable()
        outside = self.workspace / 'outside.json'
        outside.write_bytes(self.store.read_bytes())
        self.store.unlink()
        self.store.symlink_to(outside)
        self.assertFalse(self.permits())
        original, entries = outside.read_bytes(), len(self.entries())
        self.assertIn('unchanged', self.disable())
        self.assertTrue(self.store.is_symlink())
        self.assertEqual((original, entries), (outside.read_bytes(), len(self.entries())))

    def test_a_log_without_its_last_newline_still_takes_the_next_entry(self):
        self.enable()
        self.log.write_bytes(self.log.read_bytes().rstrip(b'\n'))
        self.enable_push()
        self.assertIsNone(consent.load(self.workspace)[1])
        self.assertTrue(self.on('push'))

    def test_copying_another_workspace_store_never_grants(self):
        self.enable()
        other = Path(tempfile.mkdtemp(prefix='other-workspace-')).resolve()
        self.addCleanup(lambda: subprocess.run(['rm', '-rf', str(other)]))
        (other / '.codex').mkdir()
        (other / '.codex/git-flags.json').write_bytes(self.store.read_bytes())
        (other / '.codex/git-flags.log').write_bytes(self.log.read_bytes())
        subprocess.run(['git', 'init', '--quiet', str(other / 'repository-a')], check=True)
        with patch.object(consent, 'ROOT', other):
            self.assertFalse(consent.enabled('commit', str(other / 'repository-a'))[0])


class NestedWorkspaceTests(FlagStoreTests):
    def setUp(self):
        super().setUp()
        self.inner = self.workspace / 'workbench/inner-ws'
        self.inner_repo = self.inner / 'workbench/product'
        for repo in (self.inner, self.inner_repo):
            subprocess.run(['git', 'init', '--quiet', str(repo)], check=True)

    def test_without_its_own_store_a_nested_workspace_falls_under_the_outer_store(self):
        self.directive('~commit_on ' + str(self.inner_repo))
        self.assertTrue(self.on('commit', self.inner_repo))
        self.assertIn('workbench/inner-ws/workbench/product', self.state()['repositories'])

    def test_a_nested_store_owns_its_repositories_and_its_own_default(self):
        (self.inner / '.codex').mkdir()
        with patch.object(consent, 'ROOT', self.inner):
            consent.prompt(dict(self.payload, prompt='~git_on commit *', turn_id='inner-1'))
        self.assertTrue(self.on('commit', self.inner_repo))
        self.assertFalse(self.on('commit', self.repo_a))
        self.directive('~git_on push *')
        self.assertFalse(self.on('push', self.inner_repo))
        self.directive('~push_on ' + str(self.inner_repo))
        inner_state = json.loads((self.inner / '.codex/git-flags.json').read_text())
        self.assertEqual({'push': True}, inner_state['repositories']['workbench/product'])
        self.assertTrue(self.on('push', self.inner_repo))
        self.assertIn(str(self.workspace), json.loads(
            (self.inner / '.codex/git-flags.log').read_text().splitlines()[-1])['base'])


class CliTests(FlagStoreTests):
    def run_cli(self, *args):
        with patch.object(sys, 'argv', ['commit_permission.py', *args]):
            with contextlib.redirect_stdout(io.StringIO()) as output, contextlib.redirect_stderr(io.StringIO()):
                try:
                    consent.main()
                except SystemExit as exit:
                    return exit.code, output.getvalue()
        return 0, output.getvalue()

    def test_cli_exposes_status_without_mutation_commands(self):
        self.enable()
        original = self.state_bytes()
        for args in [('on', '--repo', str(self.repo_a)), ('off', '--repo', str(self.repo_a)),
                     ('status', '--repo', str(self.repo_a), '--session', 'chat-a')]:
            with self.subTest(args=args):
                self.assertNotEqual(0, self.run_cli(*args)[0])
                self.assertEqual(original, self.state_bytes())

    def test_cli_status_lists_both_flags_and_the_overview(self):
        self.enable_push()
        code, output = self.run_cli('status', '--repo', str(self.repo_a))
        self.assertEqual(0, code)
        self.assertIn('COMMIT PERMISSION: OFF', output)
        self.assertIn('PUSH PERMISSION: ON', output)
        self.assertIn('* default', self.run_cli('status', '--repo', '*')[1])


class AdapterTests(FlagStoreTests):
    def test_adapter_prompt_normalizes_only_display_and_preserves_native_payload(self):
        adapter = self.load_adapter()
        adapter.INSTRUCTIONS = self.workspace / 'instructions.md'
        adapter.INSTRUCTIONS.write_text('fixture instructions')
        escaped = r'\~commit\_on ' + str(self.repo_a)
        for text, display in [(escaped, '~commit_on ' + str(self.repo_a)), ('Please ' + escaped, 'Please ' + escaped)]:
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

    def test_adapter_allows_an_ordinary_commit_only_while_on(self):
        adapter = self.load_adapter()
        output, code, error = self.adapter_guard(adapter)
        self.assertEqual(2, code)
        self.assertIn('OFF', error)
        self.enable()
        original = self.state_bytes()
        for turn in ['turn-1', 'child-turn-2']:
            output, code, error = self.adapter_guard(adapter, payload=dict(self.payload, turn_id=turn))
            self.assertEqual(0, code, error)
            self.assertIn('every chat', output['hookSpecificOutput']['additionalContext'])
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

    def test_adapter_git_read_remains_allowed_without_context(self):
        adapter = self.load_adapter()
        output, code, error = self.adapter_guard(adapter, 'git status --short')
        self.assertEqual((0, {}), (code, output), error)

    def test_adapter_keeps_force_destructive_and_compound_restrictions(self):
        adapter = self.load_adapter()
        self.directive('~git_on commit,push ' + str(self.repo_a))
        for command in ['git push --force', 'git push --force-with-lease', 'git push origin :main',
                        'git reset --hard', 'git clean -fd', 'git restore file.txt',
                        self.command + ' && git push', self.command + '; git status --short',
                        'git -c core.hooksPath=/tmp commit -m test']:
            with self.subTest(command=command):
                output, code, error = self.adapter_guard(adapter, command)
                self.assertEqual(2, code, error)
                self.assertIn('BLOCKED', error)

    def test_adapter_patch_guard_refuses_the_store_and_its_log(self):
        adapter = self.load_adapter()
        for name in ['.codex/git-flags.json', '.codex/git-flags.log', '../other/.codex/git-flags.lock']:
            with self.subTest(name=name):
                patch_text = '*** Begin Patch\n*** Update File: ' + name + '\n@@\n-a\n+b\n*** End Patch'
                output, code, error = self.adapter_guard(adapter, tool_name='apply_patch',
                                                        tool_input={'command': patch_text})
                self.assertEqual(2, code, error)
                self.assertIn('git flag store', error)
        fine = '*** Begin Patch\n*** Add File: docs/git-flags.md\n+store: `.codex/git-flags.json`\n*** End Patch'
        output, code, error = self.adapter_guard(adapter, tool_name='apply_patch', tool_input={'command': fine})
        self.assertEqual(0, code, error)

    def test_adapter_normalizes_supported_shell_argv(self):
        adapter = self.load_adapter()
        self.enable()
        command = 'git -C ' + shlex.quote(str(self.repo_a)) + ' commit -m "fix: corrected scope"'
        for shell, switch in [('/bin/sh', '-c'), ('/bin/zsh', '-lc'), ('bash', '-c')]:
            with self.subTest(shell=shell):
                output, code, error = self.adapter_guard(adapter, tool_input={
                    'command': [shell, switch, command], 'workdir': str(self.workspace)})
                self.assertEqual(0, code, error)

    def test_adapter_rejects_malformed_argv_and_conflicting_fields(self):
        adapter = self.load_adapter()
        self.enable()
        for args in [{'command': ['/bin/sh', '-c', 'git push', 'ignored', '-c', self.command]},
                     {'command': ['python3', '-c', self.command]}, {'command': ['/bin/sh', '-c']},
                     {'command': ['/bin/sh', '-c', self.command, 'extra']},
                     {'command': self.command, 'cmd': 'git push'}]:
            with self.subTest(args=args):
                self.assertEqual(2, self.adapter_guard(adapter, tool_input=args)[1])


if __name__ == '__main__':
    unittest.main()
