# Physics model notes

QuantaEngine v0.1 is a first executable scaffold for the “创世” idea: a generated universe should start from tunable microscopic physics and evolve toward macroscopic structure.

## Current model

The current model combines:

1. a primordial random field,
2. optional chaotic microscopic modulation,
3. a Friedmann-like expansion background,
4. a periodic scalar-field lattice,
5. energy-density diagnostics and power-spectrum diagnostics.

## Equations currently implemented

Background expansion uses dimensionless Hubble-time units:

```text
E(a)^2 = Ωr/a^4 + Ωm/a^3 + Ωk/a^2 + ΩΛ
adot = a E(a)
```

Field dynamics uses:

```text
φdot = π
πdot = ∇²φ/a² - dV/dφ - 3 H π
V(φ) = 1/2 m²φ² + 1/4 λφ⁴
```

Energy density is estimated as:

```text
ρ = 1/2 π² + 1/2 |∇φ|²/a² + V(φ)
```

## Why this model is useful

It is small enough to understand, hack, and test. It also establishes the software pattern needed for the larger project:

- define laws,
- seed microscopic fluctuations,
- evolve fields,
- couple to background geometry,
- measure emergent macroscopic structure,
- scan parameters.

## What should come next

A serious roadmap should add physically validated modules step by step:

- natural-unit and SI-unit conversion layer,
- gauge-field lattice kernels,
- multiple scalar fields and symmetry breaking,
- quantum effective potentials,
- inflation/reheating-inspired scenarios,
- particle-production modules,
- N-body structure formation,
- validation against known cosmological benchmarks,
- GPU acceleration.
