"""Tests for library.py: phase detection on fake states, the printed command forms, the local probes, the catalog
edits and the consumer repin. Nothing here touches GitHub, a registry, the hub's files or a real repository.

  python3 -I -m unittest discover -s scripts/release        (from the workspace root)
"""
import importlib.util
import io
import re
import urllib.error
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("library", HERE / "library.py")
library = importlib.util.module_from_spec(SPEC)
sys.modules["library"] = library
SPEC.loader.exec_module(library)

FAKE_ROOT = Path("/ws")
GH = 'GH_TOKEN="$(gh auth token -u sulton-max)" gh '
CLONE = "/ws/workbench/wow-two-sdk-beta/wow-two-sdk-beta.identity"


def lib(**over):
    return library.Library("wow-two-sdk-beta.identity", "Identity", root=over.pop("root", FAKE_ROOT), **over)


# ---- fake states, each one step further along

def fresh(**over):
    """Preflight green; nothing exists yet."""
    base = dict(tools_missing=[], account_ok=True, template_ok=True, scaffold_into=True,
                flags={"commit": True, "push": True, "source": "folder workbench/wow-two-sdk-beta/*"},
                hub_flags={"commit": True, "push": True, "source": "override"},
                author=library.EXPECTED_EMAIL, npm_version=(11, 15, 0), folder="missing", repo_exists=False,
                org_apps=["wheelhouse-max"], nuget_versions=[], npm_versions=[], registry_fresh=True,
                platform_row="none")
    base.update(over)
    return library.State(**base)


def created(**over):
    """The GitHub repo exists, empty, with GitHub's default settings; not cloned."""
    base = dict(repo_exists=True, visibility="private", settings={"has_issues": False, "has_wiki": False, "has_projects": True,
                                            "has_discussions": False},
                workflow={"default_workflow_permissions": "write", "can_approve_pull_request_reviews": False},
                actions_enabled=True, rulesets=[], remote_main="", publish_var="", be_tags=[], fe_tags=[],
                release_tag="", packages_run=library.Run(), image_run=library.Run())
    base.update(over)
    return fresh(**base)


def cloned(**over):
    """Cloned empty and private, settings applied; the ruleset waits for the public flip."""
    base = dict(folder="empty-clone", origin="wow-two-sdk-beta/wow-two-sdk-beta.identity", head="",
                settings={"has_issues": False, "has_wiki": False, "has_projects": False, "has_discussions": False},
                workflow={"default_workflow_permissions": "read", "can_approve_pull_request_reviews": False},
                rulesets=[])
    base.update(over)
    return created(**base)


def scaffolded(**over):
    """Stamped and filled, not committed; the packages still hold the template's sample."""
    base = dict(folder="clone", scaffolded=True, placeholders=[], description="Own user store and OIDC provider",
                sample_content=True)
    base.update(over)
    return cloned(**base)


def pushed(**over):
    base = dict(head="abc123", remote_main="abc123", hub_dirty=["scripts/active.sh",
                                                                 "conventions/deployment/hosting/ports.md"])
    base.update(over)
    return scaffolded(**base)


def registered(**over):
    """Pushed and registered in the hub; the first image is out; the first real slice replaced the sample."""
    base = dict(catalog_entry={"slug": "identity", "deploy": "none",
                               "repositories": ["wow-two-sdk-beta/wow-two-sdk-beta.identity"]},
                hub_committed=True, hub_pushed=True, hub_dirty=[], deploy_worktree="none", deploy_head="none",
                deploy_origin="none", release_tag="v0.1.1", sample_content=False, visibility="public",
                rulesets=["main-guard"])
    base.update(over)
    return pushed(**base)


def plan(state, library_=None, **kw):
    steps = library.evaluate(library_ or lib(), state, **kw)
    return {s.id: s for s in steps}, steps


def chain_ids(steps):
    return [s.id for s in library.next_phase(steps)[1]]


def commands(steps):
    return [c for s in library.next_phase(steps)[1] for c in s.commands]


