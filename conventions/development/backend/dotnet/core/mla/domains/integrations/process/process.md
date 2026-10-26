# Process

*Last updated: 2026-10-26*

> Running a child process — a CLI, `yt-dlp`, `ffmpeg`, a Python adapter — behind the client/broker boundary.

## Registration

- must run a child process through the be sdk's `IProcessClient`; never start a `Process` by hand.
- must register it with `AddProcessClient`, keyed by name when tools need different options.
- must set `ProcessClientOptions.Timeout` to the tool's budget; a timeout kills the whole process tree.
- must pass the caller's cancellation token into every run.
- client and broker placement → [integrations](../integrations.md#contract).

---

## Environment

- must not shell out with the host's whole environment; a child gets only the variables listed.
- must add an inherited variable by name to `InheritedVariables`, beyond `ProcessEnvironmentConstants.Baseline`.
- must set a child-only value in `ProcessSpec.Environment`, never in the host's own environment.

---

## Arguments

- must pass arguments as `ProcessSpec.Arguments`, never through a shell or one command string.
- must pass a secret or a payload through `StandardInput`, never as an argument.

---

## Output and failures

- must read a JSON answer with `RunJsonAsync`, never by parsing standard output by hand.
- must read a tool's failure line through an `IProcessFailureParser`, such as `JsonFailureLineParser`.
- must word a message per `ProcessFailureMapper.KindOf`; never echo arguments, environment or output.
- may use `Start` only for a child that outlives the call and is reaped elsewhere.
