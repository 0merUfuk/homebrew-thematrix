# homebrew-thematrix

Homebrew tap for [the-matrix](https://github.com/0merUfuk/the-matrix) — four Go CLIs that provision and maintain autonomous Claude Code agent ecosystems.

## Install

```bash
brew tap 0merUfuk/thematrix
brew install neo morp oracle trinity
```

## Tools

| Formula | Description |
|---------|-------------|
| `neo` | Meta-CLI orchestrator — provisions agent ecosystems |
| `morp` | Service scaffolding + autonomous development loops |
| `oracle` | Knowledge synthesis engine for any tech stack |
| `trinity` | Maintenance runtime for agent ecosystems |

The four the-matrix formulae are updated via [GoReleaser](https://goreleaser.com).

## Rifja

This tap also distributes [Rifja](https://github.com/0merUfuk/rifja),
an offline CLI for resuming engineering work across agent sessions and Git.

```sh
brew install 0merUfuk/thematrix/rifja
rifja --help
```

Homebrew manages its Python runtime and environment. Update with `brew update`
and `brew upgrade 0merUfuk/thematrix/rifja`; remove with `brew uninstall --force 0merUfuk/thematrix/rifja`.
Existing `session-visualizer` installations migrate on `brew update` and
`brew upgrade 0merUfuk/thematrix/rifja`. The old formula and command remain aliases.
Application state and backups survive uninstall. The project release procedure
updates the formula from checksummed, attested GitHub release assets.

### Platform note

Current Homebrew no longer supplies prebuilt bottles for Intel macOS. It may
compile dependencies such as OpenSSL during installation, making a first install
considerably slower. The application is tested on Intel macOS, but the quickest
Homebrew installation experience is on Apple Silicon and Linux x86-64.

## Skuggsja

[Skuggsja](https://github.com/0merUfuk/skuggsja) has moved to its
[dedicated Homebrew tap](https://github.com/0merUfuk/homebrew-skuggsja).
New installations use:

```sh
brew install 0merUfuk/skuggsja/skuggsja
```

For existing installations, prepare the destination before updating:

```sh
brew trust --formula 0merUfuk/skuggsja/skuggsja
brew tap 0merUfuk/skuggsja
brew update
```

Check every installed receipt, including retained older kegs:

```sh
for receipt in "$(brew --cellar skuggsja)"/*/INSTALL_RECEIPT.json; do
  printf '%s\n' "$receipt"
  cat "$receipt"
done
```

Each receipt's `source.tap` should be `0merufuk/skuggsja`. Automatic same-version
migration preserves binaries and pins. If an earlier update already processed
the move while the destination was unavailable, qualified reinstall alone can
retain the former tap through Homebrew's receipt cache. Recover without uninstall:

```sh
brew trust --command 0merUfuk/skuggsja/skuggsja-migrate
HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_FROM_API=1 HOMEBREW_NO_ANALYTICS=1 \
  brew skuggsja-migrate --check
HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_FROM_API=1 HOMEBREW_NO_ANALYTICS=1 \
  brew skuggsja-migrate --apply
```

The dedicated command verifies known original release binaries, backs up affected
receipts and changes only their tap association. It preserves retained kegs,
pins, completions and reports; it does not read harness histories. Check its
reported result rather than assuming an exit code proves migration.

Keep The Matrix tap for its other tools. Do not force-untap it or silently unpin
Skuggsja. See the [project migration guide](https://github.com/0merUfuk/skuggsja#existing-the-matrix-tap-installations)
for the supported legacy versions and details of this one-time recovery.