class PhaseDetection(unittest.TestCase):

    def test_nothing_exists_starts_at_create(self):
        by, steps = plan(fresh())
        self.assertEqual(by["create"].status, "next")
        self.assertEqual(by["clone"].status, "pending")
        self.assertEqual(library.next_phase(steps)[0], 1)
        self.assertEqual(chain_ids(steps), ["create", "clone", "settings"])
        cmds = commands(steps)
        self.assertTrue(cmds[0].startswith(GH + "repo create wow-two-sdk-beta/wow-two-sdk-beta.identity --private "))
        self.assertEqual(cmds[1], GH + f"repo clone wow-two-sdk-beta/wow-two-sdk-beta.identity {CLONE}")
        # settings come after the clone: the guard matches a gh write to a checkout's origin
        self.assertLess(cmds.index(cmds[1]), next(i for i, c in enumerate(cmds) if "repo edit" in c))

    def test_repo_created_but_empty_resumes_at_clone(self):
        by, steps = plan(created())
        self.assertEqual(by["create"].status, "done")
        self.assertEqual(by["clone"].status, "next")
        self.assertEqual(chain_ids(steps), ["clone", "settings"])
        edit = next(c for c in commands(steps) if "repo edit" in c)
        self.assertIn("--enable-projects=false", edit)
        self.assertNotIn("--enable-issues=false", edit)  # already off, so not repeated
        self.assertTrue(any("actions/permissions/workflow" in c for c in commands(steps)))

    def test_empty_clone_moves_to_scaffold(self):
        by, steps = plan(cloned())
        self.assertEqual([by[i].status for i in ("clone", "settings")], ["done"] * 2)
        self.assertEqual(library.next_phase(steps)[0], 2)
        self.assertEqual(chain_ids(steps), ["scaffold", "placeholders", "commit", "push"])
        self.assertEqual(commands(steps)[0], "SHAPE=domain INTO=clone bash /ws/.claude/skills/create-repo/scaffold.sh "
                                             "wow-two-sdk-beta.identity Identity wow-two-sdk-beta")

    def test_scaffolded_with_placeholders_asks_for_the_edit(self):
        by, steps = plan(scaffolded(placeholders=[("README.md", "{{PLACEHOLDER}}")]))
        self.assertEqual(by["scaffold"].status, "done")
        self.assertEqual(by["placeholders"].status, "next")
        self.assertIn("README.md", by["placeholders"].edits[0])
        self.assertEqual(chain_ids(steps), ["placeholders", "commit", "push"])

    def test_scaffolded_but_uncommitted_verifies_then_commits(self):
        by, steps = plan(scaffolded())
        self.assertEqual(chain_ids(steps), ["commit", "push"])
        cmds = commands(steps)
        self.assertTrue(cmds[0].startswith("dotnet test "))
        self.assertIn(f"git -C {CLONE} var GIT_AUTHOR_IDENT", cmds)
        self.assertIn(f"git -C {CLONE} commit -m 'feat: added the Identity domain from the domain template'", cmds)
        self.assertEqual(cmds[-1], f"git -C {CLONE} push origin main")

    def test_scaffolded_but_unpushed_prints_the_push_only(self):
        by, steps = plan(scaffolded(head="abc123"))
        self.assertEqual(by["commit"].status, "done")
        self.assertEqual(by["push"].status, "next")
        self.assertEqual(commands(steps), [f"git -C {CLONE} push origin main"])

    def test_pushed_private_hands_over_the_public_flip(self):
        by, _ = plan(pushed())
        self.assertEqual(by["public"].status, "hand")
        self.assertIn("repo edit wow-two-sdk-beta/wow-two-sdk-beta.identity --visibility public "
                      "--accept-visibility-change-consequences", by["public"].hand[0])
        self.assertEqual(by["ruleset"].status, "pending")
        self.assertEqual(by["content"].status, "pending")
        self.assertEqual(by["nuget-policy"].status, "pending")

    def test_public_repo_without_ruleset_applies_it(self):
        by, steps = plan(registered(rulesets=[]))
        self.assertEqual(by["public"].status, "done")
        self.assertEqual(by["ruleset"].status, "next")
        self.assertEqual(library.next_phase(steps)[0], 2)
        self.assertEqual(chain_ids(steps), ["ruleset"])

    def test_pushed_without_catalog_entry_runs_the_hub_phase(self):
        by, steps = plan(pushed(platform_row="unnamed"))
        self.assertEqual(by["push"].status, "done")
        self.assertEqual(library.next_phase(steps)[0], 3)
        self.assertEqual(chain_ids(steps), ["catalog", "platform-row", "registry", "hub-commit", "hub-push"])
        cmds = commands(steps)
        self.assertIn("apply-local catalog wow-two-sdk-beta.identity --brand Identity --org wow-two-sdk-beta "
                      "--purpose 'Own user store and OIDC provider'", cmds[0])
        add = next(c for c in cmds if " add " in c)
        self.assertIn("scripts/active.sh", add)
        self.assertIn("catalog.yml", add)
        self.assertEqual(cmds[-1], "git -C /ws push origin main")
        self.assertEqual(by["image"].status, "waiting")  # CI builds it from the scaffold push

    def test_sample_content_holds_the_registry_phase(self):
        by, _ = plan(registered(sample_content=True))
        self.assertEqual(by["content"].status, "waiting")
        self.assertIn("Greetings sample", by["content"].note)
        self.assertEqual(by["nuget-policy"].status, "pending")
        by, _ = plan(registered(sample_content=True), publish=True)
        self.assertEqual(by["content"].status, "done")

    def test_packages_not_published_hands_over_the_registry_steps(self):
        by, steps = plan(registered())
        self.assertEqual(by["content"].status, "done")
        self.assertEqual(by["nuget-policy"].status, "consent")
        self.assertEqual(by["npm-first"].status, "hand")
        self.assertEqual(by["arm"].status, "pending")
        self.assertEqual(by["be-published"].status, "pending")
        # the next agent work is the Wheelhouse catalog flip, since the image and the App are there
        self.assertEqual(library.next_phase(steps)[0], 6)
        text = library.render_next(lib(), steps)
        self.assertIn("[ready] nuget-policy", text)
        self.assertIn("[ready] npm-first", text)
        self.assertIn("npm trust github @wow-two-beta/fe-identity --file publish-packages.yml "
                      "--repo wow-two-sdk-beta/wow-two-sdk-beta.identity --allow-publish", text)

    def test_confirmed_policy_arms_and_dispatches_once(self):
        by, steps = plan(registered(deploy_origin="wheelhouse", deploy_head="wheelhouse",
                                    deploy_worktree="wheelhouse"), confirmed=["nuget-policy"])
        self.assertEqual(by["arm"].status, "next")
        self.assertEqual(library.next_phase(steps)[0], 4)
        self.assertEqual(chain_ids(steps), ["arm", "be-published"])
        text = library.render_next(lib(), steps)
        self.assertEqual(text.count("workflow run publish-packages.yml"), 1)
        self.assertIn(GH + "variable set PUBLISH_PACKAGES --body true -R wow-two-sdk-beta/wow-two-sdk-beta.identity",
                      text)

    def test_running_and_failed_publish_runs(self):
        state = registered(publish_var="true", packages_run=library.Run("in_progress", "", "https://run/1"))
        by, _ = plan(state, confirmed=["nuget-policy"])
        self.assertEqual(by["be-published"].status, "waiting")
        state = registered(publish_var="true", packages_run=library.Run("completed", "failure", "https://run/2"))
        by, _ = plan(state, confirmed=["nuget-policy"])
        self.assertEqual(by["be-published"].status, "blocked")

    def test_published_family_with_a_stale_consumer_prints_the_repin(self):
        consumer = Path("/ws/workbench/wow-two-platform/wow-two-platform.wheelhouse")
        pin = library.Pin(consumer / "engineering/Directory.Packages.props", consumer, "property",
                          "IdentitySdkVersion", "10.0.0-beta")
        state = registered(nuget_versions=["10.0.0-beta", "10.0.1-beta"], publish_var="true",
                           consumers=[pin], consumer_flags={str(consumer): {"commit": True, "push": True}},
                           deploy_origin="wheelhouse", deploy_head="wheelhouse", deploy_worktree="wheelhouse")
        by, steps = plan(state, confirmed=["wheelhouse", "secrets"])
        self.assertEqual(by["be-published"].status, "done")
        self.assertEqual(by["consumers"].status, "next")
        cmds = by["consumers"].commands
        self.assertIn("repin wow-two-sdk-beta.identity", cmds[0])
        self.assertIn("--version 10.0.1-beta --only workbench/wow-two-platform/wow-two-platform.wheelhouse --write",
                      cmds[0])
        self.assertEqual(cmds[-1], f"git -C {consumer} push origin main")

    def test_no_consumer_skips_the_last_phase(self):
        by, _ = plan(registered(nuget_versions=["10.0.0-beta"], publish_var="true", consumers=[]))
        self.assertEqual(by["consumers"].status, "skip")

    def test_image_public_probe_reads_back_into_the_step(self):
        by, _ = plan(registered(image_public=True))
        self.assertEqual(by["image-public"].status, "done")
        by, _ = plan(registered(image_public=False))
        self.assertEqual(by["image-public"].status, "hand")
        self.assertEqual(by["image-public"].owner, "developer")
        hand = "\n".join(by["image-public"].hand)
        self.assertIn("https://github.com/organizations/wow-two-sdk-beta/settings/packages", hand)
        self.assertIn("https://github.com/orgs/wow-two-sdk-beta/packages/container/"
                      "wow-two-sdk-beta.identity%2Fidentity/settings", hand)
        by, steps = plan(registered(image_public=None))
        self.assertEqual(by["image-public"].status, "unknown")
        self.assertIn("[check] image-public", library.render_next(lib(), steps))

    def test_image_public_waits_for_the_image_and_never_gates_deploy(self):
        by, _ = plan(pushed())  # no release yet: the probe did not run
        self.assertEqual(by["image"].status, "waiting")
        self.assertEqual(by["image-public"].status, "pending")
        self.assertNotIn("image-public", by["deploy"].needs)
        by, _ = plan(registered(image_public=False))
        self.assertEqual(by["deploy"].status, "next")  # a private image does not hold the Wheelhouse flip

    def test_occupied_folder_blocks_creation(self):
        by, steps = plan(fresh(folder="foreign", origin=None))
        self.assertEqual(by["create"].status, "blocked")
        self.assertEqual(library.next_phase(steps), (None, []))

    def test_identity_mismatch_blocks_the_commit(self):
        by, _ = plan(scaffolded(author="SRakhimov@EBSCO.COM"))
        self.assertEqual(by["author"].status, "blocked")
        self.assertEqual(by["commit"].status, "pending")

    def test_flags_off_hand_the_directive_to_the_developer(self):
        by, steps = plan(fresh(flags={"commit": True, "push": False, "source": "default"}))
        self.assertEqual(by["flags"].status, "hand")
        self.assertEqual(by["create"].status, "pending")
        self.assertIn("~git_on push workbench/wow-two-sdk-beta/*", library.render_next(lib(), steps))

    def test_hub_flags_off_hand_the_hub_commit(self):
        by, _ = plan(pushed(hub_flags={"commit": False, "push": False, "source": "default"}))
        self.assertEqual(by["hub-commit"].owner, "developer")
        self.assertEqual(by["hub-commit"].status, "pending")  # after the catalog entry the agent writes

    def test_unknown_probes_do_not_advance(self):
        by, steps = plan(fresh(repo_exists=None))
        self.assertEqual(by["create"].status, "unknown")
        self.assertEqual(by["clone"].status, "pending")


