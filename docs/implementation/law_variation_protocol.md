# Law Variation Protocol

This protocol defines how QuantaEngine should change fundamental laws and prove that changed laws generate different universes.

The key distinction:

```text
Changing a random seed creates a different history inside the same law.
Changing a LawBook creates a different universe class.
```

Both are useful, but they must never be confused.

## 1. Law identity

Every run must record three hashes:

| Hash | Meaning | Changes when |
|---|---|---|
| `law_hash` | Fundamental/effective laws | constants, fields, interactions, symmetries, potentials, gravity model, chemistry rules change |
| `config_hash` | Runtime configuration | step count, resolution, output cadence, solver tolerance, observers change |
| `run_hash` | Full reproducible run identity | law, config, seed, code version, input files change |

A paper, README claim, or report must specify which level changed.

## 2. Allowed law variation classes

### Class A — Constant scaling

Change numerical constants while keeping law structure fixed.

Examples:

```yaml
mutations:
  - parameter: lawbook.constants.G
    operation: scale
    values: [0.1, 0.3, 1.0, 3.0, 10.0]
  - parameter: lawbook.constants.alpha_em
    operation: scale
    values: [0.2, 0.5, 1.0, 2.0, 5.0]
```

Expected effects:

- gravity strength changes expansion and clustering;
- electromagnetic-like coupling changes atom-like binding and chemistry;
- mass ratios change bound-state stability;
- decay constants change abundance histories.

### Class B — Potential shape variation

Change field potentials while keeping field content fixed.

Examples:

- quadratic potential;
- quartic potential;
- double-well potential;
- cosine potential;
- metastable false vacuum potential.

Expected effects:

- different vacuum states;
- different phase-transition patterns;
- different fluctuation histories;
- defect formation or absence.

### Class C — Symmetry and phase variation

Change symmetry groups or breaking scales.

Examples:

```yaml
symmetries:
  gauge_groups: [U1_like, SU2_like]
  broken_phases:
    - name: weak_like_breaking
      critical_scale: 0.3
```

Expected effects:

- changed species masses;
- changed interaction channels;
- changed stable matter candidates;
- changed early-universe transitions.

### Class D — Interaction graph variation

Enable, disable, or modify interaction vertices.

Examples:

- allow decay A → B + C;
- disable annihilation;
- add long-range force carrier;
- change reaction thresholds.

Expected effects:

- species abundances change;
- stable particles appear/disappear;
- matter bridge changes;
- chemistry graph changes.

### Class E — Gravity/cosmology model variation

Change expansion and clustering law.

Examples:

- Newtonian particle-mesh gravity;
- modified force exponent toy model;
- different equation-of-state components;
- different curvature term;
- dark-energy-like parameter variation.

Expected effects:

- structure growth changes;
- star/galaxy formation changes;
- planet formation and habitability change.

### Class F — Emergent-rule variation

Use this only when lower-level physics is approximated.

Examples:

- different chemistry reaction model;
- different stellar lifetime model;
- different mutation model;
- different agent learning model.

Rules:

- Must be labeled as effective/emergent, not fundamental.
- Must not be mixed with fundamental-law claims.
- Must specify what lower-scale physics was compressed into the rule.

## 3. Law variation experiment design

Every law variation experiment should follow this structure.

### Step 1 — Define baseline LawBook

Required:

- complete LawBook YAML;
- law hash;
- validation report;
- baseline run outputs;
- reason baseline is selected.

### Step 2 — Define mutations

Each mutation must specify:

- parameter path;
- operation;
- values or distribution;
- allowed range;
- expected affected modules;
- validators that should detect invalid cases.

### Step 3 — Define ensemble

Do not compare single histories unless explicitly marked as illustrative.

Recommended:

```yaml
ensemble:
  seeds: [1, 2, 3, 4, 5, 6, 7, 8]
  repeats_per_law: 8
  max_failed_fraction: 0.5
```

### Step 4 — Define metrics

Use metrics at multiple scales.

