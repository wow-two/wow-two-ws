#!/usr/bin/env python3
"""wow2 -- the WoW2 command line. First slice: write-only settings and secrets in Wheelhouse.

  wow2 setup --url <console>                       store the console URL and an integration key in the Keychain
  wow2 install                                     link `wow2` into ~/.local/bin and put it on PATH (setup does too)
  wow2 check                                       prove the stored key reaches the settings save
  wow2 secret set <product> <env> <key>            type a secret at a hidden prompt, or pipe it on stdin
  wow2 secret generate <product> <env> <key>       Wheelhouse makes a random value; nobody ever sees it
  wow2 setting set <product> <env> <key> [value]   a plain, non-secret setting

The target is `<product>-<env>` (`harvest-dev`); `--target` names another. The key is an integration key granting
`settings:write`, which saves values and reads nothing back. Values never reach argv, a log, stdout or the Keychain:
they go from the prompt or stdin straight into one HTTPS request. Wheelhouse audits each save as `key:{name}`, by key
and vault version only. Docs: wow-two-platform.wheelhouse `engineering/deployment/deployment.md` § The wow2 CLI.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

KEYCHAIN_SERVICE = "wow2.wheelhouse"
KEY_PATTERN = re.compile(r"^wh_[A-Za-z0-9]{32}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ENVIRONMENTS = ("dev", "prod")
GENERATE_FORMATS = ("hex", "base64url")
TIMEOUT_SECONDS = 30


class CliError(Exception):
    """A refusal to report on stderr with exit code 1; its text never holds a value."""


@dataclass(frozen=True)
class Credentials:
    url: str
    key: str


# Keychain --------------------------------------------------------------------------------------------------------


def keychain_read(account: str) -> str | None:
    """Reads one generic password of the wow2 service; the value stays in this process."""
    done = subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", account, "-w"],
                          capture_output=True, text=True, check=False)
    return done.stdout.rstrip("\n") if done.returncode == 0 else None


def keychain_write(account: str, value: str) -> None:
    """Stores one generic password through `security -i` on stdin, so the value never shows in a process list."""
    if not re.fullmatch(r"[A-Za-z0-9_:/.\-]+", value):
        raise CliError(f"refused to store {account}: unexpected characters")
    command = f"add-generic-password -U -s {KEYCHAIN_SERVICE} -a {account} -l wow2-wheelhouse-{account} -w {value}\n"
    done = subprocess.run(["security", "-i"], input=command, capture_output=True, text=True, check=False)
    if done.returncode != 0 or "error" in done.stderr.lower():
        raise CliError(f"the Keychain refused {account}: {done.stderr.strip().splitlines()[-1] if done.stderr.strip() else done.returncode}")


def stored_credentials(read: Callable[[str], str | None] | None = None) -> Credentials:
    read = read or keychain_read  # looked up per call, so a test's patch holds
    url, key = read("url"), read("key")
    if not url or not key:
        raise CliError("no Wheelhouse console stored; run `wow2 setup --url <console>` first")
    return Credentials(url.rstrip("/"), key)


# Wheelhouse ------------------------------------------------------------------------------------------------------


def save_settings(credentials: Credentials, target: str, values: list[dict], opener=urllib.request.urlopen) -> dict:
    """PUTs the values to the target's settings and returns the reply's `data`; errors name the status and Wheelhouse's
    own detail, which never quotes a value."""
    body = json.dumps({"values": values}).encode()
    request = urllib.request.Request(
        f"{credentials.url}/api/deployments/targets/{urllib.parse.quote(target)}/settings", data=body, method="PUT",
        headers={"Authorization": f"Bearer {credentials.key}", "X-Wheelhouse-Action": "settings",
                 "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "wow2-cli"})
    try:
        with opener(request, timeout=TIMEOUT_SECONDS, context=ssl.create_default_context()) as response:
            return json.load(response).get("data") or {}
    except urllib.error.HTTPError as error:
        raise CliError(describe_refusal(error.code, error.read(), target)) from None
    except urllib.error.URLError as error:
        raise CliError(f"cannot reach {credentials.url}: {error.reason} (is the tailnet up?)") from None


def describe_refusal(status: int, payload: bytes, target: str) -> str:
    if status == 401:
        return "401: the stored key is unknown or revoked; create one and run `wow2 setup` again"
    if status == 403:
        return "403: the stored key does not grant settings:write"
    detail = ""
    try:
        problem = json.loads(payload or b"{}")
        detail = problem.get("detail") or problem.get("title") or ""
        errors = problem.get("errors")
        if isinstance(errors, dict):
            detail = " ".join([detail] + [m for messages in errors.values() for m in messages]).strip()
    except (ValueError, AttributeError):
        pass
    if status == 404:
        return f"404: no target {target}" + ("" if not detail else f" ({detail})") + "; name it with --target"
    return f"{status}: {detail or 'Wheelhouse refused the save'}"


def target_of(product: str, environment: str, explicit: str | None) -> str:
    if environment not in ENVIRONMENTS:
        raise CliError(f"environment must be one of {', '.join(ENVIRONMENTS)}")
    target = explicit or f"{product}-{environment}"
    for name, slug in (("product", product), ("target", target)):
        if not SLUG_PATTERN.fullmatch(slug):
            raise CliError(f"{name} {slug!r} is not a slug")
    return target


def check_key(name: str) -> str:
    if not name or len(name) > 1009 or any(ch.isspace() for ch in name):
        raise CliError("a setting key is a configuration path such as Ai:Providers:anthropic:ApiKey")
    return name


def read_value(prompt: str, hidden: bool, stdin=None, ask=getpass.getpass) -> str:
    """The value from piped stdin (one trailing newline dropped), else from a prompt, hidden for a secret."""
    stdin = stdin or sys.stdin
    if not stdin.isatty():
        value = stdin.read()
        value = value[:-1] if value.endswith("\n") else value
        value = value[:-1] if value.endswith("\r") else value
    else:
        value = ask(prompt) if hidden else input(prompt)
    if not value:
        raise CliError("no value given; nothing saved")
    return value


def report(target: str, data: dict) -> str:
    lines = []
    for item in data.get("keys", []):
        if item.get("removed"):
            what = "removed"
        elif item.get("secret"):
            what = f"secret v{item['version']}" if item.get("version") else "secret"
            what += " (generated)" if item.get("generated") else ""
        else:
            what = "setting"
        lines.append(f"{item.get('key')} -> {target}: {what}")
    return "\n".join(lines) or f"{target}: nothing saved"


# Commands --------------------------------------------------------------------------------------------------------


def cmd_setup(args, ask=getpass.getpass) -> str:
    url = (args.url or input("Wheelhouse console URL: ")).strip().rstrip("/")
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.path not in ("", "/"):
        raise CliError("the console URL is its https origin, such as https://wheelhouse.<tailnet>.ts.net")
    key = ask("Integration key (settings:write; hidden): ").strip()
    if not KEY_PATTERN.fullmatch(key):
        raise CliError("that is not a Wheelhouse integration key (wh_ and 32 letters or digits); nothing stored")
    keychain_write("url", url)
    keychain_write("key", key)
    lines = [f"stored the console URL and key {key[:11]}… in the Keychain ({KEYCHAIN_SERVICE})"]
    lines.append(link_on_path())
    try:
        lines.append(check(Credentials(url, key)))
    except CliError as error:
        lines.append(f"stored, but the check failed: {error}")
    return "\n".join(line for line in lines if line)


PATH_MARKER = "# wow2: ~/.local/bin on PATH"


def link_on_path(home: Path | None = None, script: Path | None = None) -> str:
    """Links ~/.local/bin/wow2 to this script and puts ~/.local/bin on a login shell's PATH; both idempotent."""
    home = home or Path.home()
    script = (script or Path(__file__)).resolve()
    bin_dir = home / ".local" / "bin"
    link = bin_dir / "wow2"
    lines = []
    if link.is_symlink() and link.resolve() == script:
        pass
    elif link.exists() or link.is_symlink():
        lines.append(f"left {link} as it is (it is not this script); run this script by its path")
    else:
        bin_dir.mkdir(parents=True, exist_ok=True)
        link.symlink_to(script)
        lines.append(f"linked {link} -> {script}")
    lines.append(ensure_on_path(home))
    return "\n".join(line for line in lines if line)


