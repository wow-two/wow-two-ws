"""Explicit, repository-scoped commit consent for one Codex turn.

This local workflow gate never grants native sandbox or publishing permissions.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def state_path(session_id):
    if not isinstance(session_id, str) or not session_id:
        raise ValueError('missing session_id')
    key = hashlib.sha256((str(ROOT) + '\0' + session_id).encode()).hexdigest()
    return Path(tempfile.gettempdir()) / ('codex-commit-' + key + '.json')


def read_state(session_id):
    try:
        value = json.loads(state_path(session_id).read_text())
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def write_state(session_id, value):
    path = state_path(session_id)
    fd, name = tempfile.mkstemp(prefix=path.name, dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(value, stream)
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def observe(payload):
    """Only real lifecycle callers supply the current session/turn identity."""
    sid, turn = payload.get('session_id'), payload.get('turn_id')
    if not isinstance(sid, str) or not sid or not isinstance(turn, str) or not turn:
        return {}
    state = read_state(sid)
    if state.get('turn_id') != turn:
        state = {'turn_id': turn, 'repo': None, 'closed': False}
        write_state(sid, state)
    return state


def repo_root(path):
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('repository must be inside this workspace')
    result = subprocess.run(['git', '-C', str(path), 'rev-parse', '--show-toplevel'],
                            text=True, capture_output=True, timeout=5, check=True)
    root = Path(result.stdout.strip()).resolve()
    if not root.is_relative_to(ROOT):
        raise ValueError('repository must be inside this workspace')
    return str(root)


def set_permission(session_id, repo=None):
    state = read_state(session_id)
    if not state.get('turn_id') or state.get('closed'):
        raise ValueError('no live turn observed by the hook; consent remains OFF')
    state['repo'] = repo_root(repo) if repo else None
    write_state(session_id, state)
    return status(state)


def status(state):
    if state.get('repo') and not state.get('closed'):
        return ('COMMIT PERMISSION: ON for this turn only, repository ' + state['repo'] +
                '. Ordinary staged commits are permitted. Push, amend and other history changes '
                'remain forbidden. Inspect the staged paths and report each commit.')
    return 'COMMIT PERMISSION: OFF. Stage approved changes; the developer commits.'


def prompt(payload):
    state = observe(payload)
    if not state:
        return status({})
    # Exact standalone directives only; quoted text, fences and XML are data.
    text = payload.get('prompt', '')
    fence = None
    directives = []
    if isinstance(text, str):
        for line in text.splitlines():
            line = line.strip()
            match = re.match(r'^(`{3,}|~{3,})', line)
            if match:
                if fence is None:
                    fence = match[1][0]
                elif match[1][0] == fence:
                    fence = None
                continue
            if fence or '<' in text or '>' in text:
                continue
            match = re.fullmatch(r'~commit_(on|off)(?:\s+([^`]+))?', line)
            if match:
                directives.append(match.groups())
    sid = payload['session_id']
    if directives:
        # OFF wins over ON regardless of text ordering.
        if any(action == 'off' for action, _ in directives):
            state['repo'] = None
            write_state(sid, state)
        elif len(directives) == 1 and directives[0][1]:
            try:
                return set_permission(sid, ROOT / directives[0][1].strip())
            except (ValueError, OSError, subprocess.SubprocessError) as exc:
                state['repo'] = None
                write_state(sid, state)
                return status(state) + ' Cannot enable: ' + str(exc)
    return status(state)


def close(payload):
    if not payload.get('session_id') or not payload.get('turn_id'):
        return
    state = read_state(payload.get('session_id'))
    if state.get('turn_id') == payload.get('turn_id'):
        state.update(repo=None, closed=True)
        write_state(payload['session_id'], state)


def permits(payload, command, cwd):
    state = observe(payload)
    if not state.get('repo') or state.get('closed'):
        return False
    # Accept one ordinary staged commit. No wrappers, substitutions, shell
    # chains, alternate index/config, amend, implicit staging or pathspecs.
    if any(char in command for char in ('$', '`', '\n', '\r')):
        return False
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        lexer.commenters = ''
        args = list(lexer)
        if not args or args.pop(0) != 'git':
            return False
        if len(args) >= 2 and args[0] == '-C':
            cwd = str(Path(cwd) / args[1])
            args = args[2:]
        if len(args) != 3 or args[:2] != ['commit', '-m'] or not args[2].strip():
            return False
        return repo_root(cwd) == state['repo']
    except (ValueError, OSError, subprocess.SubprocessError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['on', 'off', 'status'])
    parser.add_argument('--repo')
    parser.add_argument('--session', default=os.environ.get('CODEX_THREAD_ID'))
    args = parser.parse_args()
    if args.action == 'on':
        if not args.repo:
            parser.error('on requires --repo; use only after explicit user consent')
        print(set_permission(args.session, args.repo))
    elif args.action == 'off':
        print(set_permission(args.session))
    else:
        print(status(read_state(args.session)))


if __name__ == '__main__':
    main()
