# QuantaEngine 创世

QuantaEngine is an open-source multi-scale physics compiler. It starts with fundamental constants, effective particle parameters, and cosmological initial conditions, then evaluates a universe layer by layer:

```text
configuration -> validation -> particles -> atoms -> nuclei -> cosmology
              -> stars -> structure -> complexity -> universe report
```

The MVP answers interpretable feasibility questions: whether hydrogen and light nuclei are stable, whether long-lived stars and heavy elements are possible, whether primordial structure can grow, and whether physical windows for complex chemistry, life, and civilization remain open.

## What It Is

- A typed, inheritable YAML configuration system.
- A modular toy + analytic effective-physics pipeline.
- A reproducible CLI for reports, comparisons, and parameter scans.
- A tested foundation that can later swap in higher-fidelity solvers.

## What It Is Not

QuantaEngine is not a full Standard Model derivation, BBN network, stellar-evolution code, N-body simulation, chemistry network, biological model, or prediction of life. Life-window and civilization-potential scores are physical-feasibility indicators, not probabilities.

## Install

Python 3.11 or newer is required.

```bash
python -m pip install -e ".[dev]"
quanta --version
python -m pytest
```

## Generate A Standard Universe

```bash
quanta validate-config configs/standard_universe.yaml
quanta run configs/standard_universe.yaml \
  --output reports/standard.md \
  --json reports/standard.json
```

Expected standard-universe checkpoints include hydrogen binding near `13.6 eV`, a Bohr radius near `5.29e-11 m`, an age near `13.8 Gyr`, stable light nuclei, long-lived stars, and a nonzero complexity window.

## Compare Universes

```bash
quanta compare \
  configs/standard_universe.yaml \
  configs/strong_alpha_universe.yaml
```

## Scan A Fundamental Parameter

```bash
quanta scan configs/standard_universe.yaml \
  --param dimensionless.alpha_scale \
  --values 0.5,0.8,1.0,1.2,1.5 \
  --output reports/scan_alpha.csv
```

The scan writes CSV data, a PNG score plot, and a Markdown summary.

## Python API

```python
from quanta_engine.pipeline import run_universe_pipeline

report = run_universe_pipeline("configs/standard_universe.yaml")
print(report.to_markdown())
print(report.to_json_dict()["complexity"])
```

## Adversarial Cosmogenesis (two co-trained paradigms)

The `cosmogenesis` package generates a self-consistent universe with **two
independent paradigms** that optimize separately yet co-train adversarially:

- **Scheme A** — the analytic forward-pass compiler above (transparent closed-form
  layers, hard windows, white-box sensitivity ascent).
- **Scheme B** — a from-scratch *variational self-consistency relaxation*: emergent
  scales come from extremizing balance functionals, windows are soft logistics,
  and a cross-layer **self-consistency residual** plus a fixed-point relaxation can
  flag a universe as internally inconsistent even when every single window passes —
  something A's one-pass model cannot detect. It optimizes with an evolution strategy.

Both consume the **same** `UniverseConfig` / parameter vector (shared entry point)
and return a common `UniverseAssessment`. Each round they optimize, cross-evaluate,
**critique the other's champion**, and **consider** the other's suggested fix (A
adopts B's self-consistency residual as a regularizer; B adopts A's hard-window and
robustness concerns), converging on a consensus universe robust under both views.

```bash
python -m cosmogenesis run-adversarial \
  --base configs/standard_universe.yaml --rounds 6 --out reports/adversarial
```

```python
from cosmogenesis import run_adversarial

result = run_adversarial("configs/standard_universe.yaml", rounds=6, out_dir="reports/adversarial")
print(result.consensus_vector, result.consensus_score_a, result.consensus_score_b)
```

Design rationale: [docs/design/ADVERSARIAL_COSMOGENESIS.md](docs/design/ADVERSARIAL_COSMOGENESIS.md).