def ensure_on_path(home: Path) -> str:
    """Appends ~/.local/bin to PATH in the login profile (zsh: ~/.zprofile, which Warp's login tabs read) unless a
    startup file already puts it there."""
    shell = os.path.basename(os.environ.get("SHELL", "zsh"))
    if shell == "bash":
        profile, startup = home / ".bash_profile", [home / ".bash_profile", home / ".bashrc", home / ".profile"]
    else:
        profile, startup = home / ".zprofile", [home / ".zprofile", home / ".zshrc", home / ".zshenv"]
    for path in startup:
        text = path.read_text() if path.is_file() else ""
        if PATH_MARKER in text or any(".local/bin" in line and "PATH" in line and not line.lstrip().startswith("#")
                                      for line in text.splitlines()):
            return ""
    existing = profile.read_text() if profile.is_file() else ""
    separator = "" if not existing or existing.endswith("\n") else "\n"
    with profile.open("a") as handle:
        handle.write(f'{separator}\n{PATH_MARKER}\nexport PATH="$PATH:$HOME/.local/bin"\n')
    return f"added ~/.local/bin to PATH in {profile}; open a new terminal tab for `wow2`"


def cmd_check(args, credentials: Credentials, opener=urllib.request.urlopen) -> str:
    return check(credentials, opener)


