# hermes-kanban

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status: Beta](https://img.shields.io/badge/status-beta-yellow.svg)](#status)

SQLite-backed Kanban board for multi-profile, multi-project agent collaboration.
Zero-runtime-dependency (stdlib only) task queue with WAL-mode concurrency,
CAS coordination, multi-board support, and a 15-verb CLI.

> Extracted from [`hermes-agent`](https://github.com/NousResearch/hermes-agent)
> as a standalone package with proper project structure, TDD coverage, and
> upstream import shims so existing callers keep working unchanged.

---

## Status

**Beta.** In active production use across multiple Hermes deployments. Public
API may shift before 1.0; pin `==0.x.y` in production until the API stabilises.
Schema migrations are tested but not yet automated end-to-end.

## Architecture

| Module | Responsibility |
|---|---|
| `kanban_db` | Core SQLite engine — WAL mode, CAS coordination, multi-board, schema migrations |
| `kanban` | CLI surface — 15-verb argparse interface, used by the `/kanban` slash command |
| `kanban_diagnostics` | Board health diagnostics and repair (orphan detection, lock recovery) |
| `kanban_specify` | Task specification and template management |
| `dispatch_cards` | VCG-optimized kanban card generation |

## Installation

```bash
pip install -e .
# with dev tooling
pip install -e ".[dev]"
```

## Quick start

```python
from hermes_kanban import kanban_db as kb

# Connect to the default board
db = kb.connect()

# Create a card
card_id = kb.create_card(db, title="Implement feature X", assignee="worker-a")

# Claim and start work (atomic CAS — multiple workers can race safely)
kb.claim_task(db, card_id, agent="worker-a")

# Mark complete
kb.complete_task(db, card_id, summary="Feature X done", metadata={"changed_files": ["src/x.py"]})
```

## Dispatch primitives

`hermes-kanban` exposes two scheduler entry points used by upstream
orchestrators (e.g. [`hermes-orchestration`](https://github.com/jhashemi/hermes-orchestration)
and the executive_agents_framework VCG dispatcher):

- **`dispatch_once(conn, ...)`** — flat ready-queue dispatch. Highest-priority
  ready task wins; ties broken by deterministic agent_id sort.
- **`dispatch_once_free(conn, ...)`** — task-tree unfolding variant. BFS through
  `task_links` builds a candidate subtree from each ready task, scoring nodes
  by `descendant_count` and `descendant_priority_sum`. Used to dispatch
  fan-out work plans (Gap G-S5-H1-1 closure).

Both return a `DispatchResult` with `assignments`, `silent_crashes`, and
`tree_depth` (max task-tree depth traversed).

## Testing

```bash
pytest                          # unit + integration
pytest -m "not stress"          # skip stress / concurrency tests
pytest tests/unit/              # unit only
pytest -n 4 -m "not stress"     # parallel, skip stress
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). TL;DR: TDD first, RED test before
fix, single-purpose commits, pass `pytest -m "not stress"` before PR.

## License

[MIT](LICENSE) — copyright 2025-2026 J Hashemi. Portions adapted from
hermes-agent (also MIT-licensed, copyright 2025 Nous Research).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Origin

Extracted from `hermes_cli/kanban_db.py` and `hermes_cli/kanban.py` in
hermes-agent. Upstream imports remain functional via thin adapter modules
so no downstream code in hermes-agent breaks.
