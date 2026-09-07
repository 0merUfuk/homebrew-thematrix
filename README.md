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


## Skuggsja

[Skuggsja](https://github.com/0merUfuk/skuggsja) has moved to its
[dedicated Homebrew tap](https://github.com/0merUfuk/homebrew-skuggsja).
New installations use:

```sh
brew install 0merUfuk/skuggsja/skuggsja
```

For an existing installation, run `brew update` and inspect
`"$(brew --prefix skuggsja)/INSTALL_RECEIPT.json"`. The receipt's `source.tap`
should be `0merufuk/skuggsja`. Homebrew can migrate receipts at the same version
without replacing kegs when the destination tap is available and trusted;
this is not guaranteed to complete on every installation.

If the receipt still names this tap, check `brew list --pinned` first. Preserve
any Skuggsja pin and stop before reinstalling unless you deliberately choose
to unpin. On Homebrew versions with tap trust, the explicit unpinned path is:

```sh
brew trust --formula 0merUfuk/skuggsja/skuggsja
brew tap 0merUfuk/skuggsja
brew reinstall 0merUfuk/skuggsja/skuggsja
skuggsja version
cat "$(brew --prefix skuggsja)/INSTALL_RECEIPT.json"
```

Reinstall selects the destination tap's current version. No uninstall is
needed first. Keep The Matrix tap for its other tools; do not force-untap it.
Generated reports and source histories remain in place. See the
[project migration guide](https://github.com/0merUfuk/skuggsja#existing-the-matrix-tap-installations)
for details and instructions matching your Homebrew version.
