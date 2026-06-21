"""Stable identities and seeds for reproducible cosmogenesis runs."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from quanta_engine.version import __version__


def stable_digest(*parts: object, size: int = 16) -> str:
    payload = json.dumps(parts, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.blake2b(payload.encode("utf-8"), digest_size=size).hexdigest()


def stable_seed(run_seed: int, *parts: object) -> int:
    digest = stable_digest(run_seed, *parts, size=8)
    return int(digest, 16) % (2**32)


def stable_identifier(prefix: str, run_seed: int, *parts: object) -> str:
    return f"{prefix}-{stable_digest(run_seed, *parts, size=8).upper()}"


def object_fingerprint(value: Any) -> str:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return stable_digest(value, size=16)


def file_sha256(path: str | Path) -> str | None:
    target = Path(path)
    if not target.is_file():
        return None
    return hashlib.sha256(target.read_bytes()).hexdigest()


def software_version() -> str:
    return __version__


def code_revision(root: str | Path | None = None) -> str | None:
    if revision := os.environ.get("GITHUB_SHA"):
        return revision
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return completed.stdout.strip() if completed.returncode == 0 else None
