"""Scheme C: minimal-axiom dimensional-analysis engine (third paradigm).

Philosophy: derive universe feasibility from the FEWEST possible dimensionless
numbers using anthropic inequalities (Carr-Rees / Barrow-Tipler style), with no
layered pipeline (unlike A) and no fixed-point relaxation (unlike B). It asks a
handful of order-of-magnitude questions:

  - alpha (EM coupling): are atoms bound and non-relativistic?
  - alpha_G = G m_p^2 / (hbar c) (gravitational coupling): do stars contain many
    nucleons (N* ~ alpha_G^-3/2 >> 1)?
  - hierarchy sqrt(alpha_G)/alpha << 1: are gravitating objects vastly larger
    than atoms (so stars and structure exist at all)?
  - a minimal cosmological constraint on Lambda and the perturbation amplitude.

Optimizer: random-restart coordinate hill-climb (cheap, few parameters), in
keeping with the "minimal machinery" philosophy.
"""

from __future__ import annotations

import math

import numpy as np

from quanta_engine.core.schema import UniverseConfig
from quanta_engine.core.units import MEV_C2_KG

from .assessment import UniverseAssessment, logistic_window
from .parameters import AXES, ParameterVector, apply_vector
from .scheme import BaseScheme

# Standard-universe gravitational coupling alpha_G ~ 5.9e-39, used to centre the
# anthropic stellar window.
_ALPHA_G0 = 5.9e-39


def _falling(value: float, threshold: float, width_decades: float = 1.0) -> float:
    """Smooth 1->0 step as ``value`` rises through ``threshold`` (log space)."""

    if value <= 0:
        return 1.0
    return 1.0 / (1.0 + math.exp((math.log10(value) - math.log10(threshold)) / width_decades))


class SchemeC(BaseScheme):
    name = "C:minimal-axiom-dimensional"

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
        cfg = apply_vector(self.base_config, vector)
        n = self._numbers(vector)
        alpha, alpha_g = n["alpha"], n["alpha_G"]
        cc = cfg.dimensionless.cosmological_constant_scale
        amp = math.sqrt(max(cfg.cosmology.primordial_amplitude, 0.0))

        # --- minimal anthropic margins ---
        # 1. atoms: alpha bound & non-relativistic.
        m_atoms = logistic_window(alpha, lo=1e-3, hi=0.1)
        # 2. stars contain many nucleons: N* ~ alpha_G^-3/2 large -> alpha_G small.
        n_star = alpha_g ** (-1.5)
        m_stars = logistic_window(n_star, lo=1e48, hi=1e63)
        # 3. Carr-Rees hierarchy: gravitating objects >> atoms.
        hierarchy = math.sqrt(alpha_g) / max(alpha, 1e-12)
        m_hierarchy = _falling(hierarchy, threshold=1e-8, width_decades=1.5)
        # 4. minimal cosmology: Lambda must not preclude bound structure; need seeds.
        m_lambda = _falling(cc, threshold=12.0, width_decades=0.5)
        m_seeds = logistic_window(max(amp, 1e-12), lo=1e-6, hi=3e-4)

        margins = {
            "atoms": m_atoms,
            "stars": m_stars,
            "hierarchy": m_hierarchy,
            "lambda": m_lambda,
            "seeds": m_seeds,
        }
        # minimal-axiom score: geometric mean (a single weak link sinks it).
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
            },
            warnings=warnings,
        )

    def base_score(self, vector: ParameterVector) -> float:
        return self.assess(vector).score

    def optimize(self, start: ParameterVector, budget: int = 60) -> ParameterVector:
        best = start.copy()
        best_val = self.objective(best)
        evals = 0
        step = 0.2
        while evals < budget and step > 1e-3:
            improved = False
            base = best.to_normalized()
            for i in range(len(AXES)):
                for sign in (+1.0, -1.0):
                    probe = list(base)
                    probe[i] = min(1.0, max(0.0, probe[i] + sign * step))
                    cand = ParameterVector.from_normalized(probe)
                    val = self.objective(cand)
                    evals += 1
                    if val > best_val + 1e-9:
                        best, best_val, base = cand, val, probe
                        improved = True
                    if evals >= budget:
                        break
                if evals >= budget:
                    break
            if not improved:
                step *= 0.5
        self.last_champion = best
        return best
