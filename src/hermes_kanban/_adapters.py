"""Adapter stubs for hermes-cli profile/config dependencies.

These are injected at runtime by the host application (hermes-agent).
When running standalone (tests, CLI), sensible defaults are used.

The pattern: each function tries the real hermes_cli implementation first,
falls back to a stdlib-only default if hermes_cli is not installed.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional


def normalize_profile_name(name: str) -> str:
    """Normalize a profile name, stripping whitespace and special chars.

    Falls back to simple string cleaning if hermes_cli is unavailable.
    """
    try:
        from hermes_cli.profiles import normalize_profile_name as _real
        return _real(name)
    except ImportError:
        # Simple fallback: strip, lowercase, replace spaces with hyphens
        return name.strip().lower().replace(" ", "-")


def profile_exists(name: str) -> bool:
    """Check if a profile directory exists under HERMES_HOME.

    Falls back to filesystem check if hermes_cli is unavailable.
    """
    try:
        from hermes_cli.profiles import profile_exists as _real
        return _real(name)
    except ImportError:
        home = Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")))
        return (home / "profiles" / name).is_dir() or name == "default"


def get_active_profile_name() -> str:
    """Get the currently active profile name.

    Falls back to 'default' if hermes_cli is unavailable.
    """
    try:
        from hermes_cli.profiles import get_active_profile_name as _real
        return _real()
    except ImportError:
        return os.environ.get("HERMES_PROFILE", "default")


def load_config() -> dict[str, Any]:
    """Load the hermes configuration.

    Falls back to empty dict if hermes_cli is unavailable.
    """
    try:
        from hermes_cli.config import load_config as _real
        return _real()
    except ImportError:
        return {}