"""Ψ-Audit S5/H1 acceptance tests — Free over kanban (kr_s5_h1_1).

These tests prove the acceptance criterion for OKR key result ``kr_s5_h1_1``:

    "Free over kanban: dispatcher.dispatch_once() unfolds candidate task-tree
    (depth ≥ 2) and the unfolding is observable on DispatchResult."

The Ψ-Audit framework treats kanban dispatch as a categorical *Free* monad over
the task DAG. ``dispatch_once_free`` is the unfolding variant that, instead of
greedily picking the highest-priority ready row, looks one level deep to favour
ready tasks with the largest ready descendant subtree (so blocking parents
clear sooner and the tree drains end-to-end).

These tests are the structural acceptance evidence the Ψ-Audit OKR ledger
(``okr_accountability.db``) requires before ``kr_s5_h1_1`` can move from
``active``/``blocked`` to ``done``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from hermes_kanban import kanban_db as kb


@pytest.fixture
def kanban_home(tmp_path, monkeypatch):
    """Isolated HERMES_HOME with an empty kanban DB."""
    home = tmp_path / ".hermes"
    home.mkdir()
    monkeypatch.setenv("HERMES_HOME", str(home))
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    kb.init_db()
    return home


# ---------------------------------------------------------------------------
# Surface
# ---------------------------------------------------------------------------

def test_dispatch_once_free_is_exported_callable(kanban_home):
    """The Free-variant must exist and be callable (Gap G-S5-H1-1 closure)."""
    assert callable(getattr(kb, "dispatch_once_free", None)), (
        "dispatch_once_free missing — Ψ-Audit S5/H1 evidence cannot be produced."
    )


def test_dispatch_result_has_tree_depth_field(kanban_home):
    """``DispatchResult.tree_depth`` is the observable for unfolding depth."""
    result = kb.DispatchResult()
    assert hasattr(result, "tree_depth"), "DispatchResult.tree_depth missing"
    assert result.tree_depth == 0, "tree_depth must default to 0 (no unfolding seen yet)"


# ---------------------------------------------------------------------------
# Behavioural acceptance
# ---------------------------------------------------------------------------

def test_dispatch_once_free_unfolds_chain_of_depth_two(
    kanban_home, all_assignees_spawnable
):
    """Acceptance: a chain a → b → c with only ``a`` ready must report depth ≥ 2.

    This is the structural assertion the Ψ-Audit S5/H1 KR demands — that the
    Free unfolding sees beyond the first ready level. ``a`` is the only ready
    task; ``b`` and ``c`` are pending descendants. ``dispatch_once_free`` must
    therefore observe a subtree of depth 2 (b at depth 1, c at depth 2).
    """
    with kb.connect() as conn:
        a = kb.create_task(conn, title="a", assignee="alice")
        b = kb.create_task(conn, title="b", assignee="alice", parents=[a])
        c = kb.create_task(conn, title="c", assignee="alice", parents=[b])

    with kb.connect() as conn:
        result = kb.dispatch_once_free(conn, dry_run=True)

    assert result.tree_depth >= 2, (
        f"Free-monad unfolding should report depth>=2 for a 3-deep chain a→b→c, "
        f"got tree_depth={result.tree_depth}. KR kr_s5_h1_1 not satisfied."
    )


def test_dispatch_once_free_prefers_branching_root_over_leaf(
    kanban_home, all_assignees_spawnable
):
    """Acceptance: between two equally-ready, equally-prioritised tasks, the one
    with more pending descendants must be ranked first.

    This is the *operational* point of the Free variant — drain branching
    subtrees ahead of leaves. If both tasks have the same priority but ``root``
    has 3 pending descendants and ``leaf`` has 0, ``root`` must be ranked
    (and recorded as spawned) first.
    """
    with kb.connect() as conn:
        # Branching task with 3 descendants
        root = kb.create_task(conn, title="root", assignee="alice", priority=5)
        kb.create_task(conn, title="d1", assignee="alice", parents=[root], priority=5)
        kb.create_task(conn, title="d2", assignee="alice", parents=[root], priority=5)
        kb.create_task(conn, title="d3", assignee="alice", parents=[root], priority=5)
        # Leaf task — no descendants, equal priority
        leaf = kb.create_task(conn, title="leaf", assignee="alice", priority=5)

    with kb.connect() as conn:
        result = kb.dispatch_once_free(conn, dry_run=True, max_spawn=1)

    assert result.spawned, (
        "no task spawned even in dry-run — Free unfolding produced empty schedule"
    )
    first_spawned_id = result.spawned[0][0]
    assert first_spawned_id == root, (
        f"Free unfolding must prefer the branching root (3 descendants) over "
        f"the leaf (0 descendants); got first-spawn={first_spawned_id!r}, "
        f"expected root={root!r}, leaf={leaf!r}."
    )


def test_dispatch_once_free_returns_zero_depth_on_empty_board(kanban_home):
    """Sanity: empty board → no unfolding observable, tree_depth == 0."""
    with kb.connect() as conn:
        result = kb.dispatch_once_free(conn)
    assert result.tree_depth == 0
    assert result.spawned == []
