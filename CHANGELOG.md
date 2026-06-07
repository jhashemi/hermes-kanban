# Changelog

All notable changes to `hermes-kanban` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `dispatch_once_free()` — task-tree unfolding variant of `dispatch_once()`.
  BFS traversal through `task_links` builds a candidate subtree from each
  ready task, scoring nodes by `descendant_count` and `descendant_priority_sum`.
  Closes Gap **G-S5-H1-1** (executive_agents_framework dispatch coverage gap).
- `_build_task_subtree()` — internal BFS helper. Returns `{task_id → {depth,
  descendant_count, descendant_priority_sum}}` for every task reachable from
  a list of ready ids.
- `DispatchResult.tree_depth` field — maximum task-tree depth traversed
  during dispatch (0 = flat / no tree).
- `.gitignore` covering Python build artifacts (`.venv/`, `__pycache__/`,
  `*.egg-info/`, `.pytest_cache/`, `htmlcov/`), local data (`*.duckdb`,
  `*.sqlite`), and IDE / OS detritus.

### Fixed
- Untracked stale `src/hermes_kanban/__pycache__/kanban_db.cpython-311.pyc`
  that had drifted from source. Pre-existing pollution of ~2900 `.venv/`
  files in HEAD remains for a future hygiene pass.

## [0.1.0] — 2026-06-07

### Added
- Initial extraction from `hermes-agent` (`hermes_cli/kanban_db.py` and
  `hermes_cli/kanban.py`) as a standalone, zero-runtime-dependency package.
- `kanban_db` — Core SQLite engine: WAL mode, CAS coordination, multi-board.
- `kanban` — CLI surface: 15-verb argparse interface, used by the
  `/kanban` slash command.
- `kanban_diagnostics` — Board health diagnostics and repair.
- `kanban_specify` — Task specification and template management.
- `dispatch_cards` — VCG-optimized kanban card generation.
- Upstream import compatibility shims so existing hermes-agent callers
  continue to work without modification.

[Unreleased]: https://github.com/jhashemi/hermes-kanban/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/jhashemi/hermes-kanban/releases/tag/v0.1.0
