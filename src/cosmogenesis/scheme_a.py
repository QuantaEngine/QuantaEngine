"""Scheme A: the analytic forward-pass compiler (wraps quanta_engine).

Philosophy: transparent closed-form layers, hard windows, white-box sensitivity.
Optimizer: deterministic coordinate-ascent guided by finite-difference sensitivity
(the natural extension of quanta_engine's existing scan + normalized_sensitivity).
Critique of B: fragility / robustness analysis of B's champion under A's score.
"""

from __future__ import annotations

from quanta_engine.core.schema import UniverseConfig
from quanta_engine.pipeline import run_universe_pipeline

from .assessment import UniverseAssessment
from .critique import Critique, fragility_profile, nudge_toward
from .parameters import AXES, ParameterVector, apply_vector
from .scheme import BaseScheme


class SchemeA(BaseScheme):
    name = "A:analytic-compiler"

    def __init__(self, base_config: UniverseConfig) -> None:
        super().__init__(base_config)
        # Set when A accepts B's critique: penalize B's self-consistency residual.
        self._rival_residual = None  # type: ignore[var-annotated]

    # ---- core entry point (same shape as run_universe_pipeline) ----
    def assess(self, vector: ParameterVector) -> UniverseAssessment:
        config = apply_vector(self.base_config, vector)
        report = run_universe_pipeline(config)
        c = report.complexity_report
        margins = {
            "chemistry": c.chemistry_score,
            "energy": c.energy_gradient_score,
            "stability": c.stability_score,
            "elements": c.element_diversity_score,
            "life": c.life_window_score,
            "civilization": c.civilization_potential_score,
        }
        warnings = list(report.validation_report.errors)
        for rep in (
            report.atomic_report,
            report.nuclear_report,
            report.cosmology_report,
            report.stellar_report,
            report.structure_report,
        ):
            warnings.extend(getattr(rep, "warnings", []))
        return UniverseAssessment(
            scheme=self.name,
            score=c.civilization_potential_score,
            feasible=report.validation_report.passed and report.final_verdict != "sterile",
            margins=margins,
            residual=0.0,  # A performs no cross-layer self-consistency check
            diagnostics={
                "verdict": report.final_verdict,
                "stable_hydrogen": report.atomic_report.stable_hydrogen,
                "deuteron_stable": report.nuclear_report.deuteron_stable,
                "helium4_stable": report.nuclear_report.helium4_stable,
                "fusion": report.stellar_report.hydrogen_fusion_possible,
                "long_lived_stars": report.stellar_report.long_lived_stars_possible,
                "stellar_lifetime_years": report.stellar_report.characteristic_stellar_lifetime_years,
                "age_Gyr": report.cosmology_report.age_of_universe_Gyr,
                "structure": report.structure_report.structure_growth_possible,
                "planets": report.structure_report.planet_formation_possible,
                "hard_window_failures": self._hard_failures(report),
            },
            warnings=warnings,
        )

    @staticmethod
    def _hard_failures(report) -> float:
        windows = [
            report.atomic_report.stable_hydrogen,
            report.nuclear_report.deuteron_stable,
            report.nuclear_report.helium4_stable,
            report.stellar_report.hydrogen_fusion_possible,
            report.stellar_report.long_lived_stars_possible,
            report.structure_report.structure_growth_possible,
            report.structure_report.planet_formation_possible,
        ]
        return 1.0 - sum(bool(w) for w in windows) / len(windows)

    def hard_window_failures(self, vector: ParameterVector) -> float:
        """Fraction of A's hard windows that fail — used as B's imposed penalty."""

        return float(self.assess(vector).diagnostics["hard_window_failures"])

    def base_score(self, vector: ParameterVector) -> float:
        return self.assess(vector).score

    def penalty_value(self, vector: ParameterVector) -> float:
        total = 0.0
        w = self.penalties.get("residual", 0.0)
        if w and self._rival_residual is not None:
            total += w * self._rival_residual(vector)
        return total

    # ---- optimizer: finite-difference coordinate ascent ----
    def optimize(self, start: ParameterVector, budget: int = 60) -> ParameterVector:
        best = start.copy()
        best_val = self.objective(best)
        step = 0.18  # normalized step
        evals = 0
        while evals < budget and step > 1e-3:
            improved = False
            normalized = best.to_normalized()
            for i in range(len(AXES)):
                for sign in (+1.0, -1.0):
                    probe = list(normalized)
                    probe[i] = min(1.0, max(0.0, probe[i] + sign * step))
                    cand = ParameterVector.from_normalized(probe)
                    val = self.objective(cand)
                    evals += 1
                    if val > best_val + 1e-9:
                        best, best_val, normalized = cand, val, probe
                        improved = True
                    if evals >= budget:
                        break
                if evals >= budget:
                    break
            if not improved:
                step *= 0.5
        self.last_champion = best
        return best

    # ---- critique of Scheme B's champion ----
    def critique(self, rival_champion: ParameterVector, rival) -> Critique:
        profile = fragility_profile(rival_champion, self.base_score)
        fragile_axis = max(profile, key=profile.get)
        severity = min(1.0, profile[fragile_axis])
        assessment = self.assess(rival_champion)
        # Windows B's soft margins tolerated but A's hard logic rejects.
        glossed = [w for w in assessment.warnings if w]
        suggestion = nudge_toward(
            rival_champion, self.last_champion, fragile_axis, fraction=0.5
        )
        weakness = (
            f"B's champion is fragile along '{fragile_axis}' "
            f"(score drops {profile[fragile_axis]*100:.0f}% under a 5% perturbation); "
            f"{len(glossed)} hard-window warning(s) B's soft margins glossed over."
        )
        return Critique(
            critic=self.name,
            target=rival.name,
            weakness=weakness,
            severity=severity,
            evidence={"fragility_profile": profile, "hard_warnings": glossed[:5]},
            suggestion=suggestion,
            penalty="robustness+hard_window",
        )

    # ---- consider B's critique of A ----
    def consider(self, critique: Critique, rival=None) -> bool:
        """B asks A to regularize its self-consistency residual. Adopt iff it does
        not destroy A's own objective at A's current champion."""

        if rival is None or critique.penalty is None:
            return False
        before = self.base_score(self.last_champion)
        # Tentatively wire B's residual as a penalty and test on A's champion.
        self._rival_residual = lambda v: rival.assess(v).residual
        trial_weight = 0.25
        self.penalties["residual"] = trial_weight
        # Re-optimize briefly to see if A can satisfy both.
        candidate = self.optimize(self.last_champion, budget=40)
        after = self.base_score(candidate)
        if after >= before - 0.05:  # tolerate a small dip for better self-consistency
            self.last_champion = candidate
            return True
        # Reject: roll back the penalty.
        self.penalties.pop("residual", None)
        self._rival_residual = None
        return False
