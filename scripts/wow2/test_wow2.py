"""Tests for wow2.py: the request each command sends, what it prints, and that a value never reaches stdout, stderr,
argv or a refusal. Nothing here touches the Keychain, the network or a console.

  python3 -I -m unittest discover -s scripts/wow2        (from the workspace root)
"""
import importlib.util
import io
import json
import sys
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("wow2", HERE / "wow2.py")
wow2 = importlib.util.module_from_spec(SPEC)
sys.modules["wow2"] = wow2  # dataclasses resolve annotations through the module
SPEC.loader.exec_module(wow2)

SECRET = "sk-ant-api03-NEVER_PRINTED_9f2c"
KEY = "wh_" + "A" * 32
CREDENTIALS = wow2.Credentials("https://wheelhouse.example.ts.net", KEY)


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class Recorder:
    """Stands in for urlopen: keeps each request and answers with a canned reply or an HTTP error."""

    def __init__(self, data=None, status=200, problem=None):
        self.requests, self.data, self.status, self.problem = [], data or {}, status, problem or {}

    def __call__(self, request, timeout=None, context=None):
        self.requests.append(request)
        if self.status != 200:
            raise urllib.error.HTTPError(request.full_url, self.status, "refused", {},
                                         io.BytesIO(json.dumps(self.problem).encode()))
        return FakeResponse(json.dumps({"data": self.data}).encode())

    @property
    def body(self):
        return json.loads(self.requests[-1].data)


class Tty(io.StringIO):
    def isatty(self):
        return True


class Pipe(io.StringIO):
    def isatty(self):
        return False


def args(*argv):
    return wow2.parser().parse_args(list(argv))


class SecretSetTests(unittest.TestCase):
    def test_a_typed_secret_goes_to_the_derived_target_and_prints_only_key_target_and_version(self):
        opener = Recorder({"keys": [{"key": "Ai:Providers:anthropic:ApiKey", "secret": True, "version": 3}]})
        out = wow2.cmd_secret_set(args("secret", "set", "harvest", "dev", "Ai:Providers:anthropic:ApiKey"), CREDENTIALS,
                                  opener, stdin=Tty(), ask=lambda prompt: SECRET)

        request = opener.requests[-1]
        self.assertEqual((request.method, request.full_url),
                         ("PUT", "https://wheelhouse.example.ts.net/api/deployments/targets/harvest-dev/settings"))
        self.assertEqual(request.get_header("X-wheelhouse-action"), "settings")
        self.assertEqual(request.get_header("Authorization"), "Bearer " + KEY)
        self.assertEqual(opener.body, {"values": [{"key": "Ai:Providers:anthropic:ApiKey", "value": SECRET, "secret": True}]})
        self.assertEqual(out, "Ai:Providers:anthropic:ApiKey -> harvest-dev: secret v3")
        self.assertNotIn(SECRET, out)

    def test_a_piped_secret_drops_one_trailing_newline_and_never_prompts(self):
        opener = Recorder({"keys": [{"key": "A:B", "secret": True, "version": 1}]})

        def refuse(prompt):
            raise AssertionError("prompted although stdin was piped")

        wow2.cmd_secret_set(args("secret", "set", "ocharo", "prod", "A:B", "--note", "rotated"), CREDENTIALS, opener,
                            stdin=Pipe(SECRET + "\n"), ask=refuse)
        self.assertEqual(opener.body["values"][0], {"key": "A:B", "value": SECRET, "secret": True, "note": "rotated"})
        self.assertIn("/targets/ocharo-prod/", opener.requests[-1].full_url)

    def test_an_explicit_target_wins_over_the_derived_one(self):
        opener = Recorder({"keys": []})
        wow2.cmd_secret_set(args("secret", "set", "harvest", "dev", "A:B", "--target", "harvestadapters-dev"), CREDENTIALS,
                            opener, stdin=Pipe(SECRET), ask=None)
        self.assertIn("/targets/harvestadapters-dev/", opener.requests[-1].full_url)

    def test_an_empty_value_saves_nothing(self):
        opener = Recorder()
        with self.assertRaisesRegex(wow2.CliError, "no value"):
            wow2.cmd_secret_set(args("secret", "set", "harvest", "dev", "A:B"), CREDENTIALS, opener,
                                stdin=Tty(), ask=lambda prompt: "")
        self.assertEqual(opener.requests, [])

    def test_a_refusal_names_the_status_and_detail_never_the_value(self):
        for status, problem, expected in [
            (401, {}, "unknown or revoked"),
            (403, {}, "settings:write"),
            (404, {"detail": "Target 'ghost-dev' was not found."}, "no target ghost-dev"),
            (400, {"detail": "A:B is declared a secret; save it as a secret."}, "400: A:B is declared"),
        ]:
            with self.subTest(status=status):
                opener = Recorder(status=status, problem=problem)
                with self.assertRaises(wow2.CliError) as raised:
                    wow2.cmd_secret_set(args("secret", "set", "ghost", "dev", "A:B"), CREDENTIALS, opener,
                                        stdin=Pipe(SECRET), ask=None)
                self.assertIn(expected, str(raised.exception))
                self.assertNotIn(SECRET, str(raised.exception))


