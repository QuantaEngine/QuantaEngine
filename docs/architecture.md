# QuantaEngine architecture

QuantaEngine is organized around the idea that a universe can be generated from a compact specification of laws, constants, fields, and initial conditions.

## Layers

## 1. Parameter layer

`UniverseParams` is the reproducibility contract. Every generated universe should be reconstructable from:

- random seed,
- numerical geometry,
- cosmological density terms,
- primordial fluctuation controls,
- microscopic chaos controls,
- effective field controls,
- future-facing particle/interaction constants.

## 2. Initial condition layer

`spectrum.py` creates a Gaussian field with a tunable spectrum-like shape. `chaos.py` adds a controlled microscopic chaos component.

## 3. Background layer

`cosmology.py` evolves a Friedmann-like background in dimensionless Hubble-time units:

```text
H(a)^2 = Ωr/a^4 + Ωm/a^3 + Ωk/a^2 + ΩΛ
```

## 4. Field layer

`fields.py` evolves a scalar field on a periodic lattice:

```text
φ¨ + 3 H φ˙ - ∇²φ/a² + dV/dφ = 0
V(φ) = 1/2 m² φ² + 1/4 λ φ⁴
```

This is a toy kernel. It exists to make the architecture executable and testable, not to claim production cosmological accuracy.

## 5. Engine layer

`engine.py` connects parameters, initial conditions, background evolution, field evolution, observables, snapshots, and saving.

## 6. Extension layer

Future modules can add:

- gauge fields,
- multi-field inflation-like models,
- phase transitions,
- particle production,
- baryogenesis-like effective modules,
- N-body gravity,
- hydrodynamics,
- synthetic observations,
- differentiable/AI optimization.

## 7. LawBook layer

`laws.py` introduces a structured `LawBook` with constants, fields, couplings, and symmetries. In v0.1, it maps conservatively into `UniverseParams`; in future versions, it should become the main entry point for defining generated universes from effective actions and microscopic rules.
