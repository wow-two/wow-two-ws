"""Persistent repository flags, one for ordinary commits and one for ordinary pushes.

Only exact user hook directives change them: `~commit_on|off|status <repo>` and `~push_on|off|status <repo>`.
Each flag is the final state for every chat; this workflow guard grants no native execution permission.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
# v2 drops `confirmed_session_id`: the flag alone decides, and the chat that set it lives only in `last_change`.
SCHEMA_VERSION = 2
SCHEMA_VERSIONS = {1, 2}
# Event fingerprints kept for replay protection; older ones fall off.
SEEN_LIMIT = 50
# Two independent flags, each in its own record beside the repository's Git data.
KINDS = ('commit', 'push')
DIRECTIVE = re.compile(r'~(commit|push)_(on|off|status)')


def repository(path):
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('repository must be inside this workspace')
    result = subprocess.run(
        ['git', '-C', str(path), 'rev-parse', '--show-toplevel', '--absolute-git-dir'],
        text=True, capture_output=True, timeout=5, check=True)
    lines = result.stdout.strip().splitlines()
    if len(lines) != 2:
        raise ValueError('cannot resolve repository identity')
    root, git_dir = (Path(line).resolve() for line in lines)
    if not root.is_relative_to(ROOT) or not git_dir.is_relative_to(ROOT):
        raise ValueError('repository and Git directory must be inside this workspace')
    return str(root), str(git_dir)


def repo_root(path):
    return repository(path)[0]


def record_file(git_dir, kind='commit'):
    return Path(git_dir) / f'codex-{kind}-permission.json'


def state_path(repo, kind='commit'):
    return record_file(repository(repo)[1], kind)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def default_state(root, git_dir):
    return {'schema_version': SCHEMA_VERSION, 'repository': root, 'git_directory': git_dir,
            'enabled': False, 'revision': 0, 'last_change': None, 'seen_consents': []}


def consent_id(session_id, turn_id, text):
    return hashlib.sha256(json.dumps([session_id, turn_id, text]).encode()).hexdigest()


def valid_state(state, root, git_dir):
    """A readable record for this repository with a boolean flag. Who set it and why stay in `last_change` as
    evidence; they are not re-verified, so the stored flag is the final state."""
    if not isinstance(state, dict):
        return False
    seen = state.get('seen_consents', [])
    return (type(state.get('schema_version')) is int and state['schema_version'] in SCHEMA_VERSIONS
            and state.get('repository') == root and state.get('git_directory') == git_dir
            and type(state.get('enabled')) is bool
            and type(state.get('revision')) is int and state['revision'] >= 1
            and isinstance(seen, list) and all(isinstance(item, str) for item in seen))


def merged(state):
    """Folds a v1 record into v2: `confirmed_session_id` duplicated `last_change.session_id`."""
    if not state:
        return state
    state = {key: value for key, value in state.items() if key != 'confirmed_session_id'}
    state['schema_version'] = SCHEMA_VERSION
    state['seen_consents'] = list(dict.fromkeys(state.get('seen_consents', [])))[-SEEN_LIMIT:]
    return state


def read_record(root, git_dir, kind='commit'):
    path = record_file(git_dir, kind)
    if path.is_symlink():
        return {}
    try:
        state = json.loads(path.read_text())
    except FileNotFoundError:
        return default_state(root, git_dir)
    except (OSError, ValueError):
        return {}
    return merged(state) if valid_state(state, root, git_dir) else {}


def read_state(repo, kind='commit'):
    return read_record(*repository(repo), kind)


@contextmanager
def locked(git_dir, kind='commit'):
    path = Path(git_dir) / f'codex-{kind}-permission.lock'
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def write_record(git_dir, state, kind='commit'):
    path = record_file(git_dir, kind)
    if path.is_symlink():
        raise ValueError('permission file must not be a symbolic link')
    fd, name = tempfile.mkstemp(prefix=f'.codex-{kind}-', dir=git_dir)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(state, stream, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def describe(state, repo, session_id=None, kind='commit'):
    """A flag as the user and the agent read it; `session_id` is accepted for older callers and unused."""
    if not state:
        return f'{kind.upper()} PERMISSION: OFF for {repo}; invalid state. No {kind} is permitted.'
    if not state['enabled']:
        if kind == 'push':
            return f'PUSH PERMISSION: OFF for {repo}. The developer pushes.'
        return f'COMMIT PERMISSION: OFF for {repo}. Staging remains permitted; the developer commits.'
    name = os.path.relpath(repo, ROOT) if Path(repo).is_relative_to(ROOT) else repo
    if kind == 'push':
        return (f'PUSH PERMISSION: ON for {repo}. Ordinary pushes are permitted in every chat until '
                f'`~push_off {name}`. Report each pushed branch and range. '
                'Force, delete and mirror pushes remain forbidden.')
    return (f'COMMIT PERMISSION: ON for {repo}. Ordinary staged commits are permitted in every chat until '
            f'`~commit_off {name}`. Inspect staged paths and report commits. '
            'Amend and history changes remain forbidden; pushes follow the push flag.')


def status(repo, session_id=None, kind='commit'):
    root, git_dir = repository(repo)
    return describe(read_record(root, git_dir, kind), root, session_id, kind)


def statuses(repo, session_id=None):
    """Both flags of a repository, one line each."""
    root, git_dir = repository(repo)
    return '\n'.join(describe(read_record(root, git_dir, kind), root, session_id, kind) for kind in KINDS)


def directive_text(text):
    """Decode only the supported Markdown escapes in a leading permission marker."""
    if not isinstance(text, str):
        return text
    text = text.strip()
    for kind in KINDS:
        for action in ('on', 'off', 'status'):
            escaped = '\\~' + kind + '\\_' + action
            if text.startswith(escaped) and text[len(escaped):len(escaped) + 1].isspace():
                return '~' + kind + '_' + action + text[len(escaped):]
    return text


def directive(text):
    """(action, repository, kind) for a whole-message directive; None otherwise.

    The entire user message must be one directive; examples and quoted transcripts are data."""
    text = directive_text(text)
    if not isinstance(text, str) or '\n' in text.strip() or '\r' in text.strip():
        return None
    if not re.match(DIRECTIVE.pattern + r'\s', text.strip()):
        return None
    try:
        args = shlex.split(text.strip())
    except ValueError:
        return None
    match = DIRECTIVE.fullmatch(args[0]) if len(args) == 2 else None
    if not match:
        return None
    return match.group(2), args[1], match.group(1)


def prompt(payload):
    sid = payload.get('session_id')
    parsed = directive(payload.get('prompt'))
    label = (parsed[2] if parsed else 'commit').capitalize()
    try:
        if parsed and payload.get('hook_event_name') == 'UserPromptSubmit':
            action, target, kind = parsed
            root, git_dir = repository(ROOT / target)
            if action == 'status':
                return describe(read_record(root, git_dir, kind), root, sid or '', kind)
            if not nonempty(sid) or not nonempty(payload.get('turn_id')):
                return f'{label} permission unchanged: native user event identity is missing; no grant recorded.'
            with locked(git_dir, kind):
                old = read_record(root, git_dir, kind)
                # Only an explicit OFF can repair corrupt permission data.
                if not old and action == 'on':
                    return describe({}, root, sid, kind) + ' Disable explicitly before enabling again.'
                event = consent_id(sid, payload['turn_id'], payload['prompt'])
                seen = old.get('seen_consents', [])
                if event in seen:
                    return describe(old, root, sid, kind) + ' This directive was already recorded; state unchanged.'
                state = default_state(root, git_dir)
                state.update(enabled=action == 'on', revision=old.get('revision', 0) + 1,
                             seen_consents=[*seen, event][-SEEN_LIMIT:])
                state['last_change'] = {
                    'action': action, 'session_id': sid, 'turn_id': payload['turn_id'],
                    'prompt': payload['prompt'], 'at': datetime.now(timezone.utc).isoformat(), 'base': str(ROOT)}
                write_record(git_dir, state, kind)
            return describe(state, root, sid, kind)
        return statuses(payload.get('cwd') or ROOT, sid or '')
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        return f'{label} permission unchanged; no grant recorded: ' + str(exc)


def close(payload):
    """Replies, Stop events and child lifecycles do not change repository flags."""


def words(command):
    if not isinstance(command, str) or any(char in command for char in ('$', '`', '\n', '\r')):
        return []
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    lexer.commenters = ''
    try:
        return list(lexer)
    except ValueError:
        return []


def git_command(command, cwd):
    args = words(command)
    if not args or args.pop(0) != 'git':
        return None
    if len(args) >= 2 and args[0] == '-C':
        cwd = str(Path(cwd) / args[1])
        args = args[2:]
    return cwd, args


# Push options that only add history; anything else (force, delete, mirror, prune, no-verify) stays the developer's.
PUSH_OPTIONS = {'-u', '--set-upstream', '--tags', '--follow-tags'}
SHELL_PUNCTUATION = set('();<>|&')


def ordinary_commit(args):
    return len(args) == 3 and args[:2] == ['commit', '-m'] and bool(args[2].strip())


def ordinary_push(args):
    """`push [-u] [<remote> [<refspec>...]]` alone: a forced (`+ref`) or deleting (`:ref`) refspec is not ordinary."""
    if not args or args[0] != 'push':
        return False
    for arg in args[1:]:
        if not arg or set(arg) <= SHELL_PUNCTUATION:
            return False  # a compound or redirected command is never the ordinary form
        if arg.startswith('-'):
            if arg not in PUSH_OPTIONS:
                return False
        elif arg.startswith(('+', ':')):
            return False
    return True


def assess(payload, command, cwd):
    """(allowed, reason) for an ordinary commit or push, each decided by its own repository flag; None otherwise."""
    parsed = git_command(command, cwd)
    if parsed is None:
        return None
    cwd, args = parsed
    kind = 'commit' if ordinary_commit(args) else 'push' if ordinary_push(args) else None
    if kind is None:
        return None
    action = kind.capitalize()
    try:
        root, git_dir = repository(cwd)
        state = read_record(root, git_dir, kind)
        sid = payload.get('session_id')
        allowed = bool(state) and state['enabled'] and nonempty(payload.get('turn_id'))
        reason = describe(state, root, sid or '', kind)
        if not nonempty(payload.get('turn_id')):
            reason = f'{action} blocked: missing native turn identity. Repository flag unchanged.'
        return bool(allowed), reason
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        return False, f'{action} blocked: cannot resolve repository permission: ' + str(exc)


def permits(payload, command, cwd):
    result = assess(payload, command, cwd)
    return result is not None and result[0]


def notice(payload, command, cwd):
    """Kept for callers: with each flag as the final state there is no per-chat confirmation to surface."""
    return ''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['status'])
    parser.add_argument('--repo', default='.')
    args = parser.parse_args()
    try:
        print(statuses(args.repo))
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        parser.exit(1, 'Cannot inspect repository permissions: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
