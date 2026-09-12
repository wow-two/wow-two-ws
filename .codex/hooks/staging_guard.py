#!/usr/bin/env python3
"""Require native escalation for recognizable Git index writes.

This guard does not infer conversational consent or grant approval. The runtime
owns approval. Shell parsing is a guardrail, not a complete security boundary.
"""
import shlex

def index_write(command):
    try:
        lex = shlex.shlex(command, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        tokens = list(lex)
    except ValueError:
        return True  # malformed shell is not an approval bypass
    expect_command = True
    for i, token in enumerate(tokens):
        if token in {';', '&&', '||', '|', '&', '(', ')'}:
            expect_command = True
            continue
        if not expect_command:
            continue
        if token in {'env', 'sudo', 'command', 'exec', 'nohup'} or '=' in token:
            continue
        expect_command = False
        if token.rsplit('/', 1)[-1] in {'bash', 'sh', 'zsh'}:
            if i + 2 < len(tokens) and tokens[i + 1] in {'-c', '-lc'}:
                if index_write(tokens[i + 2]):
                    return True
        if token.rsplit('/', 1)[-1] != 'git':
            continue
        j = i + 1
        while j < len(tokens) and tokens[j].startswith('-'):
            j += 2 if tokens[j] in {'-C', '-c', '--git-dir', '--work-tree', '--namespace'} else 1
        if j == len(tokens):
            continue
        sub = tokens[j]
        args = []
        for arg in tokens[j + 1:]:
            if arg in {';', '&&', '||', '|', '&', ')'}:
                break
            args.append(arg)
        flags = set(args)
        if sub in {'add', 'update-index', 'read-tree', 'rm', 'mv'}:
            return True
        if sub in {'apply', 'rm'} and flags & {'--cached', '--index'}:
            return True
        if sub == 'restore' and (flags & {'--staged', '-S'} or any(a.startswith('-S') for a in args)):
            return True
        if sub == 'commit' and (flags & {'--all', '--include', '--only'} or any(a.startswith('-') and not a.startswith('--') and any(c in a[1:] for c in 'aio') for a in args)):
            return True
    return False

def check(command, tool_input):
    if index_write(command) and tool_input.get('sandbox_permissions') != 'require_escalated':
        return ('STAGING BLOCKED: explicit user consent for the repository and file set is required. '
                'With consent, use the direct shell tool with sandbox_permissions=require_escalated, '
                'a scope-specific justification and no reusable prefix. If unavailable, hand staging '
                'to the user in GitKraken. Do not bypass through another tool or script.')
    return None
