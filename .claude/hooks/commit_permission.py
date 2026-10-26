"""Workspace git flags: `commit` (everything local) and `push` (everything that reaches GitHub).

One store per workspace, `<workspace>/.claude/git-flags.json`, beside this engine: workspace defaults plus
overrides keyed by the path inside the workspace, of a repository (`workbench/org/repo`) or of a folder
(`workbench/org/*`, every repository under it, present and future). The effective flag is the repository's override,
else the longest folder override above it, else the default, kind by kind. A hash-chained change log sits beside the
store; a store that disagrees with its log reads as every flag OFF until a `_off` directive resets it. A repository's
flags live in the innermost workspace store containing it.

Only exact whole-message user directives change a flag: `~commit_on|off|status <target>`,
`~push_on|off|status <target>`, `~git_on|off <kind>[,<kind>...] <target>...` and `~git_status <target>...`, where a
target is a repository, an existing folder followed by `/*`, or `*` for the workspace default. Each flag is the final
state for every chat; this workflow guard grants no native execution permission.
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
SCHEMA_VERSION = 3
# Event fingerprints kept for replay protection; older ones fall off.
SEEN_LIMIT = 100
# `commit` covers ordinary commits and local rewrites of unpushed commits; `push` covers ordinary pushes and gh writes.
KINDS = ('commit', 'push')
# Kinds merged on 2026-09-29; a directive naming one changes nothing and says where it went.
RETIRED = {'history': 'commit', 'gh': 'push'}
DEFAULT = '*'
# A target or key ending in `/*` is a folder override: every repository under that folder, present and future.
FOLDER = '/*'
STORE = Path('.claude') / 'git-flags.json'
LOG = Path('.claude') / 'git-flags.log'
LOCK = Path('.claude') / 'git-flags.lock'
DIRECTIVE = re.compile(r'~(commit|push)_(on|off|status)')
GIT_DIRECTIVE = re.compile(r'~git_(on|off|status)')
MEANING = {
    'commit': 'Ordinary commits and local rewrites of unpushed commits (amend, rebase, cherry-pick, revert, merge, '
              'am, subtree, reset to a commit)',
    'push': 'Ordinary pushes and GitHub writes through gh (pull requests, issues, releases, workflows, secrets, '
            'repository settings)',
}
FLAG_KEYS = {'schema_version', 'workspace', 'revision', 'defaults', 'repositories', 'seen_consents', 'log_head'}


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


def store_root(root):
    """The innermost workspace at or above `root` that holds a flag store, else this workspace."""
    for directory in (Path(root), *Path(root).parents):
        if (directory / STORE).exists() or (directory / STORE).is_symlink():
            return directory
        if directory == ROOT:
            break
    return ROOT


def key(store, root):
    """A repository's key in its store: its path inside the workspace, `.` for the workspace repository."""
    return os.path.relpath(root, store)


def folder(path):
    """(store, key, folder) for a folder override: an existing directory below its workspace, keyed `<path>/*`."""
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT) or not path.is_dir():
        raise ValueError(f'folder {path} must be an existing directory inside this workspace')
    store = store_root(path)
    name = key(store, path)
    if name == '.':
        raise ValueError(f'folder {path} is the whole workspace; `*` sets the workspace default')
    return store, name + FOLDER, path


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def consent_id(session_id, turn_id, text):
    return hashlib.sha256(json.dumps([session_id, turn_id, text]).encode()).hexdigest()


def empty(store, revision=0, head=None):
    return {'schema_version': SCHEMA_VERSION, 'workspace': str(store), 'revision': revision,
            'defaults': {kind: False for kind in KINDS}, 'repositories': {}, 'seen_consents': [], 'log_head': head}


def body(state):
    """The store content its log entry vouches for: everything but the pointer to that entry."""
    return {name: value for name, value in state.items() if name != 'log_head'}


def valid_flags(flags, complete=False):
    return (isinstance(flags, dict) and all(name in KINDS and type(value) is bool for name, value in flags.items())
            and (set(flags) == set(KINDS) if complete else bool(flags)))


