# Contributing to hermes-kanban

Thanks for considering a contribution. This package is small, focused, and
follows tight conventions to stay reliable inside production agent loops.

## Ground rules

1. **TDD first.** Write a failing test before the fix. RED → GREEN → REFACTOR.
   PRs that only add code without exercising it are rejected.
2. **Single-purpose commits.** One commit, one concern. If you find yourself
   typing "and also" in a commit message, split it.
3. **Conventional Commits.** Format:
   `<type>(<scope>): <subject>` where type ∈ `feat fix docs chore refactor
   test perf build ci style revert`. Examples in the git log.
4. **Determinism over performance.** Especially in scheduling / dispatch
   code paths, no `dict` insertion-order dependencies, no wall-clock
   tie-breakers.
5. **No external runtime deps without discussion.** This package is intentionally **stdlib-only** at runtime — no SQLAlchemy, no asyncpg, nothing that adds an ABI surface. Test-only deps are fine.

## Local setup

```bash
git clone https://github.com/jhashemi/hermes-kanban.git
cd hermes-kanban
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest                          # default: unit + integration
pytest -m "not integration"     # fast feedback
pytest -n 4                     # parallel
pytest --tb=long -vv tests/...  # debug
```

All tests must pass before opening a PR. Stress tests (`-m stress`) are
optional locally but run in CI.

## Code style

- **Formatter:** none enforced; match the surrounding code.
- **Type hints:** required on public API. Internal helpers may skip.
- **Docstrings:** Google style on public symbols; one-liner is fine for
  obvious helpers.
- **Imports:** stdlib → third-party → first-party, separated by blank lines.
- **No print().** Use `logging` with module-level logger.

## Pull request checklist

- [ ] RED test added before the fix (link the failing-test commit)
- [ ] `pytest -m "not stress"` passes locally
- [ ] CHANGELOG.md updated under `[Unreleased]`
- [ ] Public API changes are documented in README
- [ ] Commit messages follow Conventional Commits
- [ ] No new external runtime dependencies (or justification given)

## Reporting bugs

Open an issue with:

- hermes-kanban version (`pip show hermes-kanban`)
- Python version (`python --version`)
- Minimal reproduction (≤30 lines preferred)
- Expected vs actual behaviour
- Full traceback if applicable

## License

By contributing you agree your contributions are licensed under the
[MIT License](LICENSE) of this project.
