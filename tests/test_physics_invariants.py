"""Property-based physics invariants for the effective universe models."""

from __future__ import annotations

import math

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from cosmogenesis.core import ParameterVector
from cosmogenesis.schemes import build_scheme
from quanta_engine.atomic.hydrogen import compute_hydrogen_properties
from quanta_engine.core.schema import load_config
from quanta_engine.core.units import J_to_eV, MeV_to_kg, eV_to_J, kg_to_MeV, year_to_second
from quanta_engine.pipeline import run_universe_pipeline
from quanta_engine.stars.lifetime import characteristic_lifetime_years
from quanta_engine.validation.conservation import density_budget

CONFIG = "configs/standard_universe.yaml"


@settings(max_examples=40, deadline=None)
@given(st.floats(min_value=1.0e-12, max_value=1.0e12, allow_nan=False, allow_infinity=False))
def test_energy_and_mass_unit_roundtrips(value: float):
    assert J_to_eV(eV_to_J(value)) == pytest.approx(value, rel=1e-12)
    assert kg_to_MeV(MeV_to_kg(value)) == pytest.approx(value, rel=1e-12)
    assert year_to_second(value) > 0.0


@settings(max_examples=30, deadline=None)
@given(
    omega_r=st.floats(min_value=0.0, max_value=0.05, allow_nan=False),
    omega_b=st.floats(min_value=0.01, max_value=0.2, allow_nan=False),
    omega_cdm=st.floats(min_value=0.05, max_value=0.5, allow_nan=False),
)
def test_density_budget_is_conserved_for_flat_universes(
    omega_r: float, omega_b: float, omega_cdm: float
):
    cfg = load_config(CONFIG)
    cfg.cosmology.omega_r = omega_r
    cfg.cosmology.omega_b = omega_b
    cfg.cosmology.omega_cdm = omega_cdm
    cfg.cosmology.omega_lambda = 1.0 - omega_r - omega_b - omega_cdm
    cfg.spacetime.curvature_k = 0.0
    assert density_budget(cfg) == pytest.approx(1.0, abs=1e-12)


@settings(max_examples=30, deadline=None)
@given(
    weaker=st.floats(min_value=0.02, max_value=5.0, allow_nan=False),
    ratio=st.floats(min_value=1.01, max_value=10.0, allow_nan=False),
)
def test_stronger_gravity_monotonically_shortens_stellar_lifetime(weaker: float, ratio: float):
    cfg = load_config(CONFIG)
    cfg.dimensionless.gravity_scale = weaker
    long_lifetime = characteristic_lifetime_years(cfg)
    cfg.dimensionless.gravity_scale = weaker * ratio
    short_lifetime = characteristic_lifetime_years(cfg)
    assert short_lifetime < long_lifetime


@settings(max_examples=30, deadline=None)
@given(
    lower=st.floats(min_value=0.3, max_value=1.4, allow_nan=False),
    ratio=st.floats(min_value=1.01, max_value=1.8, allow_nan=False),
)
def test_stronger_electromagnetism_tightens_hydrogen_monotonically(lower: float, ratio: float):
    upper = min(lower * ratio, 2.8)
    cfg = load_config(CONFIG)
    cfg.dimensionless.alpha_scale = lower
    low = compute_hydrogen_properties(cfg)
    cfg.dimensionless.alpha_scale = upper
    high = compute_hydrogen_properties(cfg)
    assert high.binding_energy_eV >= low.binding_energy_eV
    assert high.bohr_radius_m <= low.bohr_radius_m


def test_standard_universe_anchor_properties():
    report = run_universe_pipeline(CONFIG)
    assert 13.5 <= report.atomic_report.binding_energy_eV <= 13.7
    assert 5.2e-11 <= report.atomic_report.bohr_radius_m <= 5.4e-11
    assert 13.0 <= report.cosmology_report.age_of_universe_Gyr <= 14.5
    assert math.isclose(density_budget(report.config), 1.0, abs_tol=1.0e-3)

    cfg = load_config(CONFIG)
    expected = {
        "analytic_compiler": (0.98, 1.0),
        "variational_relaxer": (0.82, 0.90),
        "minimal_axiom": (0.88, 0.96),
    }
    for name, bounds in expected.items():
        score = build_scheme(name, cfg).assess(ParameterVector.default()).score
        assert bounds[0] <= score <= bounds[1]
