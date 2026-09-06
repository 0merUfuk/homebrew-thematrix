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

[Skuggsja](https://github.com/0merUfuk/skuggsja) is a local, read-only retrospective for AI coding-agent history. The formula installs a prebuilt executable on macOS or Linux, for Intel/AMD and ARM64, with its UI and shell completions included. No Go, Python or Node.js runtime is needed.

```sh
brew install 0merUfuk/thematrix/skuggsja
skuggsja
```

Update with `brew update` and `brew upgrade 0merUfuk/thematrix/skuggsja`; remove with `brew uninstall 0merUfuk/thematrix/skuggsja`. Uninstall leaves generated reports in place. See the [project documentation](https://github.com/0merUfuk/skuggsja#readme) for usage, source coverage and privacy boundaries.

The Skuggsja update workflow checks daily or on manual dispatch, verifies the release formula's GitHub attestation and source tag, and refuses version rollback. It uses this tap's own workflow token; no cross-repository secret is required. Existing formulas retain their release process.
