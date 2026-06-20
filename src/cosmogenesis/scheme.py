"""Shared scheme protocol and the common objective/optimizer plumbing."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, runtime_checkable

from quanta_engine.core.schema import UniverseConfig

from .assessment import UniverseAssessment
from .critique import Critique
from .parameters import ParameterVector

# An objective maps a parameter vector to a scalar to be MAXIMIZED.
Objective = Callable[[ParameterVector], float]


@runtime_checkable
class UniverseScheme(Protocol):
    """Both Scheme A (analytic) and Scheme B (variational) implement this."""

    name: str

    def assess(self, vector: ParameterVector) -> UniverseAssessment: ...

    def base_score(self, vector: ParameterVector) -> float:
        """The scheme's own primary objective (no adversarial penalties)."""
        ...

    def objective(self, vector: ParameterVector) -> float:
        """base_score minus any adversarial penalties accepted so far."""
        ...

    def optimize(self, start: ParameterVector, budget: int) -> ParameterVector: ...

    def critique(self, rival_champion: ParameterVector, rival: UniverseScheme) -> Critique: ...

    def consider(self, critique: Critique) -> bool:
        """Evaluate the rival's critique under our own model; adopt if it helps."""
        ...


class BaseScheme:
    """Common state: the active config, accepted penalties, champion bookkeeping."""

    name = "base"

    def __init__(self, base_config: UniverseConfig) -> None:
        self.base_config = base_config
        # penalty_name -> weight; populated when we accept a rival's critique.
        self.penalties: dict[str, float] = {}
        self.last_champion: ParameterVector = ParameterVector.default()

    # subclasses implement assess/base_score; objective is shared.
    def assess(self, vector: ParameterVector) -> UniverseAssessment:  # pragma: no cover
        raise NotImplementedError

    def base_score(self, vector: ParameterVector) -> float:  # pragma: no cover
        raise NotImplementedError

    def penalty_value(self, vector: ParameterVector) -> float:
        """Total accepted-penalty magnitude for a vector. Overridden by subclasses."""

        return 0.0

    def objective(self, vector: ParameterVector) -> float:
        return self.base_score(vector) - self.penalty_value(vector)
