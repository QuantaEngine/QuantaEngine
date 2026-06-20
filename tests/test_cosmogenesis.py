"""Tests for the adversarial cosmogenesis meta-layer."""

from __future__ import annotations

import math

import pytest

from cosmogenesis import (
    ParameterVector,
    SchemeA,
    SchemeB,
    apply_vector,
    run_adversarial,
    vector_from_config,
)
from cosmogenesis.assessment import logistic_window, softmin
from cosmogenesis.parameters import NDIM
from quanta_engine.core.schema import load_config

CONFIG = "configs/standard_universe.yaml"


@pytest.fixture(scope="module")
def base_config():
    return load_config(CONFIG)


# ---------------- parameter vector ----------------
def test_vector_config_roundtrip(base_config):
    v = vector_from_config(base_config)
    assert len(v.values) == NDIM
    cfg = apply_vector(base_config, v)
    assert cfg.dimensionless.alpha_scale == pytest.approx(base_config.dimensionless.alpha_scale)
    assert cfg.cosmology.primordial_amplitude == pytest.approx(
        base_config.cosmology.primordial_amplitude, rel=1e-6
    )


def test_normalized_roundtrip():
    v = ParameterVector([1.2, 5.0, 1.1, 2.0, -8.0])
    back = ParameterVector.from_normalized(v.to_normalized())
    assert back.values == pytest.approx(v.values, rel=1e-9)


def test_apply_vector_changes_config(base_config):
    v = vector_from_config(base_config)
    v.values[1] = 10.0  # gravity_scale
    cfg = apply_vector(base_config, v)
    assert cfg.dimensionless.gravity_scale == pytest.approx(10.0)
    # base config untouched (deep copy)
    assert base_config.dimensionless.gravity_scale == pytest.approx(1.0)


# ---------------- helpers ----------------
def test_logistic_window_inside_outside():
    assert logistic_window(13.6, 1.0, 120.0) > 0.8
    assert logistic_window(1e-3, 1.0, 120.0) < 0.1
    assert logistic_window(1e5, 1.0, 120.0) < 0.1


def test_softmin_dominated_by_worst():
    assert softmin([1.0, 1.0, 0.1]) < 0.3
    assert softmin([0.9, 0.95, 0.92]) > 0.7


# ---------------- Scheme A ----------------
def test_scheme_a_standard_high(base_config):
    a = SchemeA(base_config)
    v = vector_from_config(base_config)
    out = a.assess(v)
    assert out.feasible
    assert out.score > 0.9
    assert out.residual == 0.0


# ---------------- Scheme B ----------------
def test_scheme_b_standard_consistent(base_config):
    b = SchemeB(base_config)
    v = vector_from_config(base_config)
    out = b.assess(v)
    assert out.score > 0.5
    assert out.residual < 0.01
    assert out.diagnostics["relax_converged"]
    # independently derived age near 13.8 Gyr
    assert out.diagnostics["age_years"] / 1e9 == pytest.approx(13.8, abs=1.0)


def test_scheme_b_detects_inconsistency(base_config):
    """A universe that passes naive windows can still be flagged inconsistent."""
    b = SchemeB(base_config)
    # huge cosmological constant breaks flatness AND shortens the age below the
    # time needed for a stellar generation -> large residual.
    broken = ParameterVector([1.0, 1.0, 1.0, 40.0, -8.0])
    out = b.assess(broken)
    assert out.residual > 0.1
    assert not out.feasible


def test_scheme_b_shorter_age_for_large_lambda(base_config):
    b = SchemeB(base_config)
    young = b.assess(ParameterVector([1.0, 1.0, 1.0, 30.0, -8.0])).diagnostics["age_years"]
    old = b.assess(ParameterVector([1.0, 1.0, 1.0, 1.0, -8.0])).diagnostics["age_years"]
    assert young < old


# ---------------- optimizers ----------------
def test_scheme_a_optimizer_improves(base_config):
    a = SchemeA(base_config)
    poor = ParameterVector([0.5, 12.0, 1.0, 5.0, -7.5])
    before = a.objective(poor)
    champ = a.optimize(poor, budget=60)
    assert a.objective(champ) >= before


def test_scheme_b_optimizer_improves(base_config):
    b = SchemeB(base_config)
    poor = ParameterVector([0.5, 12.0, 1.6, 8.0, -7.5])
    before = b.objective(poor)
    champ = b.optimize(poor, budget=80)
    assert b.objective(champ) >= before


# ---------------- shared entry point ----------------
def test_both_schemes_consume_same_vector(base_config):
    v = ParameterVector([1.1, 1.0, 1.0, 1.0, -8.5])
    a_out = SchemeA(base_config).assess(v)
    b_out = SchemeB(base_config).assess(v)
    assert 0.0 <= a_out.score <= 1.0
    assert 0.0 <= b_out.score <= 1.0


# ---------------- critique + consider ----------------
def test_mutual_critique(base_config):
    a, b = SchemeA(base_config), SchemeB(base_config)
    v = vector_from_config(base_config)
    a.last_champion = v.copy()
    b.last_champion = v.copy()
    crit_a = a.critique(b.last_champion, b)
    crit_b = b.critique(a.last_champion, a)
    assert crit_a.critic == a.name and crit_a.target == b.name
    assert crit_b.critic == b.name and crit_b.target == a.name
    assert crit_a.suggestion is not None
    assert isinstance(a.consider(crit_b, rival=b), bool)
    assert isinstance(b.consider(crit_a, rival=a), bool)


# ---------------- end-to-end arena ----------------
def test_run_adversarial_end_to_end(base_config, tmp_path):
    result = run_adversarial(base_config, rounds=3, out_dir=tmp_path, seed=1, budget=40)
    assert len(result.rounds) >= 1
    assert len(result.consensus_vector) == NDIM
    assert 0.0 <= result.consensus_score_a <= 1.0
    assert 0.0 <= result.consensus_score_b <= 1.0
    assert (tmp_path / "arena_report.md").exists()
    assert (tmp_path / "arena_result.json").exists()
    assert (tmp_path / "consensus_universe.yaml").exists()


def test_adversarial_repairs_broken_universe(base_config):
    """From a broken start, both schemes should raise their own objective."""
    broken = ParameterVector([0.4, 25.0, 1.6, 18.0, -7.2])
    a0 = SchemeA(base_config).assess(broken).score
    b0 = SchemeB(base_config).assess(broken).score
    result = run_adversarial(base_config, rounds=6, seed=3, budget=90, start=broken)
    assert result.rounds[-1].score_a_on_a > a0
    assert result.rounds[-1].score_b_on_b > b0


def test_consensus_yaml_is_loadable(base_config, tmp_path):
    run_adversarial(base_config, rounds=2, out_dir=tmp_path, seed=2, budget=30)
    cfg = load_config(str(tmp_path / "consensus_universe.yaml"))
    assert math.isfinite(cfg.dimensionless.alpha_scale)
