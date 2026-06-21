"""The contract every scheme implements, plus shared analysis helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from quanta_engine.core.schema import UniverseConfig

from .assessment import UniverseAssessment
from .parameters import AXES, ParameterVector


@dataclass(slots=True)
class ConsiderDecision:
    """Outcome of a scheme independently reconsidering a rival's suggestion.

    ``champion`` is the parameter vector the recipient keeps afterwards -- either an
    improved point (when adopted) or its own unchanged current (when rejected).
    Schemes are never merged: this only ever updates one recipient's own lineage.
    """

    adopt: bool
    champion: ParameterVector
    own_before: float
    own_after: float
    reason: str


@runtime_checkable
class UniverseScheme(Protocol):
    """A self-contained universe-generation paradigm.

    The adversarial I/O is deliberately minimal and identical across schemes:
    a ``ParameterVector`` goes in, a ``UniverseAssessment`` comes out, and the
    scheme can iteratively optimize within the shared parameter space.
    """

    name: str

    def assess(self, vector: ParameterVector) -> UniverseAssessment: ...

    def base_score(self, vector: ParameterVector) -> float: ...

    def optimize(self, start: ParameterVector, budget: int) -> ParameterVector: ...


class BaseEngine:
    """Common bookkeeping for a scheme engine (no adversarial penalties here --
    cross-scheme pressure lives entirely in ``cosmogenesis.arena``)."""

    name = "base"

    def __init__(self, base_config: UniverseConfig) -> None:
        self.base_config = base_config
        self.last_champion: ParameterVector = ParameterVector.default()

    def assess(self, vector: ParameterVector) -> UniverseAssessment:  # pragma: no cover
        raise NotImplementedError

    def base_score(self, vector: ParameterVector) -> float:
        return self.assess(vector).score

    # the objective an optimizer maximizes (schemes may override).
    def objective(self, vector: ParameterVector) -> float:
        return self.base_score(vector)

    def optimize(self, start: ParameterVector, budget: int) -> ParameterVector:  # pragma: no cover
        raise NotImplementedError

    def consider(
        self,
        current: ParameterVector,
        suggestion: ParameterVector,
        budget: int = 20,
        eps: float = 1e-9,
    ) -> ConsiderDecision:
        """Independently reconsider a rival's ``suggestion`` under our OWN objective.

        We are not a blind follower: we evaluate the suggested point, and also try a
        short optimization warm-started from it within our own model. We adopt the
        result only if it *strictly* beats our current champion under our own
        objective; otherwise we keep our own champion unchanged. Schemes are never
        merged -- only this recipient's own lineage may move.
        """

        own_before = self.objective(current)
        candidate = suggestion
        own_after = self.objective(suggestion)
        if budget > 0:
            warm = self.optimize(suggestion, budget)
            warm_score = self.objective(warm)
            if warm_score > own_after:
                candidate, own_after = warm, warm_score
        if own_after > own_before + eps:
            return ConsiderDecision(
                True, candidate, own_before, own_after, "self-verified improvement"
            )
        return ConsiderDecision(
            False, current, own_before, own_after, "no self-verified improvement; kept own champion"
        )


def fragility_profile(
    champion: ParameterVector,
    score_fn,
    epsilon: float = 0.05,
) -> dict[str, float]:
    """Per-axis worst relative score drop under a +/- epsilon normalized nudge.

    The largest entry marks the axis along which a universe is least robust.
    Shared by scoring, agents, and optimizers.
    """

    base = max(score_fn(champion), 1e-9)
    normalized = champion.to_normalized()
    profile: dict[str, float] = {}
    for i, axis in enumerate(AXES):
        worst = 0.0
        for sign in (+1.0, -1.0):
            probe = list(normalized)
            probe[i] = min(1.0, max(0.0, probe[i] + sign * epsilon))
            s = score_fn(ParameterVector.from_normalized(probe))
            worst = max(worst, max(0.0, (base - s) / base))
        profile[axis.name] = worst
    return profile
