"""File-backed theory identity: TheorySpec, philosophy, lineage, registry."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


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
    allow_merge: bool = False  # invariant: theories are never merged
    preserve_parent: bool = True


class Claim(BaseModel):
    claim_id: str
    statement: str
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    falsifiability: float = Field(default=0.5, ge=0.0, le=1.0)


class TheorySpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    theory_id: str
    name: str
    family: str
    version: str = "0.1.0"
    parent_id: str | None = None

    # which physics paradigm generates this theory's universes.
    engine: str  # "AnalyticCompiler" | "VariationalRelaxer" | "MinimalAxiomDimensional"
    base_config: str = "configs/standard_universe.yaml"
    # optional starting point in the shared parameter space (defaults to config).
    seed_vector: list[float] | None = None

    philosophy: TheoryPhilosophy = Field(default_factory=TheoryPhilosophy)
    axioms: dict[str, Any] = Field(default_factory=dict)
    claims: list[Claim] = Field(default_factory=list)
    known_limits: list[str] = Field(default_factory=list)
    defense_prior: DefensePrior = Field(default_factory=DefensePrior)
    lineage_policy: LineagePolicy = Field(default_factory=LineagePolicy)

    def bump_patch(self) -> str:
        major, minor, patch = (int(x) for x in self.version.split("."))
        return f"{major}.{minor}.{patch + 1}"

    def bump_minor(self) -> str:
        major, minor, _ = (int(x) for x in self.version.split("."))
        return f"{major}.{minor + 1}.0"


def load_theory(path: str | Path) -> TheorySpec:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return TheorySpec.model_validate(data)


def save_theory(theory: TheorySpec, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        yaml.safe_dump(theory.model_dump(), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


class TheoryRegistry:
    """In-memory registry of theory lineages; never merges, always preserves parents."""

    def __init__(self) -> None:
        self._theories: dict[str, TheorySpec] = {}

    def add(self, theory: TheorySpec) -> None:
        self._theories[theory.theory_id] = theory

    def get(self, theory_id: str) -> TheorySpec:
        return self._theories[theory_id]

    def __contains__(self, theory_id: str) -> bool:
        return theory_id in self._theories

    def all(self) -> list[TheorySpec]:
        return list(self._theories.values())

    def families(self) -> set[str]:
        return {t.family for t in self._theories.values()}

    def next_theory_id(self) -> str:
        nums = [int(tid.split("-")[1]) for tid in self._theories if tid.startswith("T-")]
        return f"T-{(max(nums) + 1) if nums else 1:04d}"

    def lineage(self, theory_id: str) -> list[str]:
        chain = [theory_id]
        cur = self._theories.get(theory_id)
        while cur and cur.parent_id:
            chain.append(cur.parent_id)
            cur = self._theories.get(cur.parent_id)
        return list(reversed(chain))

    @classmethod
    def from_dir(cls, root: str | Path) -> TheoryRegistry:
        registry = cls()
        for path in sorted(Path(root).glob("T-*/theory.yaml")):
            registry.add(load_theory(path))
        return registry
