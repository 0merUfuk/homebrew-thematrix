#!/usr/bin/env python3
"""Offline updater tests. A local fake gh replaces all GitHub calls."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("update_skuggsja.py")
UPSTREAM = "0merUfuk/skuggsja"


def formula(version, extra=""):
    return 'class Skuggsja < Formula\n  version "' + version + '"\n' + extra + 'end\n'


FAKE_GH = r"""import json
import os
from pathlib import Path
import sys
state = json.loads(Path(os.environ['FAKE_GH_STATE']).read_text())
args = sys.argv[1:]
with open(os.environ['FAKE_GH_LOG'], 'a') as log:
    log.write(json.dumps(args) + '\n')
if args[:2] == ['api', '--include']:
    status = state.get('status', 200)
    release = state.get('release', {})
    print('HTTP/2.0 ' + str(status) + ' Test\r\nContent-Type: application/json\r\n\r\n' + json.dumps(release))
    sys.exit(0 if status == 200 else 1)
if args[:2] == ['release', 'download']:
    if state.get('download_failure'):
        sys.exit(1)
    dest = Path(args[args.index('--dir') + 1]) / 'skuggsja.rb'
    dest.write_text(state['formula'])
    sys.exit(0)
if args[:2] == ['attestation', 'verify']:
    if state.get('attestation_failure'):
        sys.exit(1)
    if state.get('concurrent_content') is not None:
        Path(os.environ['FAKE_FORMULA']).write_text(state['concurrent_content'])
    sys.exit(0)
