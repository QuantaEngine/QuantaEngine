"""Phase A regression tests for remediation round B (QE-2026-101, QE-2026-102).

QE-2026-101: each scheme independently reconsiders a rival's suggestion under its
OWN objective and adopts it only if it independently verifies an improvement --
never blindly, never merged.
QE-2026-102: scoring objectives are engine-derived/measured, not self-declared in
theory.yaml.
"""

from __future__ import annotations

import pytest

from cosmogenesis.arena import bridge, scoring
from cosmogenesis.arena.registry import TheoryRegistry
from cosmogenesis.core import ParameterVector
from cosmogenesis.schemes import build_scheme
from quanta_engine.core.schema import load_config

CONFIG = "configs/standard_universe.yaml"


@pytest.fixture(scope="module")
def cfg():
    return load_config(CONFIG)


@pytest.fixture
def registry():
    return TheoryRegistry.from_dir("theories")


# ---------------- QE-2026-101: independent consider loop ----------------
def test_suggestion_adopted_when_self_verified_improvement(cfg):
    engine = build_scheme("analytic_compiler", cfg)
    poor = ParameterVector([0.5, 12.0, 1.0, 5.0, -7.5])  # low own score
    good = ParameterVector.default()  # standard universe, high own score
    decision = engine.consider(poor, good)
    assert decision.adopt is True
    assert decision.own_after > decision.own_before
    # the adopted champion is at least as good (under our OWN objective) as the suggestion
    assert engine.objective(decision.champion) >= engine.objective(good) - 1e-9


def test_suggestion_rejected_when_no_self_verified_improvement(cfg):
    engine = build_scheme("analytic_compiler", cfg)
    good = ParameterVector.default()  # already near our own optimum
    bad = ParameterVector([3.0, 100.0, 2.0, 40.0, -11.0])  # clearly worse for us
    decision = engine.consider(good, bad)
    assert decision.adopt is False
    # rejecting keeps our OWN current champion -- never adopts a worse rival point
    assert decision.champion.values == good.values
    assert "no" in decision.reason.lower() or "keep" in decision.reason.lower()


def test_consider_is_deterministic(cfg):
    engine = build_scheme("analytic_compiler", cfg)
    poor = ParameterVector([0.5, 12.0, 1.0, 5.0, -7.5])
    good = ParameterVector.default()
    d1 = engine.consider(poor, good)
    d2 = build_scheme("analytic_compiler", cfg).consider(poor, good)
    assert d1.adopt == d2.adopt
    assert d1.champion.values == pytest.approx(d2.champion.values)


def test_bridge_consider_never_merges(registry):
    """Considering a rival's suggestion only updates the recipient's own champion."""
    target = registry.get("T-0001")
    rival_suggestion = ParameterVector([0.5, 12.0, 1.0, 5.0, -7.5])
    decision = bridge.consider(target, rival_suggestion)
    # decision concerns only the recipient; there is no merged theory.
    assert isinstance(decision.adopt, bool)
    assert len(decision.champion.values) == len(rival_suggestion.values)


def test_duel_records_independent_considerations(registry):
    from cosmogenesis.arena import run_duel

    rep = run_duel(registry.get("T-0001"), registry.get("T-0003"), registry, rounds=1)
    considered = [c for rd in rep.rounds for c in rd.considerations]
    # every recorded consideration is an independent verdict with before/after evidence
    for c in considered:
        assert c.target_theory_id and c.source_theory_id
        assert isinstance(c.adopted, bool)
        assert c.reason
    assert rep.allow_merge is False


# ---------------- QE-2026-102: measured, not declared ----------------
def test_efficiency_is_engine_derived_not_self_declared(cfg, registry):
    """computational_efficiency must come from the engine's actual cost, not from a
    gameable theory.yaml field."""
    theory = registry.get("T-0001")
    base = scoring.score_theory(theory).computational_efficiency
    # mutate the self-declared philosophy value; the score must NOT follow it.
    gamed = theory.model_copy(deep=True)
    gamed.philosophy.computational_efficiency = 0.01
    assert scoring.score_theory(gamed).computational_efficiency == pytest.approx(base)
    gamed.philosophy.computational_efficiency = 0.99
    assert scoring.score_theory(gamed).computational_efficiency == pytest.approx(base)


def test_efficiency_differs_across_paradigms(registry):
    effs = {t.engine: scoring.score_theory(t).computational_efficiency for t in registry.all()}
    # the minimal-axiom closed-form paradigm must be more efficient than the full
    # analytic pipeline -- a real, engine-derived trade-off.
    assert effs["minimal_axiom"] > effs["analytic_compiler"]


def test_simplicity_reflects_real_free_parameters(registry):
    simp = {t.engine: scoring.score_theory(t).simplicity for t in registry.all()}
    assert simp["minimal_axiom"] > simp["analytic_compiler"]


def test_compute_cost_present_in_diagnostics(cfg):
    for name in ("analytic_compiler", "variational_relaxer", "minimal_axiom"):
        out = build_scheme(name, cfg).assess(ParameterVector.default())
        assert "compute_cost" in out.diagnostics
        assert out.diagnostics["compute_cost"] > 0
        assert "free_parameters" in out.diagnostics
