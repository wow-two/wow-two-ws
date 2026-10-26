"""Claude Code side of the workspace git flags, run against a throwaway workspace; nothing commits for real.

The hooks are copied into a temporary `<workspace>/.claude/hooks` layout, so the flag module resolves
that workspace as its root and the flag store lives in its temporary `.claude/`.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import uuid

HOOKS = Path(__file__).resolve().parents[1]
WORKSPACE = HOOKS.parents[1]


def installed_guard():
    """The workspace's own guard, loaded for its CONFIG block; one test file serves every workspace."""
    spec = importlib.util.spec_from_file_location("installed_guard", HOOKS / "guard-git.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GUARD = installed_guard()


class SwitchHarness(unittest.TestCase):
    """A throwaway workspace with the hooks installed and one product repository."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="claude-commit-switch-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / ".claude/hooks").mkdir(parents=True)
        for name in ("guard-git.py", "commit-switch.py"):
            shutil.copy(HOOKS / name, self.root / ".claude/hooks" / name)
        shutil.copy(WORKSPACE / ".claude/hooks/commit_permission.py", self.root / ".claude/hooks/commit_permission.py")
        self.repo = self.root / "workbench/product"
        subprocess.run(["git", "init", "--quiet", "--initial-branch=main", str(self.repo)], check=True)
        self.commit = 'git -C {} commit -m "feat: added a thing"'.format(self.repo)

    def hook(self, script, payload):
        return subprocess.run(["python3", "-B", str(self.root / ".claude/hooks" / script)],
                              input=json.dumps(payload), capture_output=True, text=True)

    def say(self, prompt, session="chat-a"):
        result = self.hook("commit-switch.py", {"hook_event_name": "UserPromptSubmit", "session_id": session,
                                                "prompt": prompt, "cwd": str(self.root)})
        self.assertEqual(0, result.returncode, result.stderr)
        return result.stdout

    def guard(self, command, session="chat-a"):
        return self.hook("guard-git.py", {"tool_name": "Bash", "tool_input": {"command": command},
                                          "session_id": session, "tool_use_id": "toolu_1", "cwd": str(self.root)})

    def edit(self, tool, path):
        key = "notebook_path" if tool == "NotebookEdit" else "file_path"
        return self.hook("guard-git.py", {"tool_name": tool, "tool_input": {key: str(path)},
                                          "session_id": "chat-a", "cwd": str(self.root)})

    def git(self, repo, *args):
        return subprocess.run(["git", "-C", str(repo), "-c", "user.email=t@example.invalid", "-c", "user.name=T",
                               "-c", "commit.gpgsign=false", *args], check=True, capture_output=True, text=True)

    def history(self, repo):
        """`main` with one commit, `feature` checked out with two more."""
        for branch, names in (("main", ["base"]), ("feature", ["one", "two"])):
            if branch == "feature":
                self.git(repo, "checkout", "--quiet", "-b", "feature")
            for name in names:
                (repo / (name + ".txt")).write_text(name + "\n")
                self.git(repo, "add", name + ".txt")
                self.git(repo, "commit", "--quiet", "-m", name)


class CommitSwitchTests(SwitchHarness):
    def test_off_by_default_and_only_an_exact_directive_turns_it_on(self):
        self.assertEqual(2, self.guard(self.commit).returncode)
        self.assertEqual("", self.say("please ~commit_on workbench/product"))
        self.assertEqual(2, self.guard(self.commit).returncode)
        self.assertIn("ON for", self.say("~commit_on workbench/product"))
        self.assertEqual(0, self.guard(self.commit).returncode)

    def test_the_flag_applies_to_every_chat_until_off(self):
        self.say("~commit_on workbench/product")
        self.assertEqual(0, self.guard(self.commit, session="chat-b").returncode)
        self.say("~commit_off workbench/product", session="chat-b")
        self.assertEqual(2, self.guard(self.commit).returncode)

    def test_the_workspace_default_reaches_every_repository(self):
        other = self.root / "workbench/later"
        self.assertIn("ON by default", self.say("~commit_on *"))
        subprocess.run(["git", "init", "--quiet", str(other)], check=True)
        self.assertEqual(0, self.guard(self.commit).returncode)
        self.assertEqual(0, self.guard('git -C {} commit -m "feat: added"'.format(other)).returncode)
        self.say("~commit_off workbench/later")
        self.assertEqual(2, self.guard('git -C {} commit -m "feat: added"'.format(other)).returncode)
        self.assertIn("workbench/later: commit OFF", self.say("~git_status *"))

    def test_only_the_ordinary_form_passes_while_on(self):
        self.say("~commit_on workbench/product")
        for command in ["git -C {} commit -am x".format(self.repo),
                        self.commit + " && git push",
                        "git -C {} push --force".format(self.repo),
                        "git -C {} push origin +main".format(self.repo),
                        "git -C {} push --delete origin main".format(self.repo),
                        "git -C {} push origin main && echo done".format(self.repo)]:
            with self.subTest(command=command):
                self.assertEqual(2, self.guard(command).returncode)

    def test_an_ordinary_push_follows_the_push_flag(self):
        push = "git -C {} push origin main".format(self.repo)
        self.git(self.repo, "remote", "add", "origin", "https://github.com/owner/product.git")
        self.say("~commit_on workbench/product")
        blocked = self.guard(push)
        self.assertEqual(2, blocked.returncode)
        self.assertIn("PUSH PERMISSION: OFF", blocked.stderr)
        self.assertIn("PUSH PERMISSION: ON", self.say("~push_on workbench/product"))
        self.assertEqual(0, self.guard(push).returncode)
        self.assertEqual(0, self.guard("git -C {} push -u origin feature/x".format(self.repo), "chat-b").returncode)
        self.say("~push_off workbench/product", session="chat-b")
        self.assertEqual(2, self.guard(push).returncode)
        self.assertEqual(0, self.guard(self.commit).returncode)

    def test_the_push_flag_never_permits_a_commit(self):
        self.say("~push_on workbench/product")
        self.assertEqual(2, self.guard(self.commit).returncode)
        self.assertEqual(0, self.guard("git -C {} push".format(self.repo)).returncode)

    def test_session_start_shows_the_working_repository_flags(self):
        self.say("~push_on workbench/product")
        result = self.hook("commit-switch.py", {"hook_event_name": "SessionStart", "session_id": "chat-c",
                                                "cwd": str(self.repo)})
        self.assertIn("commit OFF (default) · push ON (override)", result.stdout)

    def test_a_retired_kind_changes_nothing(self):
        self.assertIn("merged into `commit`", self.say("~git_on history workbench/product"))
        self.assertEqual(2, self.guard(self.commit).returncode)

    def test_a_broken_switch_never_permits_a_commit(self):
        self.say("~commit_on workbench/product")
        (self.root / ".claude/hooks/commit_permission.py").write_text("def broken(:\n")
        result = self.guard(self.commit)
        self.assertEqual(2, result.returncode)
        self.assertIn("commit switch failed", result.stderr)
        self.assertEqual(0, self.guard("git status").returncode)


@unittest.skipIf(GUARD.STRICT, "a STRICT workspace forbids every gated category; StrictTests cover it")
class GitFlagTests(SwitchHarness):
    """History rewrites follow `commit`, gh writes follow `push`; rarely needed risky commands never run."""

    def setUp(self):
        super().setUp()
        self.other = self.root / "workbench/other"
        subprocess.run(["git", "init", "--quiet", "--initial-branch=main", str(self.other)], check=True)
        for repo in (self.repo, self.other):
            self.history(repo)
        self.rebase = "git -C {} rebase main".format(self.repo)

    def test_a_history_rewrite_follows_the_commit_flag(self):
        blocked = self.guard(self.rebase)
        self.assertEqual(2, blocked.returncode)
        self.assertIn("git flag `commit`", blocked.stderr)
        self.say("~git_on commit workbench/product")
        for command in [self.rebase, "git -C {} commit --amend --no-edit".format(self.repo),
                        "git -C {} reset --soft HEAD~1".format(self.repo), "git -C {} reset".format(self.repo),
                        "git -C {} rebase main --exec 'git commit --amend --no-edit'".format(self.repo),
                        "git -C {} rebase --continue".format(self.repo),
                        "git -C {} cherry-pick main".format(self.repo), "git -C {} merge main".format(self.repo)]:
            with self.subTest(command=command):
                self.assertEqual(0, self.guard(command, session="chat-b").returncode)
        self.assertEqual(2, self.guard("git -C {} rebase main".format(self.other)).returncode)
        self.say("~git_off commit workbench/product")
        self.assertEqual(2, self.guard(self.rebase).returncode)

    def test_a_rewrite_never_replaces_a_pushed_commit(self):
        remote = self.root / "remote.git"
        subprocess.run(["git", "init", "--quiet", "--bare", str(remote)], check=True)
        self.git(self.repo, "remote", "add", "origin", str(remote))
        self.git(self.repo, "push", "--quiet", "origin", "main", "feature")
        self.say("~git_on commit workbench/product")
        for command in ["git -C {} commit --amend --no-edit".format(self.repo), self.rebase,
                        "git -C {} reset --soft HEAD~1".format(self.repo),
                        "git -C {} rebase --root".format(self.repo),
                        "git -C {} rebase -i HEAD~2".format(self.repo)]:
            with self.subTest(command=command):
                blocked = self.guard(command)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("remote-tracking branch", blocked.stderr)
        for command in ["git -C {} revert --no-edit HEAD".format(self.repo), "git -C {} merge main".format(self.repo),
                        "git -C {} reset".format(self.repo)]:
            with self.subTest(command=command):
                self.assertEqual(0, self.guard(command).returncode)
        (self.repo / "three.txt").write_text("three\n")
        self.git(self.repo, "add", "three.txt")
        self.git(self.repo, "commit", "--quiet", "-m", "three")
        self.assertEqual(0, self.guard("git -C {} commit --amend --no-edit".format(self.repo)).returncode)
        self.assertEqual(0, self.guard("git -C {} rebase origin/feature".format(self.repo)).returncode)
        self.assertEqual(2, self.guard("git -C {} reset --soft HEAD~2".format(self.repo)).returncode)

    def test_an_unclear_rewrite_range_blocks(self):
        self.say("~git_on commit workbench/product")
        for command in ["git -C {} rebase missing-branch".format(self.repo),
                        "git -C {} rebase main feature extra".format(self.repo)]:
            with self.subTest(command=command):
                blocked = self.guard(command)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("cannot tell which commits", blocked.stderr)

    def test_one_directive_names_several_kinds_and_repositories(self):
        self.say("~git_on commit,push workbench/product workbench/other")
        for repo in (self.repo, self.other):
            with self.subTest(repo=repo):
                self.git(repo, "remote", "add", "origin", "https://github.com/owner/{}.git".format(repo.name))
                self.assertEqual(0, self.guard("git -C {} rebase main".format(repo)).returncode)
                self.assertEqual(0, self.guard("git -C {} push origin main".format(repo)).returncode)
                self.assertEqual(0, self.guard("git -C {} commit -m \"x: y\"".format(repo)).returncode)

    def test_all_never_enables_and_off_all_clears_every_flag(self):
        self.assertEqual("", self.say("~git_on all workbench/product"))
        self.assertEqual(2, self.guard(self.rebase).returncode)
        self.say("~git_on commit,push workbench/product")
        self.say("~git_off all workbench/product")
        for command in [self.commit, self.rebase, "git -C {} push".format(self.repo)]:
            with self.subTest(command=command):
                self.assertEqual(2, self.guard(command).returncode)

    def test_only_a_whole_message_directive_changes_a_flag(self):
        for prompt in ["please ~git_on commit workbench/product", "~git_on commit workbench/product\nthanks",
                       "```\n~git_on commit workbench/product\n```", "~git_on commit",
                       "~git_on commit,commit workbench/product", "~git_on rewrite workbench/product",
                       "~git_on config workbench/product", "~git_on force workbench/product"]:
            with self.subTest(prompt=prompt):
                self.assertEqual("", self.say(prompt))
                self.assertEqual(2, self.guard(self.rebase).returncode)

    def test_a_hidden_repository_blocks_a_gated_command(self):
        self.say("~git_on commit workbench/product")
        for command in ["cd {} && git rebase main".format(self.repo),
                        "git --git-dir={}/.git rebase main".format(self.repo)]:
            with self.subTest(command=command):
                blocked = self.guard(command)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("git -C <repo>", blocked.stderr)

    def test_safe_commands_run_without_a_flag(self):
        for command in ["git -C {} mv a.txt b.txt", "git -C {} rm old.txt", "git -C {} apply fix.patch",
                        "git -C {} submodule update --init", "git -C {} notes add -m note HEAD",
                        "git -C {} config --get user.email", "git -C {} pull", "git -C {} stash"]:
            with self.subTest(command=command):
                self.assertEqual(0, self.guard(command.format(self.repo)).returncode)

    def test_rare_risky_commands_never_run_whatever_the_flags(self):
        self.say("~git_on commit,push workbench/product")
        for command in ["git -C {} restore file.txt", "git -C {} checkout -- file.txt", "git -C {} reset --hard",
                        "git -C {} clean -fd", "git -C {} rm -f old.txt", "git -C {} mv -f a.txt b.txt",
                        "git -C {} apply -R changes.patch",
                        "git -C {} switch --discard-changes main", "git -C {} push --force-with-lease origin main",
                        "git -C {} push origin :old-branch", "git -C {} push --mirror",
                        "git -C {} config user.email a@b.c", "git -C {} config --global user.email a@b.c",
                        "git -C {} remote add upstream https://example.invalid/x.git",
                        "git -C {} worktree add ../other", "git -C {} submodule add https://example.invalid/x.git",
                        "git -C {} filter-repo --path x", "git -C {} update-ref -d refs/heads/x",
                        "git -C {} reflog expire --all", "git -C {} gc --prune=now", "git -C {} send-email x.patch",
                        "gh repo delete owner/product --yes"]:
            with self.subTest(command=command):
                blocked = self.guard(command.format(self.repo))
                self.assertEqual(2, blocked.returncode)
                self.assertIn("no flag permits it", blocked.stderr)

    def test_a_gh_write_reads_the_push_flag_of_the_repository_with_that_origin(self):
        self.git(self.repo, "remote", "add", "origin", "https://github.com/Owner/product.git")
        create = "gh pr create -R owner/product --title t --body b"
        blocked = self.guard(create)
        self.assertEqual(2, blocked.returncode)
        self.assertIn("git flag `push`", blocked.stderr)
        self.say("~git_on push workbench/product")
        for command in [create, "gh api -X POST repos/owner/product/dispatches -f event_type=x",
                        "gh repo edit owner/product --visibility private"]:
            with self.subTest(command=command):
                self.assertEqual(0, self.guard(command).returncode)
        self.assertEqual(2, self.guard("gh pr create -R owner/elsewhere --title t --body b").returncode)
        self.assertEqual(0, self.guard("gh pr list -R owner/elsewhere").returncode)

    def test_nested_workspace_repositories_keep_independent_push_flags(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        workspace = self.root / "workbench/ocharo-hq/ocharo-ws"
        nested = workspace / "workbench/ocharo-platform"
        deeper = nested / "workbench/independent"
        for path, slug in ((workspace, "ocharo-ws"), (nested, "ocharo-platform"), (deeper, "independent")):
            subprocess.run(["git", "init", "--quiet", str(path)], check=True)
            self.git(path, "remote", "add", "origin", "git@github.com:ocharo-hq/{}.git".format(slug))
        self.say("~git_on push .")
        for slug in ("ocharo-ws", "ocharo-platform", "independent"):
            with self.subTest(slug=slug):
                self.assertEqual(2, self.guard("gh repo edit ocharo-hq/{} --description test".format(slug)).returncode)
        self.say("~git_off push .")
        self.say("~git_on push workbench/ocharo-hq/ocharo-ws/workbench/ocharo-platform")
        self.assertEqual(0, self.guard("gh repo edit ocharo-hq/ocharo-platform --description test").returncode)
        self.assertEqual(2, self.guard("gh repo edit ocharo-hq/independent --description test").returncode)

    def test_discovery_ignores_dependency_trees_and_symlinks(self):
        spec = importlib.util.spec_from_file_location("fixture_guard", self.root / ".claude/hooks/guard-git.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for excluded in ("node_modules", "vendor", ".git"):
            fake = self.root / "workbench/group" / excluded / "unmanaged/.git"
            fake.mkdir(parents=True)
            (fake / "config").write_text("[remote \"origin\"]\n url = https://github.com/owner/{}\n".format(excluded))
            self.assertIsNone(module.local_repository("owner/" + excluded))
        with tempfile.TemporaryDirectory(prefix="external-repository-") as outside:
            external = Path(outside)
            (external / ".git").mkdir()
            (external / ".git/config").write_text("[remote \"origin\"]\n url = https://github.com/owner/external\n")
            (self.root / "workbench/external-link").symlink_to(external, target_is_directory=True)
            self.assertIsNone(module.local_repository("owner/external"))
        hidden = self.repo / "src/not-managed/.git"
        hidden.mkdir(parents=True)
        (hidden / "config").write_text("[remote \"origin\"]\n url = https://github.com/owner/implementation\n")
        self.assertIsNone(module.local_repository("owner/implementation"))

    def test_checkout_paths_without_separator_cannot_discard_work(self):
        self.git(self.repo, "branch", "fixture-main")
        (self.repo / "one.txt").write_text("uncommitted\n")
        for suffix in ("HEAD one.txt", "one.txt", "*.txt", "-p one.txt", "--patch one.txt",
                       "--pathspec-from-file=paths.txt", "HEAD missing.txt"):
            with self.subTest(suffix=suffix):
                self.assertEqual(2, self.guard("git -C {} checkout {}".format(self.repo, suffix)).returncode)
        for suffix in ("fixture-main", "-", "-b feature2 fixture-main", "--detach HEAD"):
            with self.subTest(suffix=suffix):
                self.assertEqual(0, self.guard("git -C {} checkout {}".format(self.repo, suffix)).returncode)
        self.assertEqual("uncommitted\n", (self.repo / "one.txt").read_text())

    def test_modern_config_commands_distinguish_reads_from_writes(self):
        self.say("~git_on commit,push workbench/product")
        for suffix in ("edit", "--local edit", "set user.name Someone", "unset user.name",
                       "rename-section old new", "remove-section user"):
            with self.subTest(suffix=suffix):
                self.assertEqual(2, self.guard("git -C {} config {}".format(self.repo, suffix)).returncode)
        for suffix in ("list", "get user.name", "--local get user.name", "--get user.name", "user.name"):
            with self.subTest(suffix=suffix):
                self.assertEqual(0, self.guard("git -C {} config {}".format(self.repo, suffix)).returncode)

    def test_repository_delete_api_is_never_unlocked_by_push(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        self.say("~git_on push .")
        self.git(self.repo, "remote", "add", "origin", "https://github.com/owner/product.git")
        self.say("~git_on push workbench/product")
        for endpoint in ("repos/owner/product", "/repos/owner/product/", "repos/owner/product?x=1",
                         "https://api.github.com/repos/owner/product"):
            with self.subTest(endpoint=endpoint):
                self.assertEqual(2, self.guard("gh api -X DELETE " + endpoint).returncode)
        self.assertEqual(0, self.guard("gh api -X DELETE repos/owner/product/issues/comments/1").returncode)
        self.say("~git_off push workbench/product")
        self.assertEqual(2, self.guard("gh api -X DELETE repos/owner/product/issues/comments/1").returncode)
        self.assertEqual(0, self.guard("gh api repos/owner/product").returncode)

    def test_repo_creation_cannot_smuggle_remote_configuration_or_push(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        (self.root / "workbench/wow-two-sdk-beta").mkdir(parents=True)
        self.say("~git_on push . workbench/product workbench/wow-two-sdk-beta/*")
        for suffix in ("--source .", "--source=. --push", "--push", "--remote origin", "--remote=origin",
                       "-s .", "-s.", "-r origin", "-rorigin", "-cr origin"):
            with self.subTest(suffix=suffix):
                blocked = self.guard("gh repo create wow-two-sdk-beta/new --private " + suffix)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("no flag permits it", blocked.stderr)
        self.assertEqual(0, self.guard("gh repo create wow-two-sdk-beta/new --private").returncode)
        self.say("~git_off push workbench/wow-two-sdk-beta/*")
        self.assertEqual(2, self.guard("gh repo create wow-two-sdk-beta/new --private").returncode)

    def test_a_gh_write_to_a_repository_not_checked_out_reads_off(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        self.say("~git_on push * .")
        for command in ["gh repo edit wow-two-apps/not-cloned --visibility public",
                        "gh pr create -R owner/elsewhere --title t --body b",
                        "gh api -X PATCH repos/owner/elsewhere -f private=false",
                        "gh secret set TOKEN -R owner/elsewhere --body value",
                        "gh workflow run deploy.yml --repo=owner/elsewhere"]:
            with self.subTest(command=command):
                blocked = self.guard(command)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("git flag `push`", blocked.stderr)
                self.assertIn("matches no repository", blocked.stderr)
        blocked = self.guard("GH_REPO=owner/elsewhere gh repo edit --visibility public")
        self.assertEqual(2, blocked.returncode)
        self.assertIn("GH_REPO", blocked.stderr)
        # the working repository and gh's `{owner}/{repo}` placeholders still read the working repository
        for command in ["gh repo edit --description x", "gh api -X POST repos/{owner}/{repo}/dispatches -f event_type=x"]:
            with self.subTest(command=command):
                self.assertEqual(0, self.guard(command).returncode)

    def test_repository_creation_reads_the_flag_of_its_future_checkout_folder(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        (self.root / "workbench/wow-two-sdk-beta").mkdir(parents=True)
        self.say("~git_on push .")
        creations = ["gh repo create wow-two-sdk-beta/new-lib --public --disable-wiki -d 'A library'",
                     "gh repo create --public wow-two-sdk-beta/new-lib",
                     "gh api -X POST orgs/wow-two-sdk-beta/repos -f name=new-lib -F private=false",
                     "gh api orgs/wow-two-sdk-beta/repos --raw-field=name=new-lib",
                     "gh api --method POST /orgs/wow-two-sdk-beta/repos -fname=new-lib"]
        for command in creations:
            with self.subTest(command=command):
                blocked = self.guard(command)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("workbench/wow-two-sdk-beta/new-lib", blocked.stderr)
        self.say("~git_on push workbench/wow-two-sdk-beta/*")
        for command in creations:
            with self.subTest(command=command):
                self.assertEqual(0, self.guard(command).returncode)
        self.assertEqual(2, self.guard("gh repo create wow-two-apps/new-app --private").returncode)
        self.say("~git_off push workbench/wow-two-sdk-beta/*")
        self.assertEqual(2, self.guard(creations[0]).returncode)

    def test_creation_without_one_checkout_folder_reads_off(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        (self.root / "workbench/wow-two-sdk-beta/taken").mkdir(parents=True)
        (self.root / "workbench/wow-two-sdk-beta/taken/notes.md").write_text("x\n")
        self.say("~git_on push * .")
        self.assertEqual(0, self.guard("gh repo create wow-two-sdk-beta/fresh --public").returncode)
        for command in ["gh repo create owner/new --private", "gh repo create new-name --private", "gh repo create",
                        "gh repo create wow-two-sdk-beta/taken --public", "gh repo create wow-two-sdk-beta/.. --public",
                        "gh api -X POST user/repos -f name=new", "gh api -X POST orgs/owner/repos -f name=new",
                        "gh api -X POST orgs/wow-two-sdk-beta/repos --input body.json",
                        "gh api -X POST orgs/wow-two-sdk-beta/repos -F name=@name.txt",
                        "gh api -X POST orgs/wow-two-sdk-beta/repos -f private=true",
                        "gh api -X POST orgs/wow-two-sdk-beta/repos -f name=a -f name=b",
                        "gh api -X POST repos/owner/template/generate -f name=new",
                        "gh api -X POST repos/wow-two-sdk-beta/template/forks"]:
            with self.subTest(command=command):
                blocked = self.guard(command)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("git flag `push`", blocked.stderr)
        self.assertEqual(0, self.guard("gh api -X POST repos/owner/template/generate -f owner=wow-two-sdk-beta "
                                       "-f name=fresh").returncode)

    def test_graphql_mutations_read_off_and_queries_read_the_working_repository(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        self.git(self.repo, "remote", "add", "origin", "https://github.com/owner/product.git")
        self.say("~git_on push * . workbench/product")
        mutations = [
            "gh api graphql -f query='mutation { addStar(input: {starrableId: \"x\"}) { clientMutationId } }'",
            "gh api graphql -f query='mutation($id: ID!) { updateRepository(input: {repositoryId: $id}) { clientMutationId } }' -f id=x",
            "gh api graphql --raw-field 'query=query Q { viewer { login } } mutation M { x }'",
            "gh api /graphql -F query=@change.graphql", "gh api graphql --input body.json",
            "gh api graphql -f query=\"$(cat change.graphql)\"", "gh api graphql -f \"query=$DOCUMENT\"",
            "gh api -X POST graphql", "gh api -R owner/product graphql -f query='mutation { x }'",
        ]
        for command in mutations:
            with self.subTest(command=command):
                blocked = self.guard(command)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("graphql", blocked.stderr)
        queries = ["gh api graphql -f query='query { viewer { login } }'",
                   "gh api graphql -f query='query($o: String!) { repository(owner: $o, name: \"n\") { id } }' -f o=x",
                   "gh api graphql -f query='{ viewer { login } }' --jq .data"]
        for command in queries:
            with self.subTest(command=command):
                self.assertEqual(0, self.guard(command).returncode)
        self.say("~git_off push .")
        self.assertEqual(2, self.guard(queries[0]).returncode)

    def test_a_directive_naming_a_folder_without_star_changes_nothing(self):
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        (self.root / "workbench/wow-two-sdk-beta").mkdir(parents=True)
        (self.repo / "src").mkdir()
        for prompt in ["~git_on push workbench/wow-two-sdk-beta", "~git_on push workbench/product/src",
                       "~git_on commit,push workbench/product workbench/wow-two-sdk-beta"]:
            with self.subTest(prompt=prompt):
                self.assertIn("not a repository root", self.say(prompt))
                self.assertIn("commit OFF (default) · push OFF (default)", self.say("~git_status ."))
                self.assertEqual(2, self.guard(self.commit).returncode)
        self.assertIn("ON for", self.say("~git_on push ."))
        self.assertIn("workbench/wow-two-sdk-beta/*", self.say("~git_on push workbench/wow-two-sdk-beta/*"))
        self.assertIn("ON for", self.say("~commit_on workbench/product"))
        self.assertEqual(0, self.guard(self.commit).returncode)

    def test_a_folder_override_reaches_every_repository_under_it(self):
        self.assertIn("workbench/*", self.say("~git_on commit,push workbench/*"))
        later = self.root / "workbench/later"
        subprocess.run(["git", "init", "--quiet", str(later)], check=True)
        for repo in (self.repo, self.other, later):
            with self.subTest(repo=repo):
                self.assertEqual(0, self.guard('git -C {} commit -m "feat: added"'.format(repo)).returncode)
        self.assertEqual(0, self.guard(self.rebase).returncode)
        self.say("~git_off commit workbench/product")
        self.assertEqual(2, self.guard(self.rebase).returncode)
        self.assertEqual(0, self.guard("git -C {} rebase main".format(self.other)).returncode)
        self.assertIn("commit ON (folder workbench/*)", self.say("~git_status workbench/other"))
        self.assertIn("GIT FLAGS for workbench/*", self.say("~git_status workbench/*"))
        self.assertEqual("", self.say("please ~git_on push workbench/*"))

    def test_clone_needs_no_flag(self):
        for command in ["git clone https://github.com/owner/new.git workbench/owner/new",
                        "git -C workbench clone --depth 1 https://github.com/owner/new.git",
                        "gh repo clone owner/new workbench/owner/new",
                        "gh repo clone owner/new workbench/owner/new -- --depth 1"]:
            with self.subTest(command=command):
                self.assertEqual(0, self.guard(command).returncode)
        for command in ["git clone -c core.hooksPath=/tmp/x https://github.com/owner/new.git",
                        "git clone --config=credential.helper=x https://github.com/owner/new.git",
                        "git clone --template=/tmp/t https://github.com/owner/new.git",
                        "git clone -u 'sh -c x' https://github.com/owner/new.git",
                        "git clone --upload-pack=x https://github.com/owner/new.git",
                        "gh repo clone owner/new dir -- --config core.hooksPath=/tmp/x",
                        "gh repo clone owner/new dir -- -c core.hooksPath=/tmp/x"]:
            with self.subTest(command=command):
                blocked = self.guard(command)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("no flag permits it", blocked.stderr)

    def test_an_ordinary_push_names_a_configured_remote(self):
        self.git(self.repo, "remote", "add", "origin", "https://github.com/owner/product.git")
        self.say("~git_on push workbench/product")
        for command in ["push origin main", "push -u origin feature", "push"]:
            with self.subTest(command=command):
                self.assertEqual(0, self.guard("git -C {} {}".format(self.repo, command)).returncode)
        for target in ("https://github.com/owner/elsewhere.git", "git@github.com:owner/elsewhere.git",
                       str(self.other), "../other", "upstream"):
            with self.subTest(target=target):
                blocked = self.guard("git -C {} push -u {} main".format(self.repo, target))
                self.assertEqual(2, blocked.returncode)
                self.assertIn("never a URL or a path", blocked.stderr)

    def test_lfs_preserves_inspection_and_hydration_but_rejects_surgery_and_direct_push(self):
        self.say("~git_on commit,push workbench/product")
        for suffix in ("install", "uninstall", "migrate import --everything", "migrate export --everything",
                       "prune", "push origin main", "push --all origin", "update --force"):
            with self.subTest(suffix=suffix):
                self.assertEqual(2, self.guard("git -C {} lfs {}".format(self.repo, suffix)).returncode)
        for suffix in ("version", "env", "status", "ls-files", "migrate info --everything --above=1MB",
                       "pull", "fetch", "checkout", "track '*.glb'", "untrack '*.glb'", "track"):
            with self.subTest(suffix=suffix):
                self.assertEqual(0, self.guard("git -C {} lfs {}".format(self.repo, suffix)).returncode)

    @unittest.skipUnless(GUARD.LANE_CHECK, "this workspace runs without the lane check")
    def test_a_flagged_history_rewrite_still_meets_the_lane_check(self):
        (self.repo / "one.txt").write_text("changed\n")
        self.say("~git_on commit workbench/product")
        session = "lane-" + uuid.uuid4().hex
        first = self.guard(self.rebase, session=session)
        self.assertEqual(2, first.returncode)
        self.assertIn("lane check", first.stderr)
        self.assertEqual(0, self.guard(self.rebase, session=session).returncode)

    def test_status_lists_every_flag_on_one_line(self):
        self.say("~git_on push workbench/product")
        status = self.say("~git_status workbench/product")
        self.assertIn("GIT FLAGS for", status)
        self.assertIn("commit OFF (default) · push ON (override)", status)


@unittest.skipUnless(GUARD.STRICT, "only a STRICT workspace forbids the gated categories outright")
class StrictTests(SwitchHarness):
    """A STRICT workspace runs only the ordinary commit and push forms; every rewrite and gh write stays human."""

    def test_gated_categories_never_run_whatever_the_flags(self):
        self.history(self.repo)
        self.git(self.repo, "remote", "add", "origin", "https://github.com/owner/product.git")
        self.say("~git_on commit,push workbench/product")
        for command in ["git -C {} rebase main", "git -C {} commit --amend --no-edit", "git -C {} merge main",
                        "git -C {} reset --soft HEAD~1", "gh pr create -R owner/product --title t --body b"]:
            with self.subTest(command=command):
                self.assertEqual(2, self.guard(command.format(self.repo)).returncode)
        self.assertEqual(0, self.guard(self.commit).returncode)
        self.assertEqual(0, self.guard("git -C {} push origin feature".format(self.repo)).returncode)


class StoreGuardTests(SwitchHarness):
    """No tool edits, moves or reads the flag store or its change log."""

    def test_edit_tools_never_touch_the_store_or_its_log(self):
        self.say("~commit_on workbench/product")
        for tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
            for name in ("git-flags.json", "git-flags.log", "git-flags.lock"):
                with self.subTest(tool=tool, name=name):
                    blocked = self.edit(tool, self.root / ".claude" / name)
                    self.assertEqual(2, blocked.returncode)
                    self.assertIn("git flag store", blocked.stderr)
        alias = self.root / "notes.json"
        alias.symlink_to(self.root / ".claude/git-flags.json")
        self.assertEqual(2, self.edit("Write", alias).returncode)
        self.assertEqual(0, self.edit("Write", self.root / "docs/git-flags.md").returncode)
        multi = self.hook("guard-git.py", {"tool_name": "MultiEdit", "session_id": "chat-a", "tool_input": {
            "edits": [{"file_path": str(self.root / "a.md")}, {"file_path": str(self.root / ".claude/git-flags.log")}]}})
        self.assertEqual(2, multi.returncode)

    def test_shell_commands_naming_the_store_block(self):
        for command in ["cat .claude/git-flags.json", "echo '{}' > .claude/git-flags.json",
                        "python3 -c \"open('.claude/git-flags.log','a')\"", "rm .claude/git-flags.lock",
                        "cp /tmp/x .claude/git-flags.json && git status"]:
            with self.subTest(command=command):
                blocked = self.guard(command)
                self.assertEqual(2, blocked.returncode)
                self.assertIn("git flag store", blocked.stderr)
        self.assertEqual(0, self.guard("python3 -B .claude/hooks/commit_permission.py status --repo .").returncode)


if __name__ == "__main__":
    unittest.main()
