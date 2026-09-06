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

## Session Visualizer

This tap also distributes [Session Visualizer](https://github.com/0merUfuk/session-visualizer),
an offline CLI for resuming engineering work across agent sessions and Git.

```sh
brew install 0merUfuk/thematrix/session-visualizer
session-visualizer --help
```

Homebrew manages its Python runtime and environment. Update with `brew update`
and `brew upgrade 0merUfuk/thematrix/session-visualizer`; remove with `brew uninstall --force 0merUfuk/thematrix/session-visualizer`.
Application state and backups survive uninstall. The project release procedure
updates the formula from checksummed, attested GitHub release assets.
