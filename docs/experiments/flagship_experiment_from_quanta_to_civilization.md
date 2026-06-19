# Flagship Experiment: From Quanta to Civilization

This document defines the long-term showcase experiment for QuantaEngine.

The purpose is not to claim that a toy code can predict real universes. The purpose is to demonstrate the engine architecture: start from law-level choices, generate lower-scale physics, propagate consequences upward, and compare generated universe histories.

## 1. Experiment title

```text
From Quanta to Civilization: Law-Dependent Universe Generation
```

## 2. Central hypothesis

In QuantaEngine, a universe is defined by a LawBook. Changing the LawBook should change microscopic physics, and those changes should propagate through matter, structure formation, environments, life, intelligence, and civilization modules.

## 3. Experiment families

The flagship experiment should compare at least five universe families.

### Family A — Baseline Toy Universe

Purpose:

- reference universe;
- stable microphysics;
- nontrivial chemistry;
- structure formation;
- some long-lived stars;
- possible planets;
- possible life/civilization in some seeds.

Expected outcome:

- not guaranteed life;
- enough complexity for downstream modules to operate.

### Family B — Weak Binding Universe

Law change:

- reduce electromagnetic-like or binding coupling.

Expected causal chain:

```text
weaker coupling
  → fewer stable bound states
  → smaller chemistry network
  → fewer autocatalytic cycles
  → lower life emergence probability
  → fewer/no civilizations
```

Evidence required:

- bound-state count decreases;
- chemistry graph loses nodes/edges;
- life module reports failure or lower probability.

### Family C — Strong Binding / Over-Collapsed Matter Universe

Law change:

- increase binding or strong-like coupling.

Expected causal chain:

```text
stronger coupling
  → overly stable/simple composites or rapid collapse
  → reduced chemical flexibility
  → altered cooling and star formation
  → constrained biospheres
```

Evidence required:

- composite catalog changes;
- chemistry diversity may decrease despite stronger binding;
- star/planet/life outcomes differ from baseline.

### Family D — Low Gravity Universe

Law change:

- reduce gravity strength.

Expected causal chain:

```text
weaker gravity
  → slower structure growth
  → fewer halos/stars by fixed cosmic time
  → fewer enriched planetary systems
  → delayed or suppressed life/civilization
```

Evidence required:

- clustering metric decreases;
- halo count/star count decreases or shifts later;
- habitability windows change.

### Family E — High Gravity Universe

Law change:

- increase gravity strength.

Expected causal chain:

```text
stronger gravity
  → faster clustering/collapse
  → altered star lifetimes and feedback
  → more violent environments
  → different planet survival and biosphere stability
```

Evidence required:

- clustering metric increases;
- collapse/feedback events increase;
- planet/biosphere stability changes.

### Family F — High Chaos / Different Primordial Fluctuation Universe

Law change:

- increase primordial RMS or chaos strength;
- change spectral index.

Expected causal chain:

```text
larger initial fluctuations
  → earlier nonlinear structure
  → different halo/galaxy morphology
  → different star formation history
  → altered planetary and biological opportunity windows
```

Evidence required:

- initial power spectrum differs;
- halo mass function differs;
- downstream opportunity windows differ.

## 4. Required run matrix

Minimum initial demonstration:

```text
6 law families × 8 random seeds = 48 universe histories
```

Preferred later demonstration:

```text
6 law families × 32 random seeds × 3 resolutions = 576 runs
```

Each run should use the same output schema so all families can be compared.

## 5. Full-stack pipeline

```text
1. LawBook validation
2. Quantum/field initialization
3. Microphysics event/statistical evolution
4. Matter/chemistry bridge creation
5. Cosmology/structure formation
6. Star/galaxy formation and enrichment
7. Planetary environment generation
8. Prebiotic chemistry and life emergence
9. Intelligence candidate evolution
10. Civilization simulation
11. Observability/report generation
```

Each stage can terminate the run with a classified failure.

## 6. Data products

### Law products

- `lawbook.yaml`
- `law_summary.json`
- `law_hash.txt`
- `law_validation.json`

