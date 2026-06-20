"""Bridge from a TheorySpec to one of the three physics paradigms in cosmogenesis."""

from __future__ import annotations

from functools import lru_cache

from cosmogenesis import ParameterVector, SchemeA, SchemeB, SchemeC, vector_from_config
from cosmogenesis.assessment import UniverseAssessment
from quanta_engine.core.schema import load_config

from .theory import TheorySpec

ENGINE_CLASSES = {
    "AnalyticCompiler": SchemeA,
    "VariationalRelaxer": SchemeB,
    "MinimalAxiomDimensional": SchemeC,
}


@lru_cache(maxsize=32)
def _load(config_path: str):
    return load_config(config_path)


def build_engine(theory: TheorySpec):
    """Instantiate the paradigm engine named by the theory."""

    if theory.engine not in ENGINE_CLASSES:
        raise ValueError(f"unknown engine '{theory.engine}' for {theory.theory_id}")
    config = _load(theory.base_config)
    return ENGINE_CLASSES[theory.engine](config)


def seed_vector(theory: TheorySpec) -> ParameterVector:
    if theory.seed_vector is not None:
        return ParameterVector(list(theory.seed_vector))
    return vector_from_config(_load(theory.base_config))


def assess(theory: TheorySpec, vector: ParameterVector) -> UniverseAssessment:
    return build_engine(theory).assess(vector)


def optimize(theory: TheorySpec, vector: ParameterVector, budget: int = 70) -> ParameterVector:
    engine = build_engine(theory)
    return engine.optimize(vector, budget=budget)


# A scheme-agnostic feature vector for novelty search (same axes for every engine).
def novelty_features(theory: TheorySpec, vector: ParameterVector) -> list[float]:
    out = assess(theory, vector)
    diag = out.diagnostics
    return [
        *vector.values,  # the fundamental knobs
        float(diag.get("binding_eV", diag.get("alpha", 0.0)) or 0.0),
        float(diag.get("stellar_lifetime_years", 0.0) or 0.0) ** 0.0,  # presence flag
        out.score,
        out.residual,
    ]
