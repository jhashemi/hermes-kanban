# hermes-kanban

SQLite-backed Kanban board for multi-profile, multi-project collaboration.

Extracted from `hermes-agent` as a standalone package with proper project structure,
TDD coverage, and zero external dependencies (stdlib only).

## Architecture

- **kanban_db** — Core SQLite engine (WAL mode, CAS coordination, multi-board)
- **kanban** — CLI surface (15-verb argparse interface, `/kanban` slash command)
- **kanban_diagnostics** — Board health diagnostics and repair
- **kanban_specify** — Task specification and template management
- **dispatch_cards** — VCG-optimized kanban card generation

## Installation

```bash
pip install -e .
```

## Usage

```python
from hermes_kanban import kanban_db as kb

# Connect to the default board
db = kb.connect()

# Create a card
card_id = kb.create_card(db, title="Implement feature X", assignee="worker-a")

# Claim and start work
kb.claim_task(db, card_id, agent="worker-a")
```

## Testing

```bash
pytest                          # unit + integration
pytest -m "not stress"          # skip stress tests
pytest tests/unit/              # unit only
```

## Origin

This package was extracted from `hermes_cli/kanban_db.py` and `hermes_cli/kanban.py`
in hermes-agent. The upstream imports are preserved via thin adapter modules
so no downstream code breaks.