# Evidence and Acceptance Standards

QuantaEngine must be judged by evidence, not by attractive images or ambitious language.

This document defines what counts as evidence for each kind of feature.

## 1. Evidence hierarchy

| Evidence level | Meaning | Example |
|---|---|---|
| E0 — Concept | Idea only | roadmap text, no code |
| E1 — Executable toy | Code runs, assumptions explicit | scalar field toy model with tests |
| E2 — Internally validated toy | Conservation/statistical/regression checks | decay distribution matches exponential law |
| E3 — Benchmark-aligned model | Reproduces known analytic/numerical benchmark | growth equation limiting case |
| E4 — Literature/production comparable | Compared with trusted external code or published result | future comparison to CLASS/CAMB/Gadget-like outputs |
| E5 — Scientific claim ready | documented uncertainty, validation, limitations, reproducibility | release-quality benchmark report |

Most early QuantaEngine modules will be E1–E2. That is acceptable if labeled clearly.

## 2. Required evidence for every module

Every module must provide:

1. **Assumptions**
   - What equations/rules are used?
   - What is deliberately simplified?
   - What real physics is not included?

2. **Configuration example**
   - Minimal YAML that enables the module.
   - At least one parameter users can change.

3. **Unit tests**
   - Constructor/config validation.
   - Deterministic output for a fixed seed.
   - Failure on invalid input.

4. **Validation check**
   - Conservation, distribution, convergence, monotonic trend, or benchmark.

5. **Saved output**
   - Numeric data product.
   - Metadata with config/law/run hash.
   - Optional plot generated from numeric data.

6. **Documentation**
   - User-facing explanation.
   - Developer-facing API note.
   - Limitations.

## 3. Acceptance template

Use this template in pull requests.

```markdown
## Module name

## Evidence level
- [ ] E1 executable toy
- [ ] E2 internally validated toy
- [ ] E3 benchmark-aligned model
- [ ] E4 external comparison
- [ ] E5 scientific claim ready

## Assumptions

## Config example

## Tests added

## Validation checks

## Output artifacts

## Known limitations

## Reproducibility proof
- command:
- seed:
- output hash:
```

## 4. Validation categories

### 4.1 Determinism

Required for all modules.

Evidence:

- two runs with same seed/config/code produce same output checksum;
- named random streams are recorded;
- parallel execution does not change results unless documented.

### 4.2 Conservation

Required when a module has conserved quantities.

Examples:

- charge conservation in particle interactions;
- mass conservation in particle-mesh gravity;
- energy-like quantity behavior in undamped field evolution;
- population/resource accounting in ecology/civilization modules.

### 4.3 Statistical distribution

Required for stochastic modules.

Examples:

- decay times follow exponential distribution;
- event counts follow Poisson expectation;
- mutation counts match configured rates;
- sampling distributions are reproducible.

### 4.4 Convergence

Required for numerical solvers.

Examples:

- decreasing time step reduces error;
- increasing grid resolution stabilizes metric;
- solver remains finite over declared range.

### 4.5 Law sensitivity

Required for the project’s core claim.

Examples:

- changing `G` changes clustering metrics;
- changing coupling changes bound-state catalog;
- changing stellar lifetime changes habitability windows;
- changing mutation rate changes biological diversity.

### 4.6 Cross-scale consistency

Required for higher-level modules.

Examples:

- life module cannot run without chemistry bridge;
- civilization module cannot run without biosphere bridge;
- star module cannot produce heavy species forbidden by matter bridge;
- planet module cannot create rocky worlds without enrichment.

## 5. Failure evidence

Failure must be recorded.

A failed universe should produce:

```json
{
  "status": "failed",
  "failure_class": "matter_dead",
  "failure_reason": "No stable bound states found under selected coupling constants.",
  "law_hash": "...",
  "config_hash": "...",
  "seed": 42,
  "last_valid_scale": "microphysics",
  "validators": [...]
}
```

Do not hide failed runs from scan summaries.

## 6. Scale-specific acceptance standards

### LawBook

Accept when:

- schema validates;
- constants have units or are explicitly dimensionless;
- interactions reference valid fields/species;
- law hash is stable;
- invalid LawBook fails before simulation.

### Quantum/field layer

Accept when:

- initial spectrum matches requested slope/amplitude in tolerance;
- field evolution remains finite;
- energy components recorded;
- resolution/time-step sensitivity documented.

### Microphysics

Accept when:

- conservation rules are enforced;
- event distributions pass statistical tests;
- stable species table is reproducible;
- invalid interactions fail.

### Matter/chemistry

Accept when:

- bound-state logic is connected to LawBook parameters;
- chemistry graph changes under coupling changes;
- no-matter universes fail gracefully;
- reaction network metrics are saved.

### Cosmology/structure

Accept when:

- mass conservation passes;
- power spectrum is saved;
- clustering changes under gravity/initial spectrum changes;
- halo catalog is reproducible.

### Astrophysics

Accept when:

- star formation depends on cooling and density;
- enrichment depends on star history and matter rules;
- no-heavy-element universes do not produce rich planets;
- catalogs are linked to parent halos/galaxies.

### Planetary systems

Accept when:

- planets link to parent stars;
- habitability depends on environment history;
- orbit/environment checks exist;
- no-enrichment universes produce failure/low habitability.

### Life

Accept when:

- life requires autocatalytic chemistry or configured equivalent;
- mutation/selection are stochastic but reproducible;
- ensemble probabilities are reported;
- life can fail.

### Intelligence/civilization

Accept when:

- intelligence depends on biosphere and environment;
- technology depends on resources, energy, and knowledge;
- collapse and stagnation are possible;
- outcomes are reported statistically, not as deterministic destiny.

## 7. Release gates

### v0.2 release gate

- Geant4-style kernel exists.
- LawBook DSL exists.
- Module registry works.
- Three process modules run through common interface.

### v0.3 release gate

- Microphysics and field modules produce validated toy outputs.
- Law variations change microphysical outcomes.

### v0.4 release gate

- Cosmology/structure modules produce density, power, and halo outputs.
- Law variations change structure metrics.

### v0.5 release gate

- Matter/chemistry layer exists.
- Law variations change chemistry complexity.

### v0.6 release gate

- Stars/galaxies/planets produce catalogs.
- Habitability metrics depend on lower-scale outputs.

### v0.7 release gate

- Life module exists and can fail.
- Ensemble life-emergence probability can be measured.

### v0.8 release gate

- Agent/civilization module exists and consumes biosphere bridge.
- Civilization outcomes are reproducible and statistically reported.

### v1.0 release gate

- Stable public APIs.
- Validation suite.
- Full-stack toy universe demo.
- Law-space scan demo.
- Documentation states exactly what is toy, validated, and experimental.

## 8. Minimum proof for the flagship claim

The flagship claim is:

```text
Changing basic physical laws generates different microscopic and macroscopic universes.
```

Minimum proof requires:

1. two or more LawBooks with different `law_hash`;
2. same seed ensemble for each LawBook;
3. differences at microphysics or field layer;
4. propagated differences at matter or cosmology layer;
5. propagated differences at at least one higher layer: stars, planets, life, or civilization;
6. validators pass or classify failures;
7. comparison report explains the causal chain;
8. all artifacts are reproducible.

## 9. Red flags

A result must be treated as invalid or misleading if:

- it has no saved config;
- it has no seed;
- it cannot be reproduced;
- it uses hidden constants;
- it has pretty plots but no numeric data;
- validators were disabled without explanation;
- failed universes were excluded from statistics;
- higher-level modules ignored lower-scale constraints;
- it claims real-world physics accuracy from toy models.
