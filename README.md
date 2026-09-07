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

Trust the destination formula and add its tap before updating, so Homebrew can use it when processing the old tap's migration entry:

```sh
brew trust --formula 0merUfuk/skuggsja/skuggsja
brew tap 0merUfuk/skuggsja
brew update
skuggsja version
```

Inspect every installed receipt, including any retained older kegs:

```sh
for receipt in "$(brew --cellar skuggsja)"/*/INSTALL_RECEIPT.json; do
  printf '%s\n' "$receipt"
  cat "$receipt"
done
```

Each receipt's `source.tap` should be `0merufuk/skuggsja` before calling the whole installation migrated. The automatic same-version path updates all retained keg receipts without replacing their binaries or clearing a pin. It may not run again if an earlier update already processed the move while the destination was unavailable.

If the current keg's receipt still names the old tap, check `brew list --pinned`. Homebrew skips a pinned reinstall; preserve the pin unless you deliberately choose to unpin it. For an unpinned installation, recover with:

```sh
brew reinstall 0merUfuk/skuggsja/skuggsja
skuggsja version
```

Then repeat the receipt check. Reinstall selects the destination tap's current version; retained older receipts may still name their historical tap, so a successful reinstall does not prove every keg migrated. `brew trust` applies to Homebrew versions with tap trust; follow your installed version's instructions. These steps preserve Skuggsja's generated report and source histories. Keep The Matrix tap if you use its other tools.

No uninstall is needed first; do not force-untap The Matrix. See the
[project migration guide](https://github.com/0merUfuk/skuggsja#existing-the-matrix-tap-installations)
for the current instructions.