```yaml
metrics:
  microphysics:
    - stable_species_count
    - mean_lifetime
    - interaction_rate_entropy
  matter:
    - bound_state_count
    - chemistry_complexity
    - autocatalytic_cycles
  cosmology:
    - clustering_strength
    - halo_count
    - halo_mass_entropy
  planets:
    - habitable_planet_count
    - median_habitability_duration
  biology:
    - life_emergence_probability
    - biosphere_diversity_peak
  civilization:
    - intelligence_emergence_probability
    - max_technology_level
    - collapse_frequency
```

### Step 5 — Run scan

Required outputs:

- scan manifest;
- one run directory per law/seed;
- result table;
- failed-run table;
- validation summary;
- comparison report.

### Step 6 — Compare and explain

The comparison report must include:

- which laws changed;
- which lower-scale quantities changed;
- which bridges changed;
- which macro outcomes changed;
- which modules failed;
- confidence intervals over seeds;
- warnings/limitations.

## 4. Causal traceability requirement

A claim is acceptable only if it can be traced.

Bad claim:

```text
Lower alpha created more civilizations.
```

Good claim:

```text
In this toy law family, lowering alpha_em from 1.0 to 0.3 changed the atom-like binding window, increased the number of stable molecule-like reaction-network nodes from 12±3 to 41±6, increased habitable planet chemistry complexity, and raised the civilization-emergence frequency from 0/16 to 5/16 seeds. This is an effective-model result, not a claim about real universes.
```

## 5. Required run artifacts

Each law variation run must save:

```text
runs/<run_id>/
  config.yaml
  lawbook.yaml
  metadata.json
  validation.json
  result_summary.json
  products/
    fields/
    microphysics/
    matter/
    cosmology/
    astro/
    planets/
    biology/
    civilization/
  plots/
  logs/
```

Each scan must save:

```text
scans/<scan_id>/
  scan_config.yaml
  scan_manifest.json
  law_variants.parquet
  run_table.parquet
  metrics.parquet
  failures.parquet
  validation_summary.json
  comparison_report.md
```

## 6. Invalid universe handling

Invalid universes are data.

A scan must not silently drop failed universes. It must classify them:

| Class | Meaning | Example |
|---|---|---|
| `law_invalid` | LawBook fails validation | missing interaction species |
| `microphysics_dead` | no stable species/matter bridge | all particles decay |
| `matter_dead` | no stable composites/chemistry | weak binding |
| `cosmic_dead` | no structure | expansion too fast |
| `astro_dead` | no stars/enrichment | no cooling |
| `planet_dead` | no stable environments | no planets |
| `bio_dead` | no life | no autocatalysis |
| `civ_dead` | no civilization | unstable biosphere/resources |
| `numerical_fail` | solver unstable | NaN, divergence |

These are valuable outcomes because they define the boundary of possible universes.

## 7. Law variation acceptance tests

Minimum acceptance for this protocol:

1. Baseline and variant LawBooks have different `law_hash`.
2. Same LawBook with different seed has same `law_hash` but different `run_hash`.
3. A one-parameter scan produces a table of law variants and outcomes.
4. Failed universes are recorded with reasons.
5. At least one metric changes monotonically or statistically with a controlled law change in a toy benchmark.
6. Comparison report links law changes to scale-specific metric changes.
7. Re-running the scan reproduces result hashes within documented tolerances.

## 8. First recommended law-space demo

Use a minimal but meaningful three-axis scan:

```yaml
scan_name: first_law_space_demo
baseline: examples/full_stack/baseline_toy_universe.yaml
parameters:
  G_scale: [0.3, 1.0, 3.0]
  alpha_em_scale: [0.3, 1.0, 3.0]
  primordial_rms_scale: [0.5, 1.0, 2.0]
seeds: [1, 2, 3, 4]
metrics:
  - stable_species_count
  - chemistry_complexity
  - clustering_strength
  - halo_count
  - star_count
  - habitable_planet_count
  - life_emergence
  - max_technology_level
```

Expected pedagogical result:

- `G_scale` mostly affects clustering, stars, planets.
- `alpha_em_scale` mostly affects matter/chemistry/life.
- `primordial_rms_scale` mostly affects structure timing.
- Coupled effects appear downstream.

This demo should become the first public “changed laws create changed universes” showcase.