sys.exit('Unexpected fake gh command')
"""


class UpdateTests(unittest.TestCase):
    def run_case(self, *, current=None, tag="v1.2.3", release=None, downloaded=None,
                 status=200, attestation_failure=False, download_failure=False,
                 symlink=False, concurrent_content=None):
        with tempfile.TemporaryDirectory(prefix="tap-update-test-") as directory:
            base = Path(directory)
            tap = base / "tap"
            scripts = tap / ".github" / "scripts"
            scripts.mkdir(parents=True)
            shutil.copyfile(SCRIPT, scripts / SCRIPT.name)
            formulas = tap / "Formula"
            formulas.mkdir()
            destination = formulas / "skuggsja.rb"
            canary = formulas / "other.rb"
            canary.write_text("other formula must remain unchanged\n")
            if symlink:
                destination.symlink_to(canary)
            elif current is not None:
                destination.write_text(current)
            fake_bin = base / "bin"
            fake_bin.mkdir()
            fake = fake_bin / "gh"
            fake.write_text("#!" + sys.executable + "\n" + FAKE_GH)
            fake.chmod(0o700)
            state = base / "state.json"
            state.write_text(json.dumps({
                "status": status,
                "release": release if release is not None else {
                    "tag_name": tag, "draft": False, "prerelease": False,
                    "assets": [{"name": "skuggsja.rb"}],
                },
                "formula": downloaded if downloaded is not None else formula(tag[1:]),
                "attestation_failure": attestation_failure,
                "download_failure": download_failure,
                "concurrent_content": concurrent_content,
            }))
            log = base / "calls.jsonl"
            output = base / "output"
            env = {**os.environ, "PATH": str(fake_bin) + os.pathsep + os.environ.get("PATH", ""),
                   "FAKE_GH_STATE": str(state), "FAKE_GH_LOG": str(log),
                   "FAKE_FORMULA": str(destination), "GITHUB_OUTPUT": str(output)}
            result = subprocess.run([sys.executable, str(scripts / SCRIPT.name)],
                                    cwd=tap, env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual(canary.read_text(), "other formula must remain unchanged\n")
            self.assertFalse(list(formulas.glob(".skuggsja-*")), "staging file was not cleaned")
            return {
                "exit": result.returncode, "stdout": result.stdout, "stderr": result.stderr,
                "content": destination.read_text() if destination.exists() else None,
                "mode": destination.stat().st_mode & 0o777 if destination.exists() else None,
                "output": output.read_text() if output.exists() else "",
                "calls": [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else [],
            }

    def test_first_release_installs_only_verified_formula(self):
        result = self.run_case()
        self.assertEqual(result["exit"], 0, result["stderr"])
        self.assertEqual(result["content"], formula("1.2.3"))
        self.assertEqual(result["mode"], 0o644)
        self.assertEqual(result["output"], "changed=true\nversion=1.2.3\n")
        calls = result["calls"]
        self.assertEqual([call[:2] for call in calls], [["api", "--include"], ["release", "download"], ["attestation", "verify"]])
        verify = calls[-1]
        self.assertEqual(verify[verify.index("--repo") + 1], UPSTREAM)
        self.assertEqual(verify[verify.index("--signer-workflow") + 1], UPSTREAM + "/.github/workflows/release.yml")
        self.assertEqual(verify[verify.index("--source-ref") + 1], "refs/tags/v1.2.3")
        self.assertIn("--deny-self-hosted-runners", verify)

    def test_missing_first_release_is_the_only_http_noop(self):
        result = self.run_case(status=404)
        self.assertEqual(result["exit"], 0)
        self.assertIsNone(result["content"])
        self.assertEqual(result["output"], "changed=false\n")
        self.assertEqual(len(result["calls"]), 1)

    def test_other_http_failures_are_not_suppressed(self):
        for status in [401, 403, 429, 500]:
            with self.subTest(status=status):
                result = self.run_case(status=status, current=formula("1.0.0"))
                self.assertNotEqual(result["exit"], 0)
                self.assertEqual(result["content"], formula("1.0.0"))

    def test_noncanonical_tags_fail_before_download(self):
        for tag in ["v1.2.3-rc.1", "v01.2.3", "1.2.3", "v1.2.3+build", "v1.2.3;false", "v1.2.3\n"]:
            with self.subTest(tag=tag):
                result = self.run_case(tag=tag)
                self.assertNotEqual(result["exit"], 0)
                self.assertEqual(len(result["calls"]), 1)
                self.assertIsNone(result["content"])

    def test_draft_and_prerelease_fail_before_download(self):
        for key in ["draft", "prerelease"]:
            with self.subTest(flag=key):
                release = {"tag_name": "v1.2.3", "draft": False, "prerelease": False,
                           "assets": [{"name": "skuggsja.rb"}], key: True}
                result = self.run_case(release=release)
                self.assertNotEqual(result["exit"], 0)
                self.assertEqual(len(result["calls"]), 1)

    def test_missing_or_duplicate_asset_fails_before_download(self):
        for assets in [[], [{"name": "skuggsja.rb"}, {"name": "skuggsja.rb"}]]:
            with self.subTest(assets=assets):
                result = self.run_case(release={"tag_name": "v1.2.3", "draft": False,
                                               "prerelease": False, "assets": assets})
                self.assertNotEqual(result["exit"], 0)
                self.assertEqual(len(result["calls"]), 1)

    def test_numeric_upgrade_is_not_a_lexical_comparison(self):
        result = self.run_case(current=formula("1.9.0"), tag="v1.10.0")
        self.assertEqual(result["exit"], 0, result["stderr"])
        self.assertEqual(result["content"], formula("1.10.0"))

    def test_rollback_fails_before_download(self):
        result = self.run_case(current=formula("2.0.0"))
        self.assertNotEqual(result["exit"], 0)
        self.assertEqual(result["content"], formula("2.0.0"))
        self.assertEqual(len(result["calls"]), 1)

    def test_bad_attestation_cannot_change_formula(self):
        result = self.run_case(current=formula("1.0.0"), attestation_failure=True)
        self.assertNotEqual(result["exit"], 0)
        self.assertEqual(result["content"], formula("1.0.0"))
        self.assertEqual(result["output"], "")
        self.assertIn("attestation failed", result["stderr"])

    def test_download_failure_cannot_change_formula(self):
        result = self.run_case(current=formula("1.0.0"), download_failure=True)
        self.assertNotEqual(result["exit"], 0)
        self.assertEqual(result["content"], formula("1.0.0"))
        self.assertEqual(len(result["calls"]), 2)

    def test_attested_asset_must_match_release_version(self):
        result = self.run_case(current=formula("1.0.0"), downloaded=formula("9.0.0"))
        self.assertNotEqual(result["exit"], 0)
        self.assertEqual(result["content"], formula("1.0.0"))
        self.assertEqual(result["calls"][-1][:2], ["attestation", "verify"])

    def test_same_version_is_idempotent(self):
        result = self.run_case(current=formula("1.2.3"))
        self.assertEqual(result["exit"], 0, result["stderr"])
        self.assertEqual(result["output"], "changed=false\nversion=1.2.3\n")
        self.assertEqual(result["content"], formula("1.2.3"))

    def test_same_version_mutation_is_refused(self):
        result = self.run_case(current=formula("1.2.3"), downloaded=formula("1.2.3", "  # changed\n"))
        self.assertNotEqual(result["exit"], 0)
        self.assertEqual(result["content"], formula("1.2.3"))

    def test_invalid_current_version_fails_closed(self):
        result = self.run_case(current=formula("not-stable"))
        self.assertNotEqual(result["exit"], 0)
        self.assertEqual(result["content"], formula("not-stable"))
        self.assertEqual(result["calls"], [])

    def test_symlink_destination_is_not_followed(self):
        result = self.run_case(symlink=True)
        self.assertNotEqual(result["exit"], 0)
        self.assertEqual(result["calls"], [])

    def test_concurrent_checkout_change_is_not_overwritten(self):
        concurrent = formula("1.1.0")
        result = self.run_case(current=formula("1.0.0"), concurrent_content=concurrent)
        self.assertNotEqual(result["exit"], 0)
        self.assertEqual(result["content"], concurrent)
        self.assertIn("changed during verification", result["stderr"])

    def test_ruby_is_copied_as_data_without_evaluation(self):
        # Ruby that would fail if loaded is harmless data to the attested copier.
        downloaded = formula("1.2.3", '  raise "Downloaded Ruby must never execute in updater"\n')
        result = self.run_case(downloaded=downloaded)
        self.assertEqual(result["exit"], 0, result["stderr"])
        self.assertEqual(result["content"], downloaded)


if __name__ == "__main__":
    unittest.main(verbosity=2)