### Quantum/micro products

- `initial_fields.npz`
- `power_spectrum.parquet`
- `event_records.parquet`
- `species_abundance.parquet`
- `microphysics_bridge.json`

### Matter products

- `bound_states.parquet`
- `reaction_network.parquet`
- `chemistry_metrics.json`
- `matter_bridge.json`

### Cosmology products

- `density_snapshots.zarr` or `.npz`
- `power_spectrum_history.parquet`
- `halo_catalog.parquet`
- `structure_metrics.json`

### Astrophysics products

- `star_catalog.parquet`
- `galaxy_catalog.parquet`
- `enrichment_history.parquet`
- `astro_bridge.json`

### Planet products

- `planet_catalog.parquet`
- `environment_history.parquet`
- `habitability_metrics.json`
- `planetary_bridge.json`

### Biology products

- `prebiotic_cycles.parquet`
- `replicator_history.parquet`
- `biosphere_history.parquet`
- `biosphere_metrics.json`
- `biosphere_bridge.json`

### Civilization products

- `agent_history.parquet`
- `technology_timeline.parquet`
- `civilization_events.parquet`
- `civilization_metrics.json`

### Reports

- `universe_report.md`
- `law_comparison_report.md`
- `validation_summary.json`
- plots and figures generated from saved numeric data.

## 7. Primary comparison metrics

### Microphysics

- stable species count;
- mean lifetime;
- interaction entropy;
- abundance diversity;
- conservation residual.

### Matter/chemistry

- stable bound-state count;
- reaction graph node/edge count;
- chemistry complexity index;
- autocatalytic cycle count;
- energy-storage pathway count.

### Cosmology

- density contrast RMS;
- clustering strength;
- halo count;
- halo mass distribution;
- cosmic web morphology.

### Astrophysics

- star count;
- star formation history;
- long-lived star fraction;
- enrichment fraction;
- feedback event rate.

### Planetary

- planet count;
- stable orbit count;
- habitable duration;
- chemical inventory score;
- catastrophe rate.

### Biology

- life emergence probability;
- time to first replicator;
- biosphere persistence duration;
- diversity peak;
- extinction count;
- complexity growth.

### Intelligence/civilization

- intelligence emergence probability;
- time to tool-use analogue;
- max technology level;
- energy use;
- cooperation/conflict ratio;
- collapse frequency;
- expansion events.

## 8. Acceptance criteria

The flagship experiment is accepted when:

1. all six law families have distinct `law_hash` values;
2. every run records config, seed, code version, and validation status;
3. failed runs are included in statistics;
4. at least three layers show law-dependent metric differences;
5. at least one family fails before life/civilization for a documented physical reason;
6. at least one family reaches life or civilization in a subset of seeds;
7. reports show causal chains, not just final outcomes;
8. rerunning the demonstration reproduces the scan table within tolerance.

## 9. First public demo target

The first public version should not attempt the full civilization stack. It should show a credible subset:

```text
LawBook → quantum fluctuations → field/microphysics toy → matter/chemistry toy → structure formation toy
```

Then the report can say:

```text
This demo proves the modular law-to-structure pipeline. Life and civilization modules are planned and documented but not yet validated.
```

## 10. Full public demo target

A later milestone can add the full stack:

```text
LawBook → microphysics → matter → cosmic structure → stars → planets → life → agents → civilization
```

The report should generate a narrative like:

```text
Universe B did not produce life because weak binding suppressed stable molecule-like networks.
Universe D produced fewer civilizations because weak gravity delayed star formation and reduced long-duration habitable planets.
Universe E produced abundant structure but high environmental catastrophe rates, leading to frequent biosphere collapse.
```

Each sentence must link to a numeric metric and validation status.

## 11. Scientific caution statement

Every flagship report must include:

```text
QuantaEngine's early full-stack universes are toy effective simulations. They are designed to explore causal architecture and law-dependent emergence, not to claim precision prediction of real cosmology, chemistry, biology, or civilization. Each module reports its validation level and assumptions.
```

This caution protects credibility while preserving ambition.