## GenesisArena — parallel multi-theory adversarial platform (v2)

`genesis_arena` generalizes the two-scheme arena into a **parallel ecosystem of
independent theory lineages** that challenge each other but are **never merged
into a single winner**. It builds on three genuinely different physics paradigms
(the `cosmogenesis` engines):

| Theory | Family | Engine | Paradigm |
|---|---|---|---|
| `T-0001` | `conservative_eft` | `AnalyticCompiler` | forward closed-form, white-box |
| `T-0002` | `exploratory_generative` | `VariationalRelaxer` | self-consistency fixed point |
| `T-0003` | `minimal_axiom` | `MinimalAxiomDimensional` | Carr–Rees anthropic inequalities, fewest parameters |

Each round theories **attack** each other with schema-validated `ChallengeCard`s,
**defend** per their `DefensePrior`, are judged by a **deterministic Verifier +
Judge**, and are **patched / forked / left unchanged** by a `PatchGate` that
preserves parents and forbids merging. Selection keeps a **Pareto front + family
elites + novelty archive** (no single-score winner-takes-all), and evolution runs
theories and duels **in parallel**.

```bash
python -m genesis_arena theory-list
python -m genesis_arena duel theories/T-0001_conservative_eft/theory.yaml \
                             theories/T-0002_exploratory_generative/theory.yaml --rounds 1
python -m genesis_arena evolve --generations 3 --min-families 3 --no-merge \
                               --out reports/genesis_arena
```

```python
from genesis_arena import TheoryRegistry, evolve

registry = TheoryRegistry.from_dir("theories")
report = evolve(registry.all(), registry, generations=3, min_families=3, out_dir="reports/genesis_arena")
print(report.final_families, report.allow_merge)  # multiple families survive; never merged
```

Design rationale: [plans/2026-06-21-GENESIS_ARENA_V2_PARALLEL_ADVERSARIAL.md](plans/2026-06-21-GENESIS_ARENA_V2_PARALLEL_ADVERSARIAL.md)
(improves on [plans/2026-06-21-ADVERSARIAL_SELF_PLAY_IMPLEMENTATION.md](plans/2026-06-21-ADVERSARIAL_SELF_PLAY_IMPLEMENTATION.md)).

## Configuration Inheritance

Variant universes inherit a complete parent and override only selected values:

```yaml
inherit: standard_universe.yaml
universe:
  name: strong_alpha_universe
dimensionless:
  alpha_scale: 1.2
```

Included variants cover strong electromagnetism, weak and strong gravity, unstable atoms, long-lived stars, and absent primordial perturbations.

## Repository Layout

```text
configs/                 universe inputs and variants
src/quanta_engine/       multi-scale effective universe pipeline
src/quantaengine/        legacy scalar-field lattice prototype
tests/                   unit, integration, CLI, scan, and E2E tests
examples/                runnable Python demos
reports/                 reproducible demonstration outputs
docs/physics_assumptions.md
plans/                   versioned, executable plan packages
```

The original `quantaengine` scalar-field lattice API remains available for compatibility. New effective-universe work should use `quanta_engine` and the `quanta` CLI.

## Scientific Boundaries

Every physical layer exposes assumptions, warnings, and intermediate values. See [docs/physics_assumptions.md](docs/physics_assumptions.md) for calibrated formulas and limitations, [docs/examples.md](docs/examples.md) for the acceptance scenarios, [docs/MVP_COMPLETION.md](docs/MVP_COMPLETION.md) for the stage-by-stage verification matrix, and [plans/quantaengine-mvp-v1/README.md](plans/quantaengine-mvp-v1/README.md) for the reusable execution package.

## Development

```bash
python -m pytest
ruff check src tests examples
mypy src/quanta_engine
```

GitHub Actions runs the test suite and generates a standard-universe Markdown and JSON report on every push and pull request.

## License

MIT License. See [LICENSE](LICENSE).