class CommandForms(unittest.TestCase):
    """Every printed write keeps the guard's forms: named gh account, plain named-remote pushes, no banned verb."""

    STATES = (fresh, created, cloned, scaffolded, pushed, registered)

    def every_command(self):
        for make in self.STATES:
            for confirmed in ([], ["nuget-policy"]):
                _, steps = plan(make(), confirmed=confirmed)
                for step in steps:
                    yield from step.commands

    def test_gh_names_the_account(self):
        for command in self.every_command():
            if re.search(r"(^|\s)gh\s", command):
                self.assertTrue(command.startswith(GH), command)

    def test_pushes_are_plain_and_named(self):
        for command in self.every_command():
            if " push" in command and command.startswith("git "):
                self.assertRegex(command, r"^git -C \S+ push origin main$")

    def test_no_banned_operation(self):
        banned = ("remote add", "git config", "--force", "push -f", "--source", "--push", "reset --hard", "tag ",
                  "repo delete", "auth login", "auth switch", "npm publish")
        for command in self.every_command():
            for fragment in banned:
                self.assertNotIn(fragment, command)

    def test_commit_subject_suits_the_ordinary_form(self):
        for command in self.every_command():
            if " commit -m " in command:
                self.assertNotIn("$", command)  # the guard's ordinary form refuses a shell expansion
                subject = command.split(" commit -m ", 1)[1].strip("'")
                self.assertRegex(subject, r"^(feat|docs|chore): [a-z]")
                self.assertLessEqual(len(subject), 72)


