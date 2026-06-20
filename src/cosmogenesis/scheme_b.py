"""Scheme B: variational self-consistency field relaxation (fully independent).

Philosophy: a universe is a FIXED POINT of coupled physical constraints, not a
forward pass. Emergent scales are obtained by extremizing balance functionals;
soft logistic windows replace hard booleans; and crucially a global
self-consistency RESIDUAL is computed across layers and a small fixed-point
iteration is relaxed to convergence. A universe where every individual window
passes can still be rejected for high residual or non-convergence -- something
Scheme A's single forward pass cannot detect.

Optimizer: a (mu+lambda) evolution strategy (CMA-lite) over the shared vector,
maximizing softmin(margins) * exp(-lambda * residual). Stochastic and
coupling-aware, by design the opposite of A's deterministic coordinate ascent.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from quanta_engine.core.schema import UniverseConfig
from quanta_engine.core.units import JULIAN_YEAR_S, MEGAPARSEC_M

from .assessment import UniverseAssessment, logistic_window, softmin
from .critique import Critique, descend_residual, fragility_profile
from .parameters import ParameterVector, apply_vector
from .scheme import BaseScheme

# Standard-universe reference values used to calibrate the soft windows so the
# real universe lands near the top of the feasibility landscape.
_ALPHA0 = 0.0072973525693


@dataclass(slots=True)
class _Emergent:
    """Quantities Scheme B derives from first principles for one universe."""

    binding_eV: float
    bohr_radius_m: float
    nuclear_margin: float
    ignition_margin: float
    stellar_lifetime_years: float
    age_years: float
    amplitude: float
    margins: dict[str, float]
    residual_terms: dict[str, float]
    relax_converged: bool


class SchemeB(BaseScheme):
    name = "B:variational-selfconsistency"

    def __init__(self, base_config: UniverseConfig, seed: int = 7) -> None:
        super().__init__(base_config)
        self._rng = np.random.default_rng(seed)
        self._rival = None  # type: ignore[var-annotated]
        self._residual_lambda = 2.0

    # ---------- physics from first principles ----------
    def _derive(self, vector: ParameterVector) -> _Emergent:
        cfg = apply_vector(self.base_config, vector)
        k = cfg.constants
        d = cfg.dimensionless
        p = cfg.particles
        cos = cfg.cosmology

        alpha = d.alpha * d.alpha_scale
        g_scale = d.gravity_scale
        strong = d.strong_scale
        cc = d.cosmological_constant_scale

        # --- atomic scale by energy extremization: E(r)=h^2/(2 mu r^2)-alpha hc/r ---
        mu_MeV = (p.electron_mass_MeV * p.proton_mass_MeV) / (
            p.electron_mass_MeV + p.proton_mass_MeV
        )
        mu_J = mu_MeV * 1e6 * 1.602176634e-19  # MeV -> J (rest energy)
        # E_b = 1/2 mu c^2 alpha^2 ; mu c^2 already in J as mu_J.
        binding_J = 0.5 * mu_J * alpha**2
        binding_eV = binding_J / 1.602176634e-19
        bohr = k.hbar / (max(mu_J, 1e-40) / k.c**2 * k.c * max(alpha, 1e-9))

        # --- soft windows (logistic, not boolean) ---
        atomic_margin = logistic_window(binding_eV, lo=1.0, hi=120.0)
        # relativistic ceiling: penalize alpha approaching 1.
        relativistic = 1.0 / (1.0 + math.exp((alpha - 0.5) / 0.05))
        atomic = atomic_margin * relativistic

        # nuclear: strong attraction vs EM repulsion -> a band in strong_scale.
        eff_strong = strong - 0.08 * (alpha / _ALPHA0 - 1.0)
        nuclear = logistic_window(max(eff_strong, 1e-6), lo=0.8, hi=1.45, width_frac=0.25)

        # --- stellar self-consistency: virial core temp & Gamow ignition ---
        # Hotter cores with stronger gravity ignite fusion; lifetime ~ g^-2.
        ignition = 1.0 / (1.0 + math.exp(-(math.log10(g_scale) + 1.4) / 0.4))
        lifetime_years = 1.0e10 * g_scale**-2.0 * (alpha / _ALPHA0) ** 0.5
        lifetime_margin = logistic_window(lifetime_years, lo=1.0e9, hi=1.0e13)

        # --- cosmology: exact flat matter+Lambda age, independently derived ---
        omega_m = max(cos.omega_b + cos.omega_cdm, 1e-6)
        omega_lambda = max(cos.omega_lambda * cc, 1e-9)
        h0_per_s = abs(cos.H0_km_s_Mpc) * 1000.0 / MEGAPARSEC_M
        # flat LambdaCDM closed-form: t = 2/(3 H0 sqrt(OL)) asinh( sqrt(OL/OM) )
        age_s = (2.0 / (3.0 * h0_per_s * math.sqrt(omega_lambda))) * math.asinh(
            math.sqrt(omega_lambda / omega_m)
        )
        age_years = age_s / JULIAN_YEAR_S

        amplitude = math.sqrt(max(cos.primordial_amplitude, 0.0))
        # structure growth suppressed once Lambda dominates early.
        supp = 1.0 / (1.0 + omega_lambda / omega_m)
        amp_eff = amplitude * supp * 8.0  # calibration toward order-unity collapse
        structure = logistic_window(max(amplitude, 1e-12), lo=1e-6, hi=3e-4)

        margins = {
            "atomic": atomic,
            "nuclear": nuclear,
            "ignition": ignition,
            "lifetime": lifetime_margin,
            "structure": structure,
            "age": logistic_window(age_years, lo=2e9, hi=5e10),
        }

        # ---------- cross-layer self-consistency residuals (A never does this) ----------
        omega_r = max(cos.omega_r, 0.0)
        curvature = cfg.spacetime.curvature_k or 0.0
        r_flat = abs(omega_m + omega_lambda + omega_r + curvature - 1.0)
        # stars and a structure-formation epoch must fit inside the age.
        needed = max(cfg.stellar.min_lifetime_years_for_complexity, lifetime_years * 0.3)
        r_time = max(0.0, (needed - age_years) / max(needed, 1.0))
        # chemistry must survive ambient thermal energy of a temperate planet.
        e_thermal_eV = 1.380649e-23 * 300.0 / 1.602176634e-19
        r_chem = max(0.0, (e_thermal_eV - binding_eV) / max(binding_eV, 1e-9))

        # ---------- fixed-point relaxation of emergent state ----------
        # x = [metallicity Z, structure amplitude S, lifetime fraction L]
        z, s, lf = 0.1, max(amp_eff, 1e-6), lifetime_margin
        converged = False
        last = math.inf
        for _ in range(64):
            z_new = 0.6 * ignition * nuclear * s
            s_new = structure * omega_m * (1.0 + 0.2 * z)
            l_new = lifetime_margin
            delta = abs(z_new - z) + abs(s_new - s) + abs(l_new - lf)
            z, s, lf = z_new, s_new, l_new
            if delta < 1e-6:
                converged = True
                break
            if delta > last + 1.0:  # diverging
                break
            last = delta
        r_relax = 0.0 if converged else 0.5

        residual_terms = {
            "flatness": r_flat,
            "time_budget": r_time,
            "chemistry_thermal": r_chem,
            "relaxation": r_relax,
        }
        return _Emergent(
            binding_eV=binding_eV,
            bohr_radius_m=bohr,
            nuclear_margin=nuclear,
            ignition_margin=ignition,
            stellar_lifetime_years=lifetime_years,
            age_years=age_years,
            amplitude=amplitude,
            margins=margins,
            residual_terms=residual_terms,
            relax_converged=converged,
        )

    # ---------- entry point ----------
    def assess(self, vector: ParameterVector) -> UniverseAssessment:
        e = self._derive(vector)
        residual = sum(e.residual_terms.values())
        base_margin = softmin(list(e.margins.values()))
        score = base_margin * math.exp(-self._residual_lambda * residual)
        warnings = []
        if not e.relax_converged:
            warnings.append("self-consistency relaxation did not converge (internally inconsistent)")
        for name, val in e.residual_terms.items():
            if val > 0.05:
                warnings.append(f"high self-consistency residual: {name}={val:.3f}")
        return UniverseAssessment(
            scheme=self.name,
            score=score,
            feasible=score > 0.5 and e.relax_converged,
            margins=e.margins,
            residual=residual,
            diagnostics={
                "binding_eV": e.binding_eV,
                "stellar_lifetime_years": e.stellar_lifetime_years,
                "age_years": e.age_years,
                "amplitude": e.amplitude,
                "residual_terms": e.residual_terms,
                "relax_converged": e.relax_converged,
            },
            warnings=warnings,
        )

    def residual(self, vector: ParameterVector) -> float:
        return self.assess(vector).residual

    def base_score(self, vector: ParameterVector) -> float:
        return self.assess(vector).score

    def penalty_value(self, vector: ParameterVector) -> float:
        total = 0.0
        w_hard = self.penalties.get("hard_window", 0.0)
        if w_hard and self._rival is not None:
            total += w_hard * self._rival.hard_window_failures(vector)
        w_rob = self.penalties.get("robustness", 0.0)
        if w_rob:
            profile = fragility_profile(vector, self.base_score)
            total += w_rob * max(profile.values())
        return total

    # ---------- optimizer: (mu+lambda) evolution strategy ----------
    def optimize(self, start: ParameterVector, budget: int = 80) -> ParameterVector:
        dim = len(start.values)
        mean = np.array(start.to_normalized(), dtype=float)
        sigma = 0.22
        lam = 10
        mu = 4
        best_vec = start.copy()
        best_val = self.objective(best_vec)
        evals = 0
        while evals < budget:
            samples = []
            for _ in range(lam):
                child = np.clip(mean + sigma * self._rng.standard_normal(dim), 0.0, 1.0)
                vec = ParameterVector.from_normalized(list(child))
                val = self.objective(vec)
                evals += 1
                samples.append((val, child, vec))
                if val > best_val:
                    best_val, best_vec = val, vec
                if evals >= budget:
                    break
            samples.sort(key=lambda t: t[0], reverse=True)
            elites = samples[: min(mu, len(samples))]
            mean = np.mean([c for _, c, _ in elites], axis=0)
            # cool toward exploitation but keep a floor so the search can still
            # escape local self-consistency basins across rounds.
            sigma = max(sigma * 0.9, 0.05)
        self.last_champion = best_vec
        return best_vec

    # ---------- critique of Scheme A's champion ----------
    def critique(self, rival_champion: ParameterVector, rival) -> Critique:
        assessment = self.assess(rival_champion)
        terms = assessment.diagnostics["residual_terms"]
        dominant = max(terms, key=terms.get)
        severity = min(1.0, terms[dominant] * 4.0)
        improved, axis = descend_residual(rival_champion, self.residual)
        weakness = (
            f"A's champion has self-consistency residual {assessment.residual:.3f} "
            f"(dominant term '{dominant}'={terms[dominant]:.3f}); A's forward pass never "
            f"checks cross-layer consistency. Reducing it favors moving along '{axis}'."
        )
        return Critique(
            critic=self.name,
            target=rival.name,
            weakness=weakness,
            severity=severity,
            evidence={"residual_terms": terms, "relax_converged": assessment.diagnostics["relax_converged"]},
            suggestion=improved,
            penalty="residual",
        )

    # ---------- consider A's critique of B ----------
    def consider(self, critique: Critique, rival=None) -> bool:
        """A asks B to respect A's hard windows and stop being fragile. Adopt iff
        B can satisfy them without destroying its own objective."""

        if rival is None:
            return False
        before = self.base_score(self.last_champion)
        self._rival = rival
        self.penalties["hard_window"] = 0.3
        self.penalties["robustness"] = 0.2
        candidate = self.optimize(self.last_champion, budget=60)
        after = self.base_score(candidate)
        if after >= before - 0.05:
            self.last_champion = candidate
            return True
        self.penalties.pop("hard_window", None)
        self.penalties.pop("robustness", None)
        return False