def check(credentials: Credentials, opener=urllib.request.urlopen) -> str:
    # An empty save is refused by validation (400) only after the key passed authentication and its scope.
    try:
        save_settings(credentials, "wow2-check", [], opener)
    except CliError as error:
        if str(error).startswith("400"):
            return f"key {credentials.key[:11]}… reaches {credentials.url} with settings:write"
        raise
    raise CliError("the console accepted an empty save; expected a 400")


def cmd_secret_set(args, credentials: Credentials, opener=urllib.request.urlopen, stdin=None, ask=getpass.getpass) -> str:
    target = target_of(args.product, args.env, args.target)
    key = check_key(args.key)
    value = read_value(f"{key} for {target} (hidden): ", hidden=True, stdin=stdin, ask=ask)
    entry = {"key": key, "value": value, "secret": True}
    if args.note:
        entry["note"] = args.note
    return report(target, save_settings(credentials, target, [entry], opener))


def cmd_secret_generate(args, credentials: Credentials, opener=urllib.request.urlopen) -> str:
    target = target_of(args.product, args.env, args.target)
    entry = {"key": check_key(args.key), "secret": True, "generate": args.format}
    if args.note:
        entry["note"] = args.note
    return report(target, save_settings(credentials, target, [entry], opener))


def cmd_setting_set(args, credentials: Credentials, opener=urllib.request.urlopen, stdin=None) -> str:
    target = target_of(args.product, args.env, args.target)
    key = check_key(args.key)
    value = args.value if args.value is not None else read_value(f"{key} for {target}: ", hidden=False, stdin=stdin)
    entry = {"key": key, "value": value, "secret": False}
    if args.confirm_plain:
        entry["confirmPlain"] = True
    return report(target, save_settings(credentials, target, [entry], opener))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="wow2", description="The WoW2 command line: write-only Wheelhouse settings.")
    commands = root.add_subparsers(dest="command", required=True)

    setup = commands.add_parser("setup", help="store the console URL and an integration key in the Keychain")
    setup.add_argument("--url", help="the console's https origin")
    commands.add_parser("install", help="link wow2 into ~/.local/bin and put that on PATH; no key needed")
    commands.add_parser("check", help="prove the stored key reaches the settings save")

    def addressed(sub):
        sub.add_argument("product")
        sub.add_argument("env", choices=ENVIRONMENTS)
        sub.add_argument("key", help="the configuration path, such as Ai:Providers:anthropic:ApiKey")
        sub.add_argument("--target", help="the target slug when it is not <product>-<env>")

    secret = commands.add_parser("secret", help="write-only secrets").add_subparsers(dest="action", required=True)
    secret_set = secret.add_parser("set", help="a secret typed at a hidden prompt, or piped on stdin")
    addressed(secret_set)
    secret_set.add_argument("--note", help="a note kept with the new vault version")
    generate = secret.add_parser("generate", help="Wheelhouse makes 32 random bytes; nobody sees them")
    addressed(generate)
    generate.add_argument("--format", choices=GENERATE_FORMATS, default="base64url")
    generate.add_argument("--note", help="a note kept with the new vault version")

    setting = commands.add_parser("setting", help="plain settings").add_subparsers(dest="action", required=True)
    setting_set = setting.add_parser("set", help="a plain setting, from the argument, stdin or a prompt")
    addressed(setting_set)
    setting_set.add_argument("value", nargs="?")
    setting_set.add_argument("--confirm-plain", action="store_true", help="a key that reads as a secret is plain")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "setup":
            print(cmd_setup(args))
            return 0
        if args.command == "install":
            print(link_on_path() or "wow2 is already linked and on PATH")
            return 0
        credentials = stored_credentials()
        if args.command == "check":
            print(cmd_check(args, credentials))
        elif args.command == "secret" and args.action == "set":
            print(cmd_secret_set(args, credentials))
        elif args.command == "secret" and args.action == "generate":
            print(cmd_secret_generate(args, credentials))
        elif args.command == "setting" and args.action == "set":
            print(cmd_setting_set(args, credentials))
        return 0
    except CliError as error:
        print(f"wow2: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nwow2: cancelled; nothing saved", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