class Probes(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def fake_clone(self, path, url):
        (path / ".git").mkdir(parents=True)
        (path / ".git" / "config").write_text(f'[core]\n\tbare = false\n[remote "origin"]\n\turl = {url}\n'
                                              '\tfetch = +refs/heads/*:refs/remotes/origin/*\n')

    def test_folder_states(self):
        full = "wow-two-sdk-beta/wow-two-sdk-beta.identity"
        repo = self.tmp / "repo"
        self.assertEqual(library.folder_state(repo, full), ("missing", None))
        repo.mkdir()
        self.assertEqual(library.folder_state(repo, full), ("empty", None))
        self.fake_clone(repo, f"https://github.com/{full}.git")
        self.assertEqual(library.folder_state(repo, full), ("empty-clone", full))
        (repo / "README.md").write_text("x")
        self.assertEqual(library.folder_state(repo, full), ("clone", full))
        other = self.tmp / "other"
        self.fake_clone(other, "git@github.com:someone/else.git")
        self.assertEqual(library.folder_state(other, full), ("foreign", "someone/else"))

    def test_parse_flags(self):
        text = ("GIT FLAGS for workbench/wow-two-sdk-beta/* (each repository under it without its own override): "
                "commit ON (folder workbench/wow-two-sdk-beta/*) · push OFF (default). Own overrides under it: x.")
        self.assertEqual(library.parse_flags(text),
                         {"commit": True, "push": False, "source": "folder workbench/wow-two-sdk-beta/*"})
        self.assertIsNone(library.parse_flags("Cannot inspect repository flags: nope"))

    def test_image_path_is_lowercase_owner_repo_product(self):
        self.assertEqual(lib().image_path, "wow-two-sdk-beta/wow-two-sdk-beta.identity/identity")
        self.assertEqual(lib(product="ident").image_path, "wow-two-sdk-beta/wow-two-sdk-beta.identity/ident")

    def test_anonymous_pull_probe_reads_the_status_only(self):
        probe = library.Probe(lib())
        image = lib().image_path
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        with mock.patch.object(library.urllib.request, "urlopen", return_value=response) as opened:
            self.assertIs(probe.anonymous_pull(image), True)
        request = opened.call_args[0][0]
        self.assertEqual(request.full_url, f"https://ghcr.io/token?scope=repository:{image}:pull")
        self.assertFalse([h for h in request.headers if h.lower() in ("authorization", "cookie")])
        response.read.assert_not_called()  # the token in the body is never read
        for code, expected in ((401, False), (403, False), (404, None), (429, None), (500, None)):
            error = urllib.error.HTTPError(request.full_url, code, "x", {}, None)
            with mock.patch.object(library.urllib.request, "urlopen", side_effect=error):
                self.assertIs(probe.anonymous_pull(image), expected, code)
        for failure in (urllib.error.URLError("down"), TimeoutError()):
            with mock.patch.object(library.urllib.request, "urlopen", side_effect=failure):
                self.assertIsNone(probe.anonymous_pull(image))
        response.status = 204
        with mock.patch.object(library.urllib.request, "urlopen", return_value=response):
            self.assertIsNone(probe.anonymous_pull(image))

    def test_anonymous_pull_probe_stays_off_the_network_when_offline(self):
        with mock.patch.object(library.urllib.request, "urlopen", side_effect=AssertionError("network")) as opened:
            self.assertIsNone(library.Probe(lib(), offline=True).anonymous_pull(lib().image_path))
        opened.assert_not_called()

    def test_placeholders_and_sample(self):
        target = lib(root=self.tmp)
        (target.path / "product").mkdir(parents=True)
        (target.path / "README.md").write_text("# x\n\n{{PLACEHOLDER}}\n\n{{ONE_LINE_WHAT_THIS_IS}}\n")
        (target.path / "product" / "product.md").write_text("{{product}} stays: a section template\n")
        found = library.placeholders_in(target.path)
        self.assertEqual(sorted(found), [("README.md", "{{ONE_LINE_WHAT_THIS_IS}}"), ("README.md", "{{PLACEHOLDER}}")])
        greetings = target.backend / "packages" / "Abstractions" / "Greetings"
        greetings.mkdir(parents=True)
        self.assertTrue(library.has_sample(target))
        greetings.rmdir()
        self.assertFalse(library.has_sample(target))

    def test_entry_block_and_platform_row(self):
        text = "entries:\n  - slug: identity\n    deploy: none\n    status: \"Planned\"\n  - slug: other\n"
        self.assertEqual(library.block_field(library.entry_block(text, "identity"), "deploy"), "none")
        self.assertEqual(library.entry_block(text, "missing"), "")
        row = "| 2 | **Identity** | `wow-two-sdk-beta.identity` | spec |"
        self.assertEqual(library.platform_row(row, "Identity", "wow-two-sdk-beta.identity"), "named")
        self.assertEqual(library.platform_row(row, "Identity", "wow-two-sdk-beta.auth"), "unnamed")
        self.assertEqual(library.platform_row(row, "ExampleLib", "wow-two-sdk-beta.example-lib"), "none")

    def test_versions_sort_releases_above_prereleases(self):
        self.assertEqual(library.newest(["10.0.9-beta", "10.0.10-beta", "10.0.2-beta"]), "10.0.10-beta")
        self.assertEqual(library.newest(["0.0.9", "0.0.12"]), "0.0.12")

    def test_inputs_default_from_the_repo_name(self):
        example = library.Library("wow-two-sdk-beta.example-lib")
        self.assertEqual((example.brand, example.slug, example.product), ("ExampleLib", "example-lib", "examplelib"))
        self.assertEqual(example.fe_package, "@wow-two-beta/fe-example-lib")
        self.assertEqual(example.problems(), [])
        self.assertTrue(library.Library("identity", "identity").problems())


CATALOG = """catalog: 1
entries:
  # wow-two-sdk-beta (beta SDK packages)
  - slug: wow-two-sdk-beta-be
    name: wow-two-sdk-beta.be
    workspace: wow2-backbone
    kind: sdk
    deploy: none
    status: "Active (beta)"
    purpose: "be sdk"
    repositories: [wow-two-sdk-beta/wow-two-sdk-beta.be]

  # wow-two-kb (knowledge base)
  - slug: wow-two-kb-welcome
    name: wow-two-kb.welcome
    workspace: wow2-backbone
    kind: kb
    deploy: none
    status: "Stub"
    purpose: "Welcome"
    repositories: [wow-two-kb/wow-two-kb.welcome]
"""


class LocalWrites(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "scripts").mkdir()
        shutil.copy(library.ROOT / library.REGISTRY_GEN, self.tmp / library.REGISTRY_GEN)
        (self.tmp / "catalog.yml").write_text(CATALOG)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_catalog_entry_lands_in_its_org_group_and_parses(self):
        target = lib(root=self.tmp)
        text = library.insert_entry(CATALOG, target, library.entry_text(target, 'Own store; "OIDC" provider'))
        group = text.split("  # wow-two-kb")[0]
        self.assertIn("  - slug: identity\n    name: Identity\n", group)
        self.assertIn('purpose: "Own store; \\"OIDC\\" provider"', group)
        entry = library.check_catalog(target, text)
        self.assertEqual(entry["repositories"], ["wow-two-sdk-beta/wow-two-sdk-beta.identity"])
        with self.assertRaises(ValueError):
            library.insert_entry(text, target, library.entry_text(target, "again"))
        with self.assertRaises(ValueError):
            library.entry_text(target, "<one line: what the domain does>")

    def test_apply_local_writes_then_stays_idempotent(self):
        args = ["--brand", "Identity", "--root", str(self.tmp)]
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(library.main(["apply-local", "catalog", "wow-two-sdk-beta.identity", *args,
                                           "--purpose", "Own user store"]), 0)
            self.assertEqual(library.main(["apply-local", "catalog", "wow-two-sdk-beta.identity", *args,
                                           "--purpose", "Own user store"]), 0)
            self.assertEqual(library.main(["apply-local", "deploy", "wow-two-sdk-beta.identity", *args]), 0)
        text = (self.tmp / "catalog.yml").read_text()
        self.assertEqual(text.count("- slug: identity"), 1)
        self.assertEqual(library.block_field(library.entry_block(text, "identity"), "deploy"), "wheelhouse")
        self.assertEqual(library.block_field(library.entry_block(text, "wow-two-sdk-beta-be"), "deploy"), "none")
        self.assertIn("nothing written", out.getvalue())

    def test_repin_rewrites_property_literal_and_npm_pins(self):
        repo = self.tmp / "workbench" / "wow-two-platform" / "consumer"
        (repo / ".git").mkdir(parents=True)
        (repo / "Directory.Packages.props").write_text(
            "<Project>\n  <PropertyGroup><IdentitySdkVersion>10.0.0-beta</IdentitySdkVersion></PropertyGroup>\n"
            '  <ItemGroup><PackageVersion Include="WoW2.Sdk.Beta.Be.Identity.Client" Version="10.0.0-beta" />\n'
            '  <PackageVersion Include="WoW2.Sdk.Beta.Be.Identity.Module" Version="$(IdentitySdkVersion)" />'
            "</ItemGroup>\n</Project>\n")
        (repo / "package.json").write_text('{"dependencies": {"@wow-two-beta/fe-identity": "^0.0.2"}}\n')
        own = lib(root=self.tmp).path
        own.mkdir(parents=True)
        (own / "package.json").write_text('{"dependencies": {"@wow-two-beta/fe-identity": "workspace:*"}}\n')
        target = lib(root=self.tmp)
        pins = library.find_consumers(target)
        self.assertEqual(sorted(p.kind for p in pins), ["npm", "package", "property"])
        with redirect_stdout(io.StringIO()):
            changed = library.repin(target, "10.0.1-beta", "0.0.3", "workbench/wow-two-platform/consumer", True)
        self.assertEqual(len(changed), 2)
        props = (repo / "Directory.Packages.props").read_text()
        self.assertIn("<IdentitySdkVersion>10.0.1-beta</IdentitySdkVersion>", props)
        self.assertIn('Include="WoW2.Sdk.Beta.Be.Identity.Client" Version="10.0.1-beta"', props)
        self.assertIn('Version="$(IdentitySdkVersion)"', props)
        self.assertIn('"@wow-two-beta/fe-identity": "^0.0.3"', (repo / "package.json").read_text())


if __name__ == "__main__":
    unittest.main()
