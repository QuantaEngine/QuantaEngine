"""TheoryRegistry: tracks theory lineages. Never merges; always preserves parents."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from threading import RLock

import yaml

from .theory import TheorySpec, load_theory


class TheoryRegistry:
    def __init__(self, policy: dict | None = None) -> None:
        self._theories: dict[str, TheorySpec] = {}
        self.policy = dict(policy or {})
        self._lock = RLock()

    def add(self, theory: TheorySpec) -> None:
        with self._lock:
            self._theories[theory.theory_id] = theory

    def get(self, theory_id: str) -> TheorySpec:
        with self._lock:
            return self._theories[theory_id]

    def __contains__(self, theory_id: str) -> bool:
        with self._lock:
            return theory_id in self._theories

    def all(self) -> list[TheorySpec]:
        with self._lock:
            return list(self._theories.values())

    def families(self) -> set[str]:
        with self._lock:
            return {t.family for t in self._theories.values()}

    def next_theory_id(self) -> str:
        with self._lock:
            nums = [
                int(tid[2:]) for tid in self._theories if tid.startswith("T-") and tid[2:].isdigit()
            ]
            return f"T-{(max(nums) + 1) if nums else 1:04d}"

    @contextmanager
    def transaction(self):
        with self._lock:
            yield self

    def lineage(self, theory_id: str) -> list[str]:
        with self._lock:
            chain = [theory_id]
            cur = self._theories.get(theory_id)
            while cur and cur.parent_id:
                chain.append(cur.parent_id)
                cur = self._theories.get(cur.parent_id)
            return list(reversed(chain))

    @classmethod
    def from_theories(
        cls, theories: list[TheorySpec], policy: dict | None = None
    ) -> TheoryRegistry:
        registry = cls(policy=policy)
        for theory in theories:
            registry.add(theory.model_copy(deep=True))
        return registry

    @classmethod
    def from_dir(cls, root: str | Path) -> TheoryRegistry:
        root = Path(root).expanduser().resolve()
        manifest_path = root / "registry.yaml"
        if manifest_path.is_file():
            data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or not isinstance(data.get("theories"), list):
                raise ValueError(f"invalid theory registry manifest: {manifest_path}")
            policy = dict(data.get("policy") or {})
            if policy.get("allow_merge", False):
                raise ValueError("registry policy cannot enable theory merging")
            registry = cls(policy=policy)
            for item in data["theories"]:
                theory = load_theory(root / item["path"])
                expected = (item.get("id"), item.get("family"), item.get("engine"))
                actual = (theory.theory_id, theory.family, theory.engine)
                if expected != actual:
                    raise ValueError(
                        f"registry entry does not match {item['path']}: {expected} != {actual}"
                    )
                registry.add(theory)
            return registry
        registry = cls()
        for path in sorted(root.glob("T-*/theory.yaml")):
            registry.add(load_theory(path))
        return registry
