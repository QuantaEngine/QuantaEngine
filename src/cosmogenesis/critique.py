"""Cross-scheme critique objects and shared analysis helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .parameters import AXES, ParameterVector


@dataclass(slots=True)
class Critique:
    """One scheme's documented criticism of the other's champion universe.

    ``suggestion`` is a concrete parameter vector the critic proposes; the target
    scheme evaluates it under *its own* model and decides whether to adopt it.
    ``penalty`` names a regularizer the target is invited to add to its objective.
    """

    critic: str
    target: str
    weakness: str
    severity: float  # 0..1
    evidence: dict[str, Any] = field(default_factory=dict)
    suggestion: ParameterVector | None = None
    penalty: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["suggestion"] = self.suggestion.as_dict() if self.suggestion else None
        return d


def fragility_profile(
    champion: ParameterVector,
    score_fn,
    epsilon: float = 0.05,
) -> dict[str, float]:
    """How fast a champion's score collapses under +/- epsilon (normalized) per axis.

    Returns axis_name -> worst relative score drop. The largest entry is the
    "fragile axis" along which the universe is least robust.
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
            drop = max(0.0, (base - s) / base)
            worst = max(worst, drop)
        profile[axis.name] = worst
    return profile


def nudge_toward(
    champion: ParameterVector,
    target: ParameterVector,
    axis_name: str,
    fraction: float = 0.5,
) -> ParameterVector:
    """Move ``champion`` a fraction of the way to ``target`` along one axis only."""

    from .parameters import AXIS_BY_NAME

    idx = list(AXIS_BY_NAME).index(axis_name)
    cn = champion.to_normalized()
    tn = target.to_normalized()
    cn[idx] = cn[idx] + fraction * (tn[idx] - cn[idx])
    return ParameterVector.from_normalized(cn)


def descend_residual(
    champion: ParameterVector,
    residual_fn,
    step: float = 0.08,
) -> tuple[ParameterVector, str]:
    """Find the single normalized axis step that most reduces ``residual_fn``.

    Returns the improved vector and the axis name that drove the reduction.
    """

    base = residual_fn(champion)
    normalized = champion.to_normalized()
    best_vec = champion
    best_res = base
    best_axis = "(none)"
    for i, axis in enumerate(AXES):
        for sign in (+1.0, -1.0):
            probe = list(normalized)
            probe[i] = min(1.0, max(0.0, probe[i] + sign * step))
            cand = ParameterVector.from_normalized(probe)
            r = residual_fn(cand)
            if r < best_res - 1e-12:
                best_res, best_vec, best_axis = r, cand, axis.name
    return best_vec, best_axis