class OtherCommandTests(unittest.TestCase):
    def test_generate_asks_wheelhouse_for_the_value(self):
        opener = Recorder({"keys": [{"key": "Billing:SecretKey", "secret": True, "version": 1, "generated": True}]})
        out = wow2.cmd_secret_generate(args("secret", "generate", "foreverpin", "dev", "Billing:SecretKey", "--format", "hex"),
                                       CREDENTIALS, opener)
        self.assertEqual(opener.body, {"values": [{"key": "Billing:SecretKey", "secret": True, "generate": "hex"}]})
        self.assertEqual(out, "Billing:SecretKey -> foreverpin-dev: secret v1 (generated)")

    def test_a_plain_setting_takes_its_argument_and_the_confirmation(self):
        opener = Recorder({"keys": [{"key": "Ai:Tagging:Enabled", "secret": False}]})
        out = wow2.cmd_setting_set(args("setting", "set", "harvest", "dev", "Ai:Tagging:Enabled", "true", "--confirm-plain"),
                                   CREDENTIALS, opener)
        self.assertEqual(opener.body, {"values": [{"key": "Ai:Tagging:Enabled", "value": "true", "secret": False,
                                                   "confirmPlain": True}]})
        self.assertEqual(out, "Ai:Tagging:Enabled -> harvest-dev: setting")

    def test_check_reads_a_validation_refusal_as_a_working_key(self):
        self.assertIn("reaches", wow2.cmd_check(args("check"), CREDENTIALS, Recorder(status=400, problem={"title": "invalid"})))
        with self.assertRaisesRegex(wow2.CliError, "403"):
            wow2.cmd_check(args("check"), CREDENTIALS, Recorder(status=403))

    def test_addresses_are_checked_before_any_request(self):
        for argv, message in [(("secret", "set", "Harvest", "dev", "A:B"), "not a slug"),
                              (("secret", "set", "harvest", "dev", "A B"), "configuration path")]:
            with self.subTest(argv=argv), self.assertRaisesRegex(wow2.CliError, message):
                wow2.cmd_secret_set(args(*argv), CREDENTIALS, Recorder(), stdin=Pipe(SECRET), ask=None)
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            args("secret", "set", "harvest", "staging", "A:B")


class SetupTests(unittest.TestCase):
    def test_setup_stores_the_url_and_a_wellformed_key_through_stdin_only(self):
        calls = []

        def run(argv, input=None, **kwargs):
            calls.append((argv, input))
            return mock.Mock(returncode=0, stderr="", stdout="")

        with mock.patch.object(wow2.subprocess, "run", run), mock.patch.object(wow2, "link_on_path", lambda: ""), \
                mock.patch.object(wow2, "check", lambda credentials: "key reaches the console"):
            out = wow2.cmd_setup(args("setup", "--url", "https://wheelhouse.example.ts.net/"), ask=lambda prompt: KEY)
        self.assertEqual([argv for argv, _ in calls], [["security", "-i"], ["security", "-i"]])
        self.assertIn("-a url", calls[0][1])
        self.assertIn("-w https://wheelhouse.example.ts.net\n", calls[0][1])
        self.assertIn("-a key", calls[1][1])
        self.assertTrue(all(KEY not in " ".join(argv) for argv, _ in calls), "the key never reaches argv")
        self.assertNotIn(KEY, out)
        self.assertIn("key reaches the console", out)

    def test_setup_keeps_the_key_and_says_so_when_the_check_fails(self):
        def refuse(credentials):
            raise wow2.CliError("403: the stored key does not grant settings:write")

        ok = mock.Mock(returncode=0, stderr="", stdout="")
        with mock.patch.object(wow2.subprocess, "run", return_value=ok), mock.patch.object(wow2, "link_on_path", lambda: ""), \
                mock.patch.object(wow2, "check", refuse):
            out = wow2.cmd_setup(args("setup", "--url", "https://wheelhouse.example.ts.net"), ask=lambda prompt: KEY)
        self.assertIn("stored, but the check failed: 403", out)

    def test_setup_refuses_a_malformed_key_or_a_plain_http_url(self):
        with mock.patch.object(wow2.subprocess, "run") as run:
            with self.assertRaisesRegex(wow2.CliError, "not a Wheelhouse integration key"):
                wow2.cmd_setup(args("setup", "--url", "https://wheelhouse.example.ts.net"), ask=lambda prompt: "sk-oops")
            with self.assertRaisesRegex(wow2.CliError, "https origin"):
                wow2.cmd_setup(args("setup", "--url", "http://wheelhouse.example.ts.net"), ask=lambda prompt: KEY)
            run.assert_not_called()

    def test_main_reports_a_missing_setup_on_stderr(self):
        err = io.StringIO()
        with mock.patch.object(wow2, "keychain_read", lambda account: None), redirect_stderr(err), redirect_stdout(io.StringIO()):
            code = wow2.main(["secret", "set", "harvest", "dev", "A:B"])
        self.assertEqual(code, 1)
        self.assertIn("wow2 setup", err.getvalue())


if __name__ == "__main__":
    unittest.main()