def valid_store(state, store):
    """A store of this workspace with boolean flags; who set them and why stay in the log as evidence."""
    if not isinstance(state, dict) or set(state) != FLAG_KEYS:
        return False
    repositories, seen = state['repositories'], state['seen_consents']
    return (type(state['schema_version']) is int and state['schema_version'] == SCHEMA_VERSION
            and state['workspace'] == str(store)
            and type(state['revision']) is int and state['revision'] >= 1
            and valid_flags(state['defaults'], complete=True)
            and isinstance(repositories, dict)
            and all(nonempty(name) and not os.path.isabs(name) and name != DEFAULT and valid_flags(flags)
                    for name, flags in repositories.items())
            and isinstance(seen, list) and all(isinstance(item, str) for item in seen)
            and isinstance(state['log_head'], str))


def log_lines(store):
    """The non-blank lines of the change log, without their newlines; missing means none."""
    path = store / LOG
    if path.is_symlink():
        raise ValueError('the change log is a symbolic link')
    try:
        return [line for line in path.read_bytes().split(b'\n') if line.strip()]
    except FileNotFoundError:
        return []


def prefix(lines):
    """The hash a repair entry commits to: every log line before it."""
    return hashlib.sha256(b''.join(line + b'\n' for line in lines)).hexdigest()


def verified_head(lines):
    """The last entry once the chain verifies from its last repair anchor, None for an empty log.

    Each entry carries the hash of the one before; a repair entry instead commits to every line before it, so the
    broken history stays as evidence while the chain restarts. Raises ValueError on any break."""
    entries = [json.loads(line) for line in lines]
    if not all(isinstance(entry, dict) for entry in entries):
        raise ValueError('a line is not an object')
    if not entries:
        return None
    start = max((index for index, entry in enumerate(entries) if entry.get('repair') is True), default=0)
    for index in range(start, len(entries)):
        entry = entries[index]
        if entry.get('hash') != digest({name: value for name, value in entry.items() if name != 'hash'}):
            raise ValueError('entry {} fails its hash'.format(index + 1))
        if index > start:
            expected = entries[index - 1]['hash']
        else:
            expected = prefix(lines[:index]) if entry.get('repair') is True else None
        if entry.get('prev') != expected:
            raise ValueError('entry {} breaks the chain'.format(index + 1))
    return entries[-1]


def load(store):
    """(state, problem): the verified store, or None with the reason it cannot be trusted (every flag reads OFF)."""
    path = store / STORE
    try:
        head = verified_head(log_lines(store))
    except (OSError, ValueError) as exc:
        return None, 'its change log is broken: {}'.format(exc)
    if path.is_symlink():
        return None, 'the store is a symbolic link'
    try:
        state = json.loads(path.read_text())
    except FileNotFoundError:
        # No store yet, or a deleted one: every flag OFF, and the next change continues the log.
        return empty(store, head['revision'] if head else 0, head['hash'] if head else None), None
    except (OSError, ValueError):
        return None, 'the store is not readable JSON'
    if not valid_store(state, store):
        return None, 'the store fails its schema'
    if head is None or head['hash'] != state['log_head'] or head.get('state') != digest(body(state)) \
            or head.get('revision') != state['revision']:
        return None, 'the store does not match its change log; it was edited outside a directive'
    return state, None


def fresh(store):
    """An all-OFF state and the repair anchor for a store that cannot be trusted."""
    lines = log_lines(store)
    revision = 0
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if isinstance(entry, dict) and type(entry.get('revision')) is int:
            revision = max(revision, entry['revision'])
    return empty(store, revision), prefix(lines)


