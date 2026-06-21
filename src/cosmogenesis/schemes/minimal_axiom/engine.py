"""minimal_axiom engine: feasibility from the fewest dimensionless numbers.

Uses anthropic inequalities (Carr-Rees / Barrow-Tipler) over alpha, the
gravitational coupling alpha_G = G m_p^2 / (hbar c), and the mass ratio -- no
layered pipeline, no fixed point. Adversarial I/O: ParameterVector -> UniverseAssessment.
"""

from __future__ import annotations

import math
from collections.abc import Mapping

import numpy as np

from quanta_engine.core.schema import UniverseConfig
from quanta_engine.core.units import MEV_C2_KG

from ...core import (
    BaseEngine,
    CalibrationThreshold,
    ParameterVector,
    UniverseAssessment,
    apply_vector,
    logistic_window,
)
from .optimizer import restart_hill_climb

SCHEME_NAME = "minimal_axiom"
_ALPHA_G0 = 5.9e-39


def _falling(value: float, threshold: float, width_decades: float = 1.0) -> float:
    if value <= 0:
        return 1.0
    return 1.0 / (1.0 + math.exp((math.log10(value) - math.log10(threshold)) / width_decades))


class MinimalAxiom(BaseEngine):
    name = SCHEME_NAME
    calibration_thresholds = {
        "alpha_lo": CalibrationThreshold(
            1.0e-3, 3.0e-4, 3.0e-3, "dimensionless", "literature-informed", "minimal.alpha"
        ),
        "alpha_hi": CalibrationThreshold(
            0.1, 0.05, 0.3, "dimensionless", "model-validity", "minimal.alpha"
        ),
        "stellar_number_lo": CalibrationThreshold(
            1.0e48, 1.0e46, 1.0e50, "dimensionless", "order-of-magnitude", "minimal.stellar_number"
        ),
        "stellar_number_hi": CalibrationThreshold(
            1.0e63, 1.0e61, 1.0e65, "dimensionless", "order-of-magnitude", "minimal.stellar_number"
        ),
        "hierarchy_threshold": CalibrationThreshold(
            1.0e-8, 3.0e-9, 3.0e-8, "dimensionless", "order-of-magnitude", "minimal.hierarchy"
        ),
        "lambda_threshold": CalibrationThreshold(
            12.0, 6.0, 24.0, "scale", "heuristic", "minimal.lambda"
        ),
        "seed_lo": CalibrationThreshold(
            1.0e-6, 3.0e-7, 3.0e-6, "Q", "literature-informed", "minimal.seeds"
        ),
        "seed_hi": CalibrationThreshold(
            3.0e-4, 1.0e-4, 1.0e-3, "Q", "literature-informed", "minimal.seeds"
        ),
    }

    def __init__(self, base_config: UniverseConfig, seed: int = 11) -> None:
        super().__init__(base_config)
        self._rng = np.random.default_rng(seed)

    def _numbers(self, vector: ParameterVector) -> dict[str, float]:
        cfg = apply_vector(self.base_config, vector)
        k = cfg.constants
        d = cfg.dimensionless
        p = cfg.particles
        alpha = d.alpha * d.alpha_scale
        g_eff = k.G * d.gravity_scale
        m_p_kg = p.proton_mass_MeV * MEV_C2_KG
        alpha_g = g_eff * m_p_kg**2 / (k.hbar * k.c)
        beta = p.electron_mass_MeV / p.proton_mass_MeV
        return {"alpha": alpha, "alpha_G": alpha_g, "beta": beta}

    def assess(self, vector: ParameterVector) -> UniverseAssessment:
        return self._assess_with_thresholds(vector, {})

    def _assess_with_thresholds(
        self, vector: ParameterVector, overrides: dict[str, float]
    ) -> UniverseAssessment:
        thresholds: Mapping[str, float] = {
            name: item.nominal for name, item in self.calibration_thresholds.items()
        } | overrides
        cfg = apply_vector(self.base_config, vector)
        n = self._numbers(vector)
        alpha, alpha_g = n["alpha"], n["alpha_G"]
        cc = cfg.dimensionless.cosmological_constant_scale
        amp = math.sqrt(max(cfg.cosmology.primordial_amplitude, 0.0))

        m_atoms = logistic_window(alpha, lo=thresholds["alpha_lo"], hi=thresholds["alpha_hi"])
        n_star = alpha_g ** (-1.5)
        m_stars = logistic_window(
            n_star,
            lo=thresholds["stellar_number_lo"],
            hi=thresholds["stellar_number_hi"],
        )
        hierarchy = math.sqrt(alpha_g) / max(alpha, 1e-12)
        m_hierarchy = _falling(
            hierarchy, threshold=thresholds["hierarchy_threshold"], width_decades=1.5
        )
        m_lambda = _falling(cc, threshold=thresholds["lambda_threshold"], width_decades=0.5)
        m_seeds = logistic_window(
            max(amp, 1e-12), lo=thresholds["seed_lo"], hi=thresholds["seed_hi"]
        )

        margins = {
            "atoms": m_atoms,
            "stars": m_stars,
            "hierarchy": m_hierarchy,
            "lambda": m_lambda,
            "seeds": m_seeds,
        }
        vals = list(margins.values())
        score = math.exp(sum(math.log(max(v, 1e-9)) for v in vals) / len(vals))
        warnings = [f"weak anthropic margin: {key}" for key, v in margins.items() if v < 0.3]
        return UniverseAssessment(
            scheme=self.name,
            score=score,
            feasible=score > 0.5,
            margins=margins,
            residual=0.0,
            diagnostics={
                "alpha": alpha,
                "alpha_G": alpha_g,
                "N_star": n_star,
                "hierarchy_ratio": hierarchy,
                "free_parameters": 3,  # alpha, alpha_G, beta -- the minimal set
                # closed-form anthropic inequalities: the cheapest paradigm (QE-2026-102).
                "compute_cost": len(margins),
            },
            warnings=warnings,
        )

    def optimize(self, start: ParameterVector, budget: int = 60) -> ParameterVector:
        best = restart_hill_climb(self, start, budget=budget)
        self.last_champion = best
        return best
