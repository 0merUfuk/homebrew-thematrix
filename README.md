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

[Skuggsja](https://github.com/0merUfuk/skuggsja) is a local retrospective for AI coding-agent history. Its prebuilt macOS/Linux formula is pending the first stable upstream release. Once available, install it with `brew install 0merUfuk/thematrix/skuggsja`.

The Skuggsja update workflow checks daily or on manual dispatch, verifies the release formula's GitHub attestation and source tag, and refuses version rollback. It uses this tap's own workflow token; no cross-repository secret is required. Existing formulas retain their release process.
