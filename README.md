# QuantaEngine 创世

**QuantaEngine** is an open-source universe generation engine: a first-principles-inspired simulation framework that starts from tunable microscopic physics, seeds quantum-scale fluctuations, evolves fields and cosmic expansion, and lets users explore the emergence of macroscopic structure in generated universes.

> 中文名：**创世**  
> Tagline: **From fundamental quanta to generated universes.**

QuantaEngine is designed as a scientific-computing foundation rather than a visual toy. It borrows the spirit of Geant4-style modular physics simulation, but its first public version is intentionally compact: it provides a clean architecture, reproducible parameter files, a CLI, numerical kernels, tests, and extension points for future high-energy-physics, quantum-field, cosmology, and agent/AI modules.

## What this first version can do

- Define a universe through tunable physical and numerical parameters.
- Generate primordial Gaussian fluctuation fields from a power-spectrum-like model.
- Add controllable microscopic chaotic perturbations.
- Evolve a simplified Friedmann background with matter, radiation, curvature, and dark-energy terms.
- Evolve a scalar field on a periodic lattice with mass, self-coupling, gradient pressure, Hubble damping, and expansion.
- Save reproducible simulation outputs as `.npz` plus metadata JSON.
- Produce optional PNG maps of initial field, final field, and energy-density structure.
- Run from Python or the command line.
- Serve as a GitHub-ready seed repository for a much larger “生成宇宙” engine.

## What this version is not yet

This is **not** a validated replacement for Geant4, CLASS, CAMB, Gadget, Enzo, Athena++, or lattice-QFT production software. It is a research/prototyping scaffold for the larger idea: generating universes from tunable microscopic laws. The current equations are deliberately transparent and extensible, so future modules can replace the toy dynamics with validated physics.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
quantaengine run --config examples/minimal_universe.yaml --out runs/demo --steps 128 --snapshot-every 16 --plot
```

Then inspect:

```text
runs/demo/result.npz
runs/demo/metadata.json
runs/demo/initial_phi.png
runs/demo/final_phi.png
runs/demo/final_density.png
```

You can also run:

```bash
python scripts/quickstart.py
python scripts/parameter_scan.py
pytest
```

## Minimal Python API

```python
from quantaengine import UniverseParams, QuantaEngine

params = UniverseParams(
    name="demo-universe",
    seed=42,
    dimensions=2,
    grid_size=128,
    box_size=1.0,
    omega_m=0.315,
    omega_r=9.0e-5,
    omega_lambda=0.685,
    scalar_mass=0.2,
    self_coupling=0.05,
    primordial_rms=1.0e-3,
    chaos_strength=0.02,
)

engine = QuantaEngine(params)
result = engine.run(steps=128, snapshot_every=16)
print(result.summary())
```

## Repository layout

```text
quantaengine/
├── src/quantaengine/
│   ├── params.py          # Universe parameter dataclass and validation
│   ├── cosmology.py       # Friedmann-like background expansion
│   ├── spectrum.py        # primordial fluctuation generation
│   ├── chaos.py           # microscopic chaotic modulation
│   ├── fields.py          # scalar-field lattice state and evolution
│   ├── engine.py          # high-level simulation engine
│   ├── analysis.py        # observables and summary metrics
│   ├── visualize.py       # optional plotting helpers
│   ├── io.py              # config/result IO
│   └── cli.py             # command-line interface
├── examples/
├── scripts/
├── docs/
├── tests/
└── .github/workflows/
```

## Conceptual roadmap

QuantaEngine is intended to grow in layers:

1. **Law layer**: define constants, symmetries, fields, particles, interactions, and effective actions.
2. **Quantum layer**: generate fluctuations, vacuum structure, phase transitions, tunneling, and microscopic chaos.
3. **Field layer**: evolve classical/semiclassical fields on lattices.
4. **Cosmic layer**: couple fields to expansion, density perturbations, structure formation, and cosmic observables.
5. **Matter layer**: build particle/chemistry/effective-material emergence modules.
6. **Observation layer**: generate sky maps, spectra, structure catalogs, and synthetic experimental data.
7. **AI layer**: scan laws, optimize target universes, and learn inverse mappings from desired macroscopic outcomes to microscopic rules.

## Example configuration

```yaml
name: demo-universe
seed: 42
dimensions: 2
grid_size: 128
box_size: 1.0
omega_m: 0.315
omega_r: 0.00009
omega_lambda: 0.685
omega_k: 0.0
primordial_rms: 0.001
spectral_index: 0.965
chaos_strength: 0.02
scalar_mass: 0.2
self_coupling: 0.05
hubble_damping: 1.0
time_step: 0.01
initial_scale_factor: 0.01
```


## Detailed implementation plan

The repository now includes a detailed, issue-ready execution plan for evolving QuantaEngine into a Geant4-style modular physics engine. Start with:

- [CODE_EXECUTION_PLAN.md](CODE_EXECUTION_PLAN.md)
- [docs/IMPLEMENTATION_INDEX.md](docs/IMPLEMENTATION_INDEX.md)
- [docs/implementation/master_execution_checklist.md](docs/implementation/master_execution_checklist.md)
- [docs/design/geant4_style_architecture.md](docs/design/geant4_style_architecture.md)
- [docs/design/module_api_contracts.md](docs/design/module_api_contracts.md)
- [docs/implementation/physics_scale_roadmap.md](docs/implementation/physics_scale_roadmap.md)
- [docs/implementation/law_variation_protocol.md](docs/implementation/law_variation_protocol.md)
- [docs/validation/evidence_and_acceptance.md](docs/validation/evidence_and_acceptance.md)
- [docs/experiments/flagship_experiment_from_quanta_to_civilization.md](docs/experiments/flagship_experiment_from_quanta_to_civilization.md)

The long-term target is a configurable universe-generation toolkit where changing fundamental LawBooks can produce different microscopic rules, matter formation, cosmic structure, planetary environments, life probabilities, and civilization histories.

## Development philosophy

- Keep physics modules explicit and replaceable.
- Prefer dimensionless/natural-unit kernels internally unless a module explicitly requires SI units.
- Make every generated universe reproducible from a config file and seed.
- Separate conceptual physics assumptions from numerical implementation.
- Treat visual output as diagnostics, not as proof of physical validity.
- Add validation tests before claiming physical accuracy.

## License

MIT License. See [LICENSE](LICENSE).
