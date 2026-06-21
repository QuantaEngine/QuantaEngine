"""File-backed theory identity: TheorySpec, philosophy, claims, lineage policy.

A theory is a *named lineage instance*: it picks one scheme (``engine``), a config,
claims, a philosophy, a version and a parent. The registry lives in ``registry.py``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator

from ..core import NDIM


class TheoryPhilosophy(BaseModel):
    summary: str = ""
    conservatism: float = Field(default=0.5, ge=0.0, le=1.0)
    novelty: float = Field(default=0.5, ge=0.0, le=1.0)
    computational_efficiency: float = Field(default=0.5, ge=0.0, le=1.0)
    bottom_up_derivation: float = Field(default=0.5, ge=0.0, le=1.0)
    empirical_fidelity: float = Field(default=0.5, ge=0.0, le=1.0)


class DefensePrior(BaseModel):
    default_stance: str = "defend"
    conservatism: float = Field(default=0.7, ge=0.0, le=1.0)
    novelty_preference: float = Field(default=0.3, ge=0.0, le=1.0)
    minimum_evidence_threshold: float = Field(default=0.6, ge=0.0, le=1.0)


class LineagePolicy(BaseModel):
    allow_patch: bool = True
    allow_fork: bool = True
    allow_merge: Literal[False] = False
    preserve_parent: bool = True


class Claim(BaseModel):
    claim_id: str
    statement: str
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    falsifiability: float = Field(default=0.5, ge=0.0, le=1.0)


class TheorySpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    theory_id: str = Field(pattern=r"^T-\d{4,}$")
    name: str
    family: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    version: str = Field(default="0.1.0", pattern=r"^\d+\.\d+\.\d+$")
    parent_id: str | None = None

    # which scheme generates this theory's universes (key in cosmogenesis.schemes).
    engine: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    base_config: str = "configs/standard_universe.yaml"
    # optional starting point in the shared parameter space (defaults to config).
    seed_vector: list[float] | None = None

    philosophy: TheoryPhilosophy = Field(default_factory=TheoryPhilosophy)
    axioms: dict[str, Any] = Field(default_factory=dict)
    claims: list[Claim] = Field(default_factory=list)
    known_limits: list[str] = Field(default_factory=list)
    defense_prior: DefensePrior = Field(default_factory=DefensePrior)
    lineage_policy: LineagePolicy = Field(default_factory=LineagePolicy)

    _source_path: Path | None = PrivateAttr(default=None)

    @field_validator("parent_id")
    @classmethod
    def _valid_parent_id(cls, value: str | None) -> str | None:
        if value is not None and (not value.startswith("T-") or not value[2:].isdigit()):
            raise ValueError("parent_id must use the T-NNNN form")
        return value

    @field_validator("seed_vector")
    @classmethod
    def _valid_seed_vector(cls, value: list[float] | None) -> list[float] | None:
        if value is not None and len(value) != NDIM:
            raise ValueError(f"seed_vector must contain {NDIM} values")
        return value

    def resolve_base_config(self, workspace_root: str | Path | None = None) -> Path:
        configured = Path(self.base_config).expanduser()
        if configured.is_absolute():
            return configured.resolve()
        roots: list[Path] = []
        if workspace_root is not None:
            roots.append(Path(workspace_root).expanduser().resolve())
        if self._source_path is not None:
            roots.extend(self._source_path.parent.parents)
            roots.insert(0, self._source_path.parent)
        roots.append(Path.cwd())
        attempted: list[Path] = []
        for root in roots:
            candidate = (root / configured).resolve()
            if candidate in attempted:
                continue
            attempted.append(candidate)
            if candidate.is_file():
                return candidate
        tried = ", ".join(str(path) for path in attempted)
        raise FileNotFoundError(f"base_config '{self.base_config}' not found; tried: {tried}")

    def bump_patch(self) -> str:
        major, minor, patch = (int(x) for x in self.version.split("."))
        return f"{major}.{minor}.{patch + 1}"

    def bump_minor(self) -> str:
        major, minor, _ = (int(x) for x in self.version.split("."))
        return f"{major}.{minor + 1}.0"


def load_theory(path: str | Path) -> TheorySpec:
    source = Path(path).expanduser().resolve()
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    theory = TheorySpec.model_validate(data)
    theory._source_path = source
    return theory


def save_theory(theory: TheorySpec, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        yaml.safe_dump(theory.model_dump(), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