@contextmanager
def locked(store):
    fd = os.open(store / LOCK, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def record(store, state, changes, evidence, anchor=None):
    """Appends the change to the log, then replaces the store atomically; the caller holds the lock."""
    path = store / STORE
    if path.is_symlink():
        raise ValueError('the flag store must not be a symbolic link')
    state['revision'] += 1
    entry = {'revision': state['revision'], 'at': datetime.now(timezone.utc).isoformat(), 'changes': changes,
             **evidence, 'state': digest(body(state)), 'prev': anchor if anchor is not None else state['log_head']}
    if anchor is not None:
        entry['repair'] = True
    entry['hash'] = digest(entry)
    fd = os.open(store / LOG, os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a+b') as stream:
        size, separate = stream.seek(0, os.SEEK_END), False
        if size:  # a hand edit may drop the last newline; the entry must still start its own line
            stream.seek(size - 1)
            separate = stream.read(1) != b'\n'
        stream.write((b'\n' if separate else b'') + canonical(entry).encode() + b'\n')
        stream.flush()
        os.fsync(stream.fileno())
    state['log_head'] = entry['hash']
    fd, name = tempfile.mkstemp(prefix='.git-flags-', dir=store / '.claude')
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump(state, stream, indent=2, sort_keys=True)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        Path(name).unlink(missing_ok=True)


def covering(state, name, kind):
    """The key of the longest folder override that sets `kind` above `name`, or None."""
    holders = [other for other, flags in state['repositories'].items()
               if other.endswith(FOLDER) and kind in flags and name.startswith(other[:-1])]
    return max(holders, key=len, default=None)


def effective(state, name, kind):
    """(value, source) of one flag: the repository's override, else the longest folder override above it, else the
    workspace default. A `name` ending in `/` reads a new repository directly under that folder."""
    override = state['repositories'].get(name, {})
    if kind in override:
        return override[kind], 'override'
    holder = covering(state, name, kind)
    if holder is not None:
        return state['repositories'][holder][kind], 'folder ' + holder
    return state['defaults'][kind], 'default'


def label(root):
    return os.path.relpath(root, ROOT) if Path(root).is_relative_to(ROOT) else str(root)


def describe(kind, root, value, source):
    """One flag of one repository as the user and the agent read it."""
    name = label(root)
    if not value:
        if kind == 'push':
            return f'PUSH PERMISSION: OFF for {root} ({source}). The developer pushes and writes to GitHub.'
        return (f'COMMIT PERMISSION: OFF for {root} ({source}). Staging remains permitted; '
                'the developer commits and rewrites history.')
    if kind == 'push':
        return (f'PUSH PERMISSION: ON for {root} ({source}). Ordinary pushes and gh writes are permitted in every '
                f'chat until `~push_off {name}`. Report each pushed branch and range and each GitHub write. '
                'Force, delete and mirror pushes remain forbidden.')
    return (f'COMMIT PERMISSION: ON for {root} ({source}). Ordinary commits and local rewrites of unpushed commits '
            f'are permitted in every chat until `~commit_off {name}`. Inspect staged paths and report each commit '
            'and rewrite. Pushes follow the push flag.')


def describe_default(kind, store, value):
    state = 'ON' if value else 'OFF'
    return (f'{kind.upper()} PERMISSION: {state} by default in {store}: every repository without its own override, '
            f'present and future. {MEANING[kind]}.')


def describe_folder(kind, name, value, source):
    """One flag of every repository under a folder that has no override of its own."""
    state = 'ON' if value else 'OFF'
    return (f'{kind.upper()} PERMISSION: {state} for {name} ({source}): every repository under that folder without '
            f'its own override, present and future. {MEANING[kind]}.')


def describe_planned(kind, path, value, source):
    """One flag of a repository not checked out yet, read at the path it will be cloned into."""
    if value:
        return (f'{kind.upper()} PERMISSION: ON for {path}, not checked out yet ({source}). '
                f'Report each GitHub write.')
    return (f'{kind.upper()} PERMISSION: OFF for {path}, not checked out yet ({source}). The developer runs it, or '
            f'turns the folder on with `~git_on {kind} <folder>/*`.')


def describe_invalid(kind, root, store, problem):
    return (f'{kind.upper()} PERMISSION: OFF for {root}; invalid state: {problem} ({store / STORE}). '
            f'Every flag in that store reads OFF until a `~git_off` directive resets it.')


def flags_line(state, name):
    return ' · '.join('{} {} ({})'.format(kind, 'ON' if value else 'OFF', source)
                      for kind in KINDS for value, source in [effective(state, name, kind)])


def summary(root):
    """Every effective flag of one repository on one line."""
    store = store_root(root)
    state, problem = load(store)
    if problem:
        return f'GIT FLAGS for {root}: every flag OFF; the store {store / STORE} is invalid: {problem}.'
    return f'GIT FLAGS for {root}: {flags_line(state, key(store, root))}.'


def folder_summary(store, name):
    """Every effective flag of a new repository under a folder on one line, then the overrides that win under it."""
    state, problem = load(store)
    where = '' if store == ROOT else f' in {store}'
    if problem:
        return f'GIT FLAGS for {name}{where}: every flag OFF; the store {store / STORE} is invalid: {problem}.'
    line = (f'GIT FLAGS for {name}{where} (each repository under it without its own override): '
            f'{flags_line(state, name[:-1])}.')
    inside = [other for other in sorted(state['repositories']) if other != name and other.startswith(name[:-1])]
    return line + (' Own overrides under it: ' + ', '.join(inside) + '.' if inside else '')


def folder_status(store, name, kind):
    """One flag of a folder override target."""
    state, problem = load(store)
    if problem:
        return describe_invalid(kind, name, store, problem)
    return describe_folder(kind, name, *effective(state, name[:-1], kind))


def overview(store):
    """The workspace defaults and every override, one line each."""
    state, problem = load(store)
    if problem:
        return f'GIT FLAGS in {store}: every flag OFF; the store is invalid: {problem}.'
    lines = [f'GIT FLAGS in {store} (revision {state["revision"]}):',
             '- * default: ' + ' · '.join('{} {}'.format(kind, 'ON' if state['defaults'][kind] else 'OFF')
                                          for kind in KINDS)]
    for name in sorted(state['repositories']):
        lines.append(f'- {name}: ' + ' · '.join('{} {}'.format(kind, 'ON' if value else 'OFF')
                                               for kind, value in sorted(state['repositories'][name].items())))
    return '\n'.join(lines)


def status(repo, session_id=None, kind='commit'):
    """One flag of the repository holding `repo`; `session_id` is accepted for older callers and unused."""
    root, _ = repository(repo)
    store = store_root(root)
    state, problem = load(store)
    if problem:
        return describe_invalid(kind, root, store, problem)
    return describe(kind, root, *effective(state, key(store, root), kind))


def statuses(repo, session_id=None):
    if repo.endswith(FOLDER):
        store, name, _ = folder(repo[:-len(FOLDER)])
        return '\n'.join([*(folder_status(store, name, kind) for kind in KINDS), folder_summary(store, name)])
    root, _ = repository(repo)
    return '\n'.join([*(status(root, None, kind) for kind in KINDS), summary(root)])


def session_status(cwd):
    """The working repository's effective flags for session start; empty outside this workspace's repositories."""
    try:
        return summary(repository(cwd)[0])
    except (ValueError, OSError, subprocess.SubprocessError):
        return ''


def enabled(kind, path):
    """(allowed, reason) for one flag of the repository holding `path`; any doubt reads as OFF."""
    try:
        root, _ = repository(path)
        store = store_root(root)
        state, problem = load(store)
        if problem:
            return False, describe_invalid(kind, root, store, problem)
        value, source = effective(state, key(store, root), kind)
        return value, describe(kind, root, value, source)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        return False, f'{kind.upper()} PERMISSION: OFF; the repository cannot be resolved: {exc}'


def planned(kind, path):
    """(allowed, reason) for a repository not checked out yet, read at the path it will be cloned into.

    The path must sit below this workspace and be missing or an empty directory; its flag is its own override, else
    the longest folder override above it, else the default. Any doubt reads as OFF."""
    try:
        path = Path(path)
        path = (path if path.is_absolute() else ROOT / path).resolve()
        if path == ROOT or not path.is_relative_to(ROOT):
            raise ValueError(f'{path} is not a checkout path inside this workspace')
        if path.exists() and (not path.is_dir() or any(path.iterdir())):
            raise ValueError(f'{path} already exists, so the new repository has no free checkout path')
        store = store_root(path)
        state, problem = load(store)
        if problem:
            return False, describe_invalid(kind, path, store, problem)
        value, source = effective(state, key(store, path), kind)
        return value, describe_planned(kind, path, value, source)
    except (ValueError, OSError) as exc:
        return False, f'{kind.upper()} PERMISSION: OFF; {exc}.'


def directive_text(text):
    """Decode only the supported Markdown escapes in a leading permission marker."""
    if not isinstance(text, str):
        return text
    text = text.strip()
    for kind in (*KINDS, 'git'):
        for action in ('on', 'off', 'status'):
            escaped = '\\~' + kind + '\\_' + action
            if text.startswith(escaped) and text[len(escaped):len(escaped) + 1].isspace():
                return '~' + kind + '_' + action + text[len(escaped):]
    return text


def arguments(text, pattern):
    """The shell words of a whole-message directive, or None."""
    text = directive_text(text)
    if not isinstance(text, str) or '\n' in text.strip() or '\r' in text.strip():
        return None
    if not re.match(pattern.pattern + r'\s', text.strip()):
        return None
    try:
        return shlex.split(text.strip())
    except ValueError:
        return None


def directive(text):
    """(action, target, kind) for a whole-message `~commit_*` / `~push_*` directive; None otherwise.

    The entire user message must be one directive; examples and quoted transcripts are data."""
    args = arguments(text, DIRECTIVE)
    match = DIRECTIVE.fullmatch(args[0]) if args and len(args) == 2 else None
    if not match:
        return None
    return match.group(2), args[1], match.group(1)


def git_directive(text):
    """(action, kinds, targets) for a whole-message `~git_on|off|status` directive; None otherwise.

    `~git_on <kind>[,<kind>...] <target>...` and `~git_off <kind>[,...]|all <target>...` name each kind once;
    `~git_status <target>...` reads every kind. A retired kind yields the action `retired`, which changes nothing."""
    args = arguments(text, GIT_DIRECTIVE)
    match = GIT_DIRECTIVE.fullmatch(args[0]) if args else None
    if not match:
        return None
    action = match.group(1)
    if action == 'status':
        kinds, targets = KINDS, args[1:]
    elif len(args) < 3:
        return None
    else:
        names = args[1].split(',')
        if len(set(names)) != len(names):
            return None
        if action == 'off' and names == ['all']:
            kinds = KINDS
        elif all(name in KINDS for name in names):
            kinds = tuple(names)
        elif all(name in KINDS or name in RETIRED for name in names):
            action, kinds = 'retired', tuple(names)
        else:
            return None  # `all` never enables; an unknown kind voids the directive
        targets = args[2:]
    if not targets or len(set(targets)) != len(targets):
        return None
    return action, tuple(kinds), tuple(targets)


def directives(text):
    """Every (action, target, kind) a whole-message directive names; None otherwise."""
    single = directive(text)
    if single is not None:
        return [single]
    parsed = git_directive(text)
    if parsed is None:
        return None
    action, kinds, targets = parsed
    return [(action, target, kind) for target in targets for kind in kinds]


def resolve(target):
    """(store, key, repository root or folder) for a directive target; `*` is this workspace's default.

    A repository target must name the repository's root: a folder inside one (`workbench/org` inside the hub) would
    otherwise set the enclosing repository's flag, so it voids the directive."""
    if target == DEFAULT:
        return ROOT, DEFAULT, None
    if target.endswith(FOLDER):
        return folder(ROOT / target[:-len(FOLDER)])
    path = (ROOT / target).resolve()
    root, _ = repository(path)
    if Path(root) != path:
        raise ValueError(f'{target} is a folder inside {root}, not a repository root; name the repository root, '
                         f'or `{target.rstrip("/")}/*` for every repository under the folder')
    store = store_root(root)
    return store, key(store, root), root


def change(payload, sid, parsed, targets):
    """Records the changes of one genuine user prompt event, one log entry per store, and describes the result."""
    if not nonempty(sid) or not nonempty(payload.get('turn_id')):
        return 'Git flags unchanged: native user event identity is missing; no grant recorded.'
    groups = {}
    for action, target, kind in parsed:
        store, name, root = targets[target]
        groups.setdefault(store, []).append((action == 'on', name, kind, root))
    event = consent_id(sid, payload['turn_id'], payload['prompt'])
    lines = []
    for store, items in groups.items():
        with locked(store):
            state, problem = load(store)
            anchor = None
            if problem:
                if any(value for value, *_ in items):
                    lines.append(f'Git flags unchanged in {store}: {problem}. Every flag there reads OFF; '
                                 'a `~git_off` directive resets the store, then enable again.')
                    continue
                state, anchor = fresh(store)
                lines.append(f'The flag store in {store} was invalid ({problem}); it restarts with every flag OFF.')
            if event in state['seen_consents']:
                lines.append(f'This directive was already recorded in {store}; state unchanged.')
                continue
            changes = []
            for value, name, kind, _ in items:
                flags = state['defaults'] if name == DEFAULT else state['repositories'].setdefault(name, {})
                flags[kind] = value
                changes.append({'target': name, 'kind': kind, 'value': value})
            state['seen_consents'] = [*state['seen_consents'], event][-SEEN_LIMIT:]
            record(store, state, changes, {'session_id': sid, 'turn_id': payload['turn_id'],
                                           'prompt': payload['prompt'], 'base': str(ROOT)}, anchor)
            lines += [describe_default(kind, store, value) if name == DEFAULT
                      else describe_folder(kind, name, *effective(state, name[:-1], kind)) if name.endswith(FOLDER)
                      else describe(kind, root, *effective(state, name, kind)) for value, name, kind, root in items]
    return '\n'.join(lines)


def report(parsed, targets, single):
    """Status of each target: one flag for `~commit_status` / `~push_status`, every flag for `~git_status`."""
    lines = []
    for target in dict.fromkeys(target for _, target, _ in parsed):
        store, name, root = targets[target]
        if single:
            kind = parsed[0][2]
            if name.endswith(FOLDER):
                lines.append(folder_status(store, name, kind))
                continue
            if name != DEFAULT:
                lines.append(status(root, None, kind))
                continue
            state, problem = load(store)
            lines.append(f'{kind.upper()} PERMISSION: OFF by default in {store}; invalid state: {problem}.'
                         if problem else describe_default(kind, store, state['defaults'][kind]))
        else:
            lines.append(overview(store) if name == DEFAULT
                         else folder_summary(store, name) if name.endswith(FOLDER) else summary(root))
    return '\n'.join(lines)


def prompt(payload):
    sid = payload.get('session_id')
    text = payload.get('prompt')
    parsed = directives(text)
    try:
        if parsed and payload.get('hook_event_name') == 'UserPromptSubmit':
            retired = [kind for action, _, kind in parsed if action == 'retired' and kind in RETIRED]
            if retired:
                return ('Git flags unchanged: ' + ', '.join(
                    f'`{kind}` merged into `{RETIRED[kind]}`' for kind in dict.fromkeys(retired))
                    + '. The kinds are `commit` and `push`; repeat the directive with those.')
            # Every named target resolves before any flag changes, so a bad path changes nothing.
            targets = {target: resolve(target) for target in dict.fromkeys(t for _, t, _ in parsed)}
            if parsed[0][0] == 'status':
                return report(parsed, targets, directive(text) is not None)
            return change(payload, sid, parsed, targets)
        return session_status(payload.get('cwd') or ROOT)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        return 'Git flags unchanged; no grant recorded: ' + str(exc)


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


def configured_remote(cwd, args):
    """True when a push names no remote, or one the repository has configured; a URL or a path never is one."""
    named = [arg for arg in args[1:] if not arg.startswith('-')]
    if not named:
        return True
    try:
        result = subprocess.run(['git', '-C', str(cwd), 'remote'], text=True, capture_output=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0 and named[0] in result.stdout.split()


def assess(payload, command, cwd):
    """(allowed, reason) for an ordinary commit or push, each decided by its repository flag; None otherwise.

    An ordinary push names no remote or a remote configured in the repository; a URL or a path is a remote write in
    disguise, so that push is not the ordinary form."""
    parsed = git_command(command, cwd)
    if parsed is None:
        return None
    cwd, args = parsed
    kind = ('commit' if ordinary_commit(args)
            else 'push' if ordinary_push(args) and configured_remote(cwd, args) else None)
    if kind is None:
        return None
    if not nonempty(payload.get('turn_id')):
        return False, f'{kind.capitalize()} blocked: missing native turn identity. Repository flag unchanged.'
    allowed, reason = enabled(kind, cwd)
    return bool(allowed), reason


def permits(payload, command, cwd):
    result = assess(payload, command, cwd)
    return result is not None and result[0]


def notice(payload, command, cwd):
    """Kept for callers: with each flag as the final state there is no per-chat confirmation to surface."""
    return ''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['status'])
    parser.add_argument('--repo', default='.', help='a repository, a folder followed by `/*`, or `*`')
    args = parser.parse_args()
    try:
        print(overview(ROOT) if args.repo == DEFAULT else statuses(args.repo))
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        parser.exit(1, 'Cannot inspect repository flags: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
