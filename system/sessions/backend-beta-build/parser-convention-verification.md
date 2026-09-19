# Parser convention verification

*Last updated: 2026-09-13*

> The confirmed `Parser` role for format decoding, with no SDK implementation changes.

## Applied

- Added [parser](../../../conventions/development/backend/dotnet/core/mla/constructs/behavior/parser.md).
- Registered its role in the [behavior index](../../../conventions/development/backend/dotnet/core/mla/constructs/behavior/behavior.md)
  and [construct keep-list](../../../conventions/development/backend/dotnet/core/mla/constructs/constructs.md).
- Scope: text, bytes or streams decoded into structured data; format-specific implementations and selection under one parsing contract.
- Requires declared malformed, incomplete, empty and partial-input behavior without forcing one failure carrier on every parser.
- Stream contracts cover caller ownership, consumption, seeking, cancellation and deferred enumeration lifetime.
- Existing result-carrier rules remain authoritative; no new blanket prohibition on Mapper behavior.
- Business orchestration and operations performed on parsed results stay outside the parsing role.
- `CronExpressionParser.NextOccurrence` remains SDK sweep work; the role does not bless that mixed responsibility.

---

## Checks

- Checked all 91 local link targets in the new parser doc and both edited indexes: zero missing targets.
- All lines in the new parser convention are at most 120 characters.
- Scoped `git diff --check` passed.
- No SDK source edits, build, test, pack or Git mutations were performed for this documentation-only task.
