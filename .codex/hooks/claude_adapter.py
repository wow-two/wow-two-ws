#!/usr/bin/env python3
"""Adapt the workspace's shared Claude hooks to Codex lifecycle events."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SHARED = ROOT / '.claude' / 'hooks'
INSTRUCTIONS = ROOT / '.codex' / 'instructions.md'


def context(event, text):
    return {'hookSpecificOutput': {'hookEventName': event, 'additionalContext': text}}


def session_key(payload):
    sid = payload.get('session_id')
    if not isinstance(sid, str) or not sid:
        raise ValueError('missing session_id')
    return 'codex-' + hashlib.sha256((str(ROOT) + '\0' + sid).encode()).hexdigest()[:32]


def checker():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('shared_style', SHARED / 'check-style.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_shared(script, payload):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(ROOT))
    return subprocess.run(
        ['bash', str(SHARED / script)], input=json.dumps(payload),
        text=True, capture_output=True, cwd=ROOT, env=env, timeout=15)


def checked_output(result, script):
    if result.returncode:
        raise RuntimeError(f'{script} exited {result.returncode}: {result.stderr.strip()}')
    return result.stdout.strip()


def start(payload):
    sources = [Path('/Users/max/.codex/conventions/response-style.md'), Path('/Users/max/.codex/conventions/git.md'), ROOT / 'CLAUDE.md']
    deferred = []
    for path in sorted((ROOT / '.claude' / 'rules').rglob('*.md')):
        if 'templates' in path.relative_to(ROOT / '.claude' / 'rules').parts:
            continue
        content = path.read_text()
        if content.startswith('---\n') and re.search(r'^paths:', content.split('---', 2)[1], re.M):
            deferred.append(str(path.relative_to(ROOT)))
        else:
            sources.append(path)
    sources.append(INSTRUCTIONS)
    text = '\n\n'.join(f'Source: {p.relative_to(ROOT) if p.is_relative_to(ROOT) else p}\n{p.read_text()}' for p in sources)
    if deferred:
        text += '\n\nPath-scoped rules: read frontmatter and apply only to matching work: ' + ', '.join(deferred)
    return context('SessionStart', text)


def prompt(payload):
    key = session_key(payload)
    module = checker()
    advisory = io.StringIO()
    with contextlib.redirect_stdout(advisory):
        module.do_prompt({'session_id': key}, module.load_config())
    # One chain: prior verdict -> style pulse/recharge -> Codex rules -> markers.
    # The shared recharge calls the shared marker expander; use an empty prompt
    # there, and expand the actual prompt last so its explicit modifiers win.
    style = checked_output(run_shared('style-recharge.sh', {
        'session_id': key, 'prompt': ''}), 'style-recharge.sh')
    markers = checked_output(run_shared('expand-markers.sh', {
        'prompt': payload.get('prompt') if isinstance(payload.get('prompt'), str) else ''
    }), 'expand-markers.sh')
    bare = bool(re.search(r'^`~(?:bare|queued)`', markers, re.M))
    Path(tempfile.gettempdir(), 'codex-style-mode-' + key).write_text('bare' if bare else '')
    parts = [advisory.getvalue().strip(), style, INSTRUCTIONS.read_text(), markers]
    return context('UserPromptSubmit', '\n\n'.join(p for p in parts if p))


def stop(payload):
    if payload.get('stop_hook_active'):
        return {}
    reply = payload.get('last_assistant_message')
    if not isinstance(reply, str) or not reply.strip():
        # Codex supplies this field. Do not parse its unstable transcript using
        # the Claude JSONL fallback, which cannot recognize Codex messages.
        return {'systemMessage': 'Codex style check skipped: last_assistant_message unavailable.'}
    module = checker()
    key = session_key(payload)
    findings = module.measure(reply, module.load_config())
    mode = Path(tempfile.gettempdir(), 'codex-style-mode-' + key)
    bare = mode.exists() and mode.read_text() == 'bare'
    if bare:
        findings = [line for line in findings if '`### Plan`' not in line]
    path = Path(module.verdict_path(key))
    if findings:
        path.write_text('\n'.join(findings))
    else:
        path.unlink(missing_ok=True)
    return {}


def staging_check(command, args):
    # Shared personal policy; missing guard fails closed for shell operations.
    path = ROOT / '.codex/hooks/staging_guard.py'
    spec = importlib.util.spec_from_file_location('codex_staging_guard', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    reason = module.check(command, args)
    if reason:
        sys.stderr.write(reason + '\n')
        return True
    return False


def guard(payload):
    # Both names are supported for direct tests and native exec payload variants.
    if payload.get('tool_name') not in {'Bash', 'exec_command', 'shell_command', 'shell'}:
        return {}, 0
    args = payload.get('tool_input')
    if not isinstance(args, dict):
        return {'systemMessage': 'Git guard failed: missing shell input.'}, 2
    command = args.get('command', args.get('cmd'))
    if isinstance(command, list):
        # Legacy shell tools can supply [shell, -c, command].
        command = command[-1] if len(command) >= 3 and command[-2] in {'-c', '-lc'} else None
    if not isinstance(command, str):
        return {'systemMessage': 'Git guard failed: missing shell command.'}, 2
    if staging_check(command, args):
        return {}, 2
    normalized = dict(payload, session_id=session_key(payload), tool_name='Bash',
                      cwd=args.get('workdir') or payload.get('cwd') or str(ROOT),
                      tool_input={'command': command})
    result = subprocess.run([sys.executable, str(SHARED / 'guard-git.py')],
        input=json.dumps(normalized), capture_output=True, text=True, cwd=ROOT, timeout=15)
    if result.returncode:
        sys.stderr.write(result.stderr or 'Workspace Git guard failed; command not run.\n')
        return {}, 2
    return {}, 0


def touch(payload):
    args = payload.get('tool_input')
    if not isinstance(args, dict):
        return {'systemMessage': 'Codex touch tracking skipped: missing tool input.'}
    response = payload.get('tool_response')
    if isinstance(response, dict):
        if response.get('isError') or response.get('exit_code', 0) not in (0, None):
            return {}
        output = response.get('output', '')
    else:
        output = response if isinstance(response, str) else ''
    cwd = Path(payload.get('cwd') or ROOT)
    if payload.get('tool_name') == 'apply_patch':
        # Only a confirmed successful patch counts as ownership. Arbitrary shell
        # writes cannot be inferred reliably and stay outside the touch ledger.
        if 'Success. Updated the following files:' not in output:
            return {'systemMessage': 'Codex touch tracking skipped: patch success unavailable.'}
        patch = args.get('command', args.get('input', ''))
        paths = re.findall(r'^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$', patch, re.M)
    else:
        paths = [args[k] for k in ('file_path', 'notebook_path') if isinstance(args.get(k), str)]
        paths += [e['file_path'] for e in args.get('edits', [])
                  if isinstance(e, dict) and isinstance(e.get('file_path'), str)]
    normalized = dict(payload, session_id=session_key(payload), tool_name='MultiEdit',
                      tool_input={'edits': [{'file_path': str((cwd / p).resolve())} for p in paths]})
    result = subprocess.run([sys.executable, str(SHARED / 'track-touch.py')],
        input=json.dumps(normalized), capture_output=True, text=True, cwd=ROOT, timeout=15)
    checked_output(result, 'track-touch.py')
    return {}


def owns_cwd(payload):
    """Avoid two workspace policies running when nested config layers load."""
    cwd = Path(payload.get('cwd') or ROOT).resolve()
    if ROOT not in (cwd, *cwd.parents):
        return True  # Direct tests / callers without workspace cwd still resolve ROOT.
    for parent in (cwd, *cwd.parents):
        if parent == ROOT:
            return True
        if (parent / '.codex/hooks/claude_adapter.py').is_file():
            return False
    return True


def main():
    event = ''
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError('hook payload must be an object')
        event = payload.get('hook_event_name', '')
        if not owns_cwd(payload):
            print('{}')
            return 0
        if event == 'PreToolUse':
            output, code = guard(payload)
        else:
            handler = {'SessionStart': start, 'UserPromptSubmit': prompt, 'Stop': stop, 'PostToolUse': touch}.get(event)
            output, code = (handler(payload) if handler else {}), 0
    except Exception as exc:
        output = {'systemMessage': f'Codex Claude adapter failed ({event or "unknown event"}): {exc}'}
        code = 2 if event == 'PreToolUse' else 0
        if code:
            sys.stderr.write(output['systemMessage'] + '\n')
    print(json.dumps(output, ensure_ascii=False))
    return code


if __name__ == '__main__':
    sys.exit(main())
