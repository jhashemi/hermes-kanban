"""Fixtures shared across hermes_kanban tests."""

from __future__ import annotations

import os
import pytest


@pytest.fixture
def all_assignees_spawnable(monkeypatch):
    """Pretend every assignee maps to a real Hermes profile.

    Most dispatcher tests use synthetic assignees ("alice", "bob") that
    don't correspond to actual profile directories on disk. Without this
    patch, the dispatcher's profile-exists guard routes those tasks into
    ``skipped_nonspawnable`` instead of spawning, which would break tests
    that assert spawn behavior.
    """
    import hermes_kanban._adapters as adapters
    monkeypatch.setattr(adapters, "profile_exists", lambda name: True)


@pytest.fixture
def kanban_home(tmp_path, monkeypatch):
    """Provide a temporary kanban home directory and DB connection.

    Sets HERMES_KANBAN_HOME to a temp directory so tests don't touch
    the real ~/.hermes. Returns the Path.
    """
    monkeypatch.setenv("HERMES_KANBAN_HOME", str(tmp_path))
    yield tmp_path