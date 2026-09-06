#!/usr/bin/env python3
"""Update one formula from an attested stable release; never execute its Ruby."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

UPSTREAM = "0merUfuk/skuggsja"
WORKFLOW = UPSTREAM + "/.github/workflows/release.yml"
STABLE = r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
ROOT = Path(__file__).resolve().parents[2]


class UpdateError(Exception):
    """A failed update guard; the installed formula must remain unchanged."""


def gh(*args):
    try:
        return subprocess.run(
            ["gh", *args], capture_output=True, text=True, timeout=120, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise UpdateError("GitHub CLI could not complete the release check") from error


def latest_release():
    response = gh("api", "--include", "repos/" + UPSTREAM + "/releases/latest")
    # --include supplies the HTTP status even when gh exits nonzero for a 404.
    header, separator, body = response.stdout.replace("\r\n", "\n").partition("\n\n")
    status = re.search(r"^HTTP/[0-9.]+ ([0-9]{3})\b", header)
    if status and status[1] == "404" and response.returncode != 0:
        return None
    if response.returncode or not separator or not status or status[1] != "200":
        raise UpdateError("Unable to read the upstream release; only HTTP 404 is a no-op")
    try:
        release = json.loads(body)
    except ValueError as error:
        raise UpdateError("Invalid upstream release metadata") from error
    if not isinstance(release, dict):
        raise UpdateError("Invalid upstream release metadata")
    tag = release.get("tag_name")
    if not isinstance(tag, str) or not re.fullmatch("v" + STABLE, tag):
        raise UpdateError("Latest release must have a canonical stable vMAJOR.MINOR.PATCH tag")
    if release.get("draft") is not False or release.get("prerelease") is not False:
        raise UpdateError("Draft and prerelease formulas cannot update the stable tap")
    assets = release.get("assets")
    if not isinstance(assets, list) or sum(
        isinstance(asset, dict) and asset.get("name") == "skuggsja.rb" for asset in assets
    ) != 1:
        raise UpdateError("Stable release must contain exactly one skuggsja.rb asset")
    return tag


def formula_version(content):
    try:
        text = content.decode("utf-8")
    except UnicodeError as error:
        raise UpdateError("Formula is not UTF-8 text") from error
    versions = re.findall(r"^# Skuggsja release version: (.*)$", text, re.MULTILINE)
    if len(versions) != 1 or not re.fullmatch(STABLE, versions[0]):
        raise UpdateError("Formula must have exactly one canonical stable release-version comment")
    version = versions[0]
    if re.search(r"^[ \t]*version\b", text, re.MULTILINE):
        raise UpdateError("Formula version must be inferred from its release URLs")
    urls = re.findall(r'^[ \t]*url "([^"\r\n]+)"$', text, re.MULTILINE)
    expected = {f"https://github.com/{UPSTREAM}/releases/download/v{version}/skuggsja_{version}_{system}_{architecture}.tar.gz"
                for system in ("darwin", "linux") for architecture in ("arm64", "amd64")}
    if len(urls) != 4 or set(urls) != expected:
        raise UpdateError("Formula download URLs must match its release-version comment on all four platforms")
    return version


def output(changed, version=""):
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as stream:
            stream.write("changed=" + str(changed).lower() + "\n")
            if version:
                stream.write("version=" + version + "\n")


def update():
    directory = ROOT / "Formula"
    destination = directory / "skuggsja.rb"
    if directory.is_symlink() or not directory.is_dir() or destination.is_symlink():
        raise UpdateError("Formula destination must be an ordinary file in the tap's Formula directory")
    if destination.exists() and not destination.is_file():
        raise UpdateError("Existing Skuggsja formula is not an ordinary file")
    old_content = destination.read_bytes() if destination.exists() else None
    old_version = formula_version(old_content) if old_content is not None else None
    tag = latest_release()
    if tag is None:
        output(False)
        print("No public stable upstream release is available yet; no files changed.")
        return
    version = tag[1:]
    if old_version and tuple(map(int, version.split("."))) < tuple(map(int, old_version.split("."))):
        raise UpdateError("Refusing to roll back the installed Skuggsja formula")

    with tempfile.TemporaryDirectory(prefix="skuggsja-release-") as temporary:
        artifact = Path(temporary) / "skuggsja.rb"
        downloaded = gh("release", "download", tag, "--repo", UPSTREAM,
                        "--pattern", "skuggsja.rb", "--dir", temporary)
        if downloaded.returncode or not artifact.is_file() or artifact.is_symlink():
            raise UpdateError("Unable to download the release formula")
        verified = gh("attestation", "verify", str(artifact), "--repo", UPSTREAM,
                      "--signer-workflow", WORKFLOW, "--source-ref", "refs/tags/" + tag,
                      "--deny-self-hosted-runners")
        if verified.returncode:
            raise UpdateError("Formula attestation failed; the installed formula is unchanged")
        # The downloaded Ruby is data only: never load, evaluate or run it here.
        content = artifact.read_bytes()
        if len(content) > 65536 or formula_version(content) != version:
            raise UpdateError("Attested formula does not match the expected release version")
        if content == old_content:
            output(False, version)
            print("Skuggsja " + version + " is already current; no files changed.")
            return
        if old_version == version:
            raise UpdateError("An existing stable version changed content; refusing an in-place replacement")
        # Refuse an unexpected concurrent checkout change before installation.
        if destination.is_symlink() or (destination.read_bytes() if destination.exists() else None) != old_content:
            raise UpdateError("Skuggsja formula changed during verification; refusing to overwrite it")
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(dir=directory, prefix=".skuggsja-", delete=False) as staged:
                temporary_path = Path(staged.name)
                staged.write(content)
            temporary_path.chmod(0o644)
            os.replace(temporary_path, destination)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
    output(True, version)
    print("Verified Skuggsja " + version + "; only Formula/skuggsja.rb was updated.")


if __name__ == "__main__":
    try:
        update()
    except (UpdateError, OSError, ValueError) as error:
        print("Skuggsja update failed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
