# Master Execution Checklist

This is the main engineering execution plan for QuantaEngine. It is written to be converted directly into GitHub milestones and issues.

Each phase contains:

- **Goal**: what the phase must accomplish.
- **Why it matters**: why this phase is necessary for the long-term “创世” goal.
- **Implementation plan**: concrete coding steps.
- **Self-check for missing facts**: what may be wrong, incomplete, hidden, or unjustified.
- **Deliverables**: files, APIs, examples, docs, tests.
- **Evidence and acceptance**: proof that the phase is done.
- **Do not proceed until**: hard gate.

The final target is a Geant4-style modular universe engine where a user can define basic physical laws, evolve microscopic physics into macroscopic structure, generate matter and interactions, produce galaxies and planets, allow life and intelligence modules to emerge under compatible conditions, and compare how changed physical laws create different universes.

---

## M0 — Repository hardening

### Goal

Turn the current seed repository into a maintainable open-source scientific package with clear conventions, CI, formatting, typed APIs, and reproducible examples.

### Why it matters

The project is ambitious. Without strong repository discipline, physics modules will become inconsistent, undocumented, and impossible to validate.

### Implementation plan

1. **Normalize package layout**
   - Keep source under `src/quantaengine/`.
   - Move the current simple modules into future-compatible namespaces only when tests are ready.
   - Add `quantaengine/kernel`, `quantaengine/law`, `quantaengine/processes`, `quantaengine/state_spaces`, `quantaengine/validation`, and `quantaengine/backends` gradually.

2. **Add developer tooling**
   - Add `ruff` for linting and formatting.
   - Add `mypy` or `pyright` for type checking.
   - Add `pytest-cov` for coverage.
   - Add pre-commit hooks.
   - Add GitHub Actions jobs for lint, type check, tests, and minimal example run.

3. **Define contribution rules**
   - Every physics feature must include an assumptions section.
   - Every module must include at least one small config example.
   - Every stochastic module must be deterministic under seed.
   - Every visual output must be tied to saved numeric data.

4. **Add issue templates**
   - Physics module proposal.
   - Numerical solver proposal.
   - Validation benchmark proposal.
   - Documentation task.
   - Bug report with reproducibility fields.

5. **Add release policy**
   - `v0.x` means research prototype.
   - `v1.0` requires validated kernel interfaces and benchmark suite.
   - No claim of physical accuracy unless tied to documented validation.

6. **Add project metadata**
   - `CITATION.cff` already exists; keep it updated.
   - Add `docs/references.md` for scientific references.
   - Add `docs/terminology.md` for terms such as LawBook, Process, ScaleBridge.

### Self-check for missing facts

- Are package names stable enough before public release?
- Are dependencies minimal and installable on Linux/macOS/Windows?
- Do tests run without optional GPU or plotting dependencies?
- Is the README honest that current physics is a toy scaffold?
- Is the license compatible with future integration of external physics libraries?

### Deliverables

- `.github/workflows/tests.yml` expanded.
- `.pre-commit-config.yaml`.
- `docs/terminology.md`.
- issue templates under `.github/ISSUE_TEMPLATE/`.
- `Makefile` targets: `make test`, `make lint`, `make typecheck`, `make demo`, `make validate-demo`.

### Evidence and acceptance

- Fresh clone installs with `pip install -e .[dev]`.
- `pytest` passes.
- `ruff check .` passes.
- `quantaengine run --config examples/minimal_universe.yaml --out runs/ci_demo --steps 16` succeeds.
- GitHub Actions passes on pull request.
- README links to the detailed implementation docs.

### Do not proceed until

A new contributor can clone the repo, run tests, run a demo universe, and understand the development roadmap within 15 minutes.

---

## M1 — Geant4-style kernel

### Goal

Create the modular kernel that lets QuantaEngine load, configure, schedule, run, observe, validate, and checkpoint independent modules.

### Why it matters

This is the architectural foundation. Without a kernel, all future physics will become ad hoc scripts. With a kernel, users can define universes by composing modules, like a Geant4 user composes detector geometry, physics lists, sources, and output actions.

### Implementation plan

1. **Create `quantaengine/kernel/`**
   - `run_manager.py`
   - `module_registry.py`
   - `state.py`
   - `process.py`
   - `observer.py`
   - `validator.py`
   - `scheduler.py`
   - `random_service.py`
   - `checkpoint.py`
   - `context.py`

2. **Implement `UniverseRunManager`**
   - Loads full YAML config.
   - Builds `LawBook`.
   - Builds initial `State`.
   - Registers processes.
   - Initializes observers and validators.
   - Runs scheduler loop.
   - Writes metadata and checkpoints.

3. **Implement `ModuleRegistry`**
   - Built-in modules loaded by string path.
   - External modules loadable through Python entry points later.
   - Registry can list modules through CLI.
   - Registry validates module type and version.

4. **Implement base classes**
   - `Process`: configure, validate_inputs, propose_step, apply, observables.
   - `Observer`: configure, record, finalize.
   - `Validator`: check, finalize.
   - `Scheduler`: next_context, active_processes, done.

5. **Implement deterministic random service**
   - Global seed.
   - Named random streams.
   - Stable seed derivation from run seed + stream name.
   - Metadata recording.

6. **Migrate current toy modules into process style**
   - Friedmann expansion becomes `ExpansionProcess`.
   - Scalar field update becomes `ScalarFieldProcess`.
   - Chaos injection becomes `ChaosProcess`.
   - Spectrum initial condition becomes `PrimordialSpectrumInitialCondition`.

7. **Add CLI commands**
   - `quantaengine inspect modules`.
   - `quantaengine run` using new kernel.
   - Keep backward compatibility for current simple demo until migration is complete.

### Self-check for missing facts

- Does the process interface support both deterministic PDE steps and stochastic event processes?
- Does the scheduler allow different time coordinates: physical time, conformal time, scale factor, event count?
- Can a process declare its validity range?
- Can a process fail gracefully if required law parameters are missing?
- Can a module be added without editing `engine.py`?
- Is process ordering explicit and reproducible?

### Deliverables

- Kernel package.
- Base classes with docstrings.
- YAML config schema for module list.
- Three migrated process modules.
- Example: `examples/kernel_demo.yaml`.
- CLI module inspection.
- Tests for registry, scheduler, random streams, checkpoint metadata, process determinism.

### Evidence and acceptance

- A toy external process can be loaded through config.
- Two runs with the same seed produce identical checksums.
- Changing one process parameter changes the law/config hash and result metadata.
- Removing a process changes output in a predictable way.
- Test coverage includes process order and random stream reproducibility.

### Do not proceed until

The engine can run at least three independent processes through the same interface and produce reproducible outputs without direct calls to old monolithic code.

---

## M2 — Units, dimensions, constants, and LawBook DSL

### Goal

Make physical laws explicit, configurable, hashable, validated, and separable from numerical implementation.

### Why it matters

The core idea is that changing fundamental physical laws creates different universes. This is impossible if constants are scattered through code. A LawBook is the genome of a generated universe.

### Implementation plan

1. **Create `quantaengine/law/`**
   - `lawbook.py`
   - `constants.py`
   - `units.py`
   - `dimensions.py`
   - `fields.py`
   - `species.py`
   - `interactions.py`
   - `symmetries.py`
   - `potentials.py`
   - `schema.py`

2. **Define unit system**
   - Default: dimensionless natural units for toy universes.
   - Explicit metadata: `unit_system: natural`, `c=1`, `hbar=1`, etc.
   - Support future SI/CGS conversion via optional library.
   - Every dimensional parameter declares dimensions.

3. **Define constants table**
   - Fundamental constants: `c`, `hbar`, `G`, `k_B`.
   - Couplings: electromagnetic-like, strong-like, weak-like.
   - Mass scales.
   - Cosmological parameters.
   - User-defined constants.

4. **Define fields and species**
   - Fields: scalar, vector, spinor placeholder, tensor placeholder.
   - Species: mass, charge vector, spin, lifetime, statistics, stability.
   - Interactions reference fields/species by ID.

5. **Define potential/action DSL**
   - Start with named potentials: quadratic, quartic, double-well, cosine, custom polynomial.
   - Later support symbolic expressions safely.
   - Store derivative rules or auto-differentiate where available.

6. **Define symmetry and phase rules**
   - Gauge/global symmetry labels.
   - Broken/unbroken phase definitions.
   - Critical temperature or scale triggers.
   - Order parameter definitions.

7. **Define law hash**
   - Canonicalize YAML.
   - Hash only law-defining values.
   - Separate `law_hash`, `run_hash`, and `code_version`.

8. **Add LawBook validators**
   - Missing constants.
   - Negative masses where not allowed.
   - Invalid interaction references.
   - Unit mismatch.
   - Coupling outside declared validity range.
   - Duplicate IDs.

9. **Add examples**
   - `examples/lawbooks/standard_toy_lawbook.yaml`.
   - `examples/lawbooks/low_gravity_lawbook.yaml`.
   - `examples/lawbooks/strong_coupling_universe.yaml`.
   - `examples/lawbooks/no_stable_atoms_universe.yaml`.

### Self-check for missing facts

- Is a changed constant enough to produce a changed `law_hash`?
- Are hidden constants still inside solver code?
- Can a LawBook define a universe with no stable matter and have higher layers detect that life is impossible?
- Are dimensionless toy constants clearly labeled as toy constants?
- Are user-defined laws validated before running expensive simulations?

### Deliverables

- LawBook classes.
- LawBook schema.
- LawBook YAML examples.
- LawBook CLI inspection.
- Unit/dimension validator.
- Tests for hashing, validation, config round-trip, and hidden default detection.

### Evidence and acceptance

- `quantaengine inspect law --config examples/lawbooks/standard_toy_lawbook.yaml` prints constants, fields, species, interactions, and hash.
- Changing `alpha_em` changes `law_hash`.
- A broken LawBook with missing species reference fails before simulation.
- Current physics modules read constants only from LawBook or process config.

### Do not proceed until

No core physics module uses hidden global constants for law-defining behavior.

---

## M3 — State spaces and numerical backends

### Goal

Generalize from the current scalar grid into multiple state representations and numerical backends.

### Why it matters

A universe crosses representations: fields on grids, particles in phase space, networks of reactions, graph-based societies, and hybrid models. A Geant4-style engine needs common state contracts without forcing everything into one array.

### Implementation plan

1. **Create state-space abstractions**
   - `UniformLatticeStateSpace`.
   - `ParticleCloudStateSpace`.
   - `ReactionNetworkStateSpace`.
   - `GraphStateSpace`.
   - `HybridStateSpace`.

2. **Define state containers**
   - `FieldState`: arrays and scale factor.
   - `ParticleState`: positions, velocities, species, weights.
   - `NetworkState`: nodes, edges, reaction rates.
   - `AgentState`: agents, traits, resources, networks.
   - `HybridUniverseState`: combines components and shared metadata.

3. **Add backend abstraction**
   - NumPy first.
   - Optional JAX/CuPy/Torch later.
   - FFT interface.
   - Random stream interface.
   - `to_numpy()` for output.

4. **Add serialization**
   - Small arrays: `.npz`.
   - Larger future arrays: HDF5/Zarr.
   - Catalogs: Parquet.
   - Metadata: JSON.

5. **Add checkpoint and restart**
   - Save state at cadence.
   - Restart from checkpoint.
   - Validate that restart reproduces uninterrupted run.

6. **Add stability utilities**
   - CFL-like time step checks for PDE modules.
   - positivity checks for densities.
   - finite-value checks.
   - boundary condition checks.

### Self-check for missing facts

- Can mixed states be serialized without losing component type?
- Does state checksum ignore non-deterministic metadata such as timestamps?
- Can the same process run on NumPy and JAX later without API changes?
- Does checkpoint restart preserve random streams?
- Are units and topology stored with state?

### Deliverables

- `state_spaces` package.
- backend interface and NumPy backend.
- checkpoint/restart API.
- example using `HybridUniverseState`.
- tests for serialization and restart equivalence.

### Evidence and acceptance

- A 64-step run checkpointed at step 32 and restarted to step 64 matches an uninterrupted 64-step run within tolerance.
- State metadata records topology, backend, law hash, run hash, step, time, and seed streams.
- At least one observer can read state without knowing concrete class internals.

### Do not proceed until

The current toy scalar simulation can run through the new state-space and backend abstractions without behavior regression.

---

## M4 — Microphysics plugin layer

### Goal

Introduce a high-energy-physics flavored module layer for particles, fields, interactions, scattering, decay, symmetry breaking, and event generation.

### Why it matters

The project’s premise is that macroscopic universes emerge from microscopic physical laws. This phase creates the foundation for that causal chain.

### Implementation plan

1. **Define particle/species model**
   - ID, name, mass, charge vector, spin placeholder, statistics, lifetime, stable flag.
   - Support toy particles first; do not claim Standard Model fidelity.

2. **Define interaction model**
   - Interaction vertices.
   - Allowed incoming/outgoing species.
   - Coupling constants.
   - Kinematic thresholds.
   - Rate/cross-section function handle.

3. **Create event record**
   - Event ID.
   - Parent particles.
   - Daughter particles.
   - Interaction type.
   - Energy/momentum bookkeeping in toy units.
   - Random stream metadata.

4. **Implement toy process plugins**
   - `DecayProcess` with exponential lifetime.
   - `TwoBodyScatteringProcess` with configurable cross section.
   - `PairCreationProcess` under threshold conditions.
   - `AnnihilationProcess` for matter/antimatter toy species.
   - `ThermalCollisionProcess` for early-universe plasma toy model.

5. **Add conservation validators**
   - energy-like scalar conservation where applicable;
   - charge conservation;
   - species count changes as expected;
   - event rate sanity check.

6. **Add microphysics bridge**
   - Given LawBook and event processes, output stable species, interaction table, decay table, effective thermodynamic quantities.

7. **Add examples**
   - stable matter universe;
   - fast-decay universe;
   - no-bound-state universe;
   - high-annihilation universe.

### Self-check for missing facts

- Are we modeling real Standard Model physics or a toy effective analogue? The docs must say which.
- Does every interaction respect declared conservation rules?
- Are cross sections dimensionally consistent in the chosen units?
- Do random event rates reproduce expected exponential/Poisson distributions?
- Can invalid LawBooks create physically impossible processes? They must fail early.

### Deliverables

- `processes/microphysics/` package.
- particle/species definitions in LawBook.
- event record format.
- microphysics bridge.
- examples and tests.

### Evidence and acceptance

- Decay process reproduces exponential lifetime distribution in statistical test.
- Charge conservation validator catches a deliberately invalid decay.
- Same seed produces same event history.
- Changing a coupling changes event rates and final species abundances.
- Microphysics bridge reports whether stable matter-like species exist.

### Do not proceed until

A changed microphysical law can be shown to change particle abundances or stability in a reproducible demo.

---

## M5 — Quantum, field, vacuum, and phase-transition layer

### Goal

Expand beyond toy fluctuations into modular quantum-field-inspired components: vacuum states, field potentials, symmetry breaking, stochastic fluctuations, tunneling/bubble nucleation analogues, and phase transitions.

### Why it matters

The project’s story begins in microscopic quantum fluctuations and chaos. This phase gives that beginning structure and testable outputs.

### Implementation plan

1. **Refactor current scalar field code**
   - Move to `processes/fields/scalar_lattice.py`.
   - Field potential comes from LawBook.
   - Gradient terms use state-space spacing.
   - Add boundary-condition metadata.

2. **Add potential models**
   - quadratic;
   - quartic;
   - double well;
   - cosine/axion-like toy;
   - user-defined polynomial.

3. **Add vacuum initializers**
   - Gaussian vacuum fluctuations;
   - thermal fluctuations;
   - squeezed/colored spectrum toy;
   - seeded defects.

4. **Add phase-transition module**
   - temperature/scale-factor dependent potential parameters;
   - order parameter evolution;
   - bubble seed stochastic events;
   - domain wall/defect toy tracking.

5. **Add chaos module upgrades**
   - Lyapunov-like divergence diagnostics.
   - controlled perturbation families.
   - compare two universes with tiny initial difference.

6. **Add field observables**
   - power spectrum;
   - two-point correlation;
   - defect count;
   - energy components;
   - order parameter distribution.

7. **Add validators**
   - finite field values;
   - energy monotonicity where damping applies;
   - stability under time-step refinement;
   - symmetry restoration/breaking sanity checks.

### Self-check for missing facts

- Are phase transitions physical models or toy analogues?
- Does the potential derivative match the potential?
- Are stochastic bubble rates documented?
- Does the system produce artifacts from grid resolution?
- Can two nearly identical seeds diverge in a measurable way under chaos settings?

### Deliverables

- field process package;
- potential DSL;
- phase-transition example;
- chaos divergence notebook/script;
- observables and tests.

### Evidence and acceptance

- A double-well potential produces domain separation in a small demo.
- Power spectrum output changes with spectral index.
- Time-step refinement test shows convergence trend.
- Tiny perturbation comparison produces documented divergence when chaos is enabled.

### Do not proceed until

The engine can create at least two visibly and numerically different early-universe field histories from different LawBooks or initial quantum/chaos settings.

---

## M6 — Cosmology and structure formation layer

### Goal

Move from early fields to expanding universes with density perturbations, gravity, structure growth, and synthetic cosmic observables.

### Why it matters

A generated universe must develop macroscopic structure, not only local fields. This is the bridge from microscopic laws to cosmic architecture.

### Implementation plan

1. **Improve background cosmology**
   - Expand current Friedmann-like model.
   - Support configurable components: radiation, matter, dark-energy-like term, curvature.
   - Add equation-of-state parameters.
   - Add scale-factor stepping.

2. **Add perturbation growth toy model**
   - Linear growth equation.
   - Transfer-function placeholder.
   - Growth factor output.
   - Compare matter/radiation/dark-energy scenarios.

3. **Add particle-mesh gravity**
   - Deposit particles on mesh.
   - Solve Poisson-like equation by FFT.
   - Update particle velocities/positions.
   - Periodic box first.

4. **Add halo finder prototype**
   - Friends-of-friends or simple density threshold.
   - Halo mass, position, radius.
   - Catalog output to Parquet/CSV.

5. **Add synthetic observables**
   - density maps;
   - matter power spectrum;
   - halo mass function;
   - correlation function;
   - cosmic web morphology metrics.

6. **Add validators**
   - mass conservation;
   - Poisson residual;
   - momentum drift;
   - growth factor sanity checks;
   - reproducibility under checkpoint restart.

7. **Add examples**
   - high-gravity universe → faster clustering;
   - low-gravity universe → weaker structure;
   - high-radiation universe → delayed matter clustering;
   - altered primordial spectrum → different cosmic web.

### Self-check for missing facts

- Are we claiming compatibility with precision cosmology? If not, label as toy/educational.
- Is the chosen time step stable for the particle-mesh solver?
- Does structure formation depend on box size and resolution?
- Are halo catalogs reproducible?
- Does changing `G` affect both expansion and clustering consistently?

### Deliverables

- particle-mesh gravity process;
- perturbation growth module;
- halo finder;
- cosmology observers;
- example law scans.

### Evidence and acceptance

- Mass is conserved within tolerance.
- Higher gravity produces statistically larger clustering metric in controlled scan.
- Different spectral indices produce different power-spectrum slopes.
- Halo catalog is generated and documented.
- Plots are backed by saved numeric arrays and metadata.

### Do not proceed until

The engine can show law-dependent macroscopic structure formation from controlled initial perturbations.

---

## M7 — Matter, nuclear, atomic, and chemistry emergence layer

### Goal

Create an effective matter-generation layer that consumes microphysics outputs and determines whether stable composite structures, atom-like species, molecule-like networks, and chemistry-like reactions exist.

### Why it matters

Life and civilization cannot be meaningful if the universe cannot produce stable matter, rich chemistry, and energy gradients. This phase connects fundamental parameters to material complexity.

### Implementation plan

1. **Define `MatterBridge`**
   - stable fundamental species;
   - allowed bound states;
   - approximate binding energies;
   - charge neutrality rules;
   - stable composite catalog;
   - reaction channels;
   - radiative/cooling properties.

2. **Implement toy bound-state solver**
   - Start with simple potential wells and threshold rules.
   - Determine whether two or more species can form stable bound states.
   - Output binding energy and lifetime.
   - Clearly label as toy effective binding model.

3. **Implement nuclear-like network**
   - Fusion/fission-like reactions under configurable rules.
   - Reaction rates depend on temperature, density, barrier parameters.
   - Generate abundance histories.

4. **Implement atom-like layer**
   - Central charged species + orbiting light species toy model.
   - Stability windows depend on mass ratio, coupling strength, and radiation rules.
   - Output atom-like species catalog.

5. **Implement molecule-like chemistry graph**
   - Nodes: species/composites.
   - Edges: reactions.
   - Metrics: network size, diversity, autocatalytic cycles, energy storage.

6. **Add chemistry observables**
   - chemical diversity index;
   - reaction network connectivity;
   - longest stable reaction chain;
   - energy-gradient availability;
   - autocatalytic cycle count.

7. **Add examples**
   - strong binding → collapsed simple matter;
   - weak binding → no stable atoms;
   - rich chemistry window → many molecular networks;
   - no long-lived stars → limited heavy species.

### Self-check for missing facts

- Are stability rules derived from lower-level law parameters, or hand-coded to always allow chemistry?
- Can a universe fail to produce matter? It must be allowed to fail.
- Are chemistry modules overfitting to Earth-like assumptions?
- Is the mapping from microphysics to matter bridge documented?
- Does changing a fundamental coupling alter bound-state stability?

### Deliverables

- `MatterBridge`.
- bound-state toy solver.
- reaction network module.
- chemistry graph module.
- matter examples and tests.

### Evidence and acceptance

- A low-coupling LawBook produces no stable atom-like species.
- A baseline toy LawBook produces a nontrivial reaction graph.
- Reaction network outputs are deterministic under seed.
- Chemistry complexity metrics are saved and plotted.
- Life modules refuse to run when matter bridge lacks minimum chemical complexity.

### Do not proceed until

The engine can demonstrate that changing microphysical constants changes matter/chemistry outcomes.

---

## M8 — Stars, galaxies, black holes, and feedback layer

### Goal

Add astrophysical formation modules: halos, gas cooling, star formation analogues, stellar evolution, heavy-element enrichment, black-hole seeds, feedback, and galaxy morphology.

### Why it matters

Macroscopic universe generation must produce long-lived energy sources, chemical enrichment, and structured environments. Stars and galaxies are central bridges to planets and life.

### Implementation plan

1. **Define `AstroBridge`**
   - halo catalog;
   - gas/matter composition;
   - cooling rules;
   - star formation thresholds;
   - stellar lifetime model;
   - enrichment model;
   - feedback parameters.

2. **Implement cooling approximation**
   - Cooling function from MatterBridge composition.
   - Temperature/density dependent cooling times.
   - Validate trends, not precision.

3. **Implement star formation toy model**
   - Gas cells or halos above density/cooling threshold form star particles.
   - Star mass function configurable.
   - Star lifetime and luminosity from simplified scaling.

4. **Implement stellar nucleosynthesis analogue**
   - Stars produce heavier composite species depending on mass/lifetime.
   - Output abundance evolution.
   - Support failure when microphysics does not permit stable heavy species.

5. **Implement feedback**
   - Radiation/thermal/kinetic feedback toy model.
   - Supernova-like enrichment events.
   - Black-hole-like accretion feedback optional.

6. **Implement galaxy catalog**
   - Stellar mass.
   - Gas mass.
   - metallicity-like enrichment.
   - star-formation history.
   - morphology metrics.

7. **Add examples**
   - universe with fast stellar burnout;
   - universe with no heavy elements;
   - universe with many small galaxies;
   - universe with suppressed galaxy formation.

### Self-check for missing facts

- Are stellar models compatible with matter bridge outputs?
- Does star formation require cooling, or does it happen by arbitrary threshold?
- Are feedback parameters law-dependent or arbitrary?
- Are heavy elements possible under the selected LawBook?
- Do outputs include uncertainty/assumption metadata?

### Deliverables

- astrophysics process package;
- star and galaxy catalogs;
- enrichment history observer;
- examples and tests.

### Evidence and acceptance

- High cooling efficiency leads to earlier star formation in controlled tests.
- No-stable-heavy-species LawBook produces no enrichment beyond allowed composites.
- Galaxy catalog saved with reproducible schema.
- Star formation histories change when gravity/cooling/matter rules change.

### Do not proceed until

The engine can produce law-dependent star/galaxy histories connected to earlier matter and structure modules.

---

## M9 — Planetary systems and environments

### Goal

Generate planet-like environments from star/galaxy outputs: disks, planets, orbital stability, surface/atmosphere/ocean analogues, energy gradients, and habitability metrics.

### Why it matters

Life requires localized environments with stable matter, energy flow, and long-lived conditions. This phase creates the bridge from cosmic structure to biospheres.

### Implementation plan

1. **Define `PlanetaryBridge`**
   - star catalog subset;
   - heavy-element/composite abundance;
   - disk material;
   - orbital rules;
   - radiation environment;
   - chemistry inventory;
   - environment stability windows.

2. **Implement disk/planet formation toy model**
   - Planet occurrence depends on enrichment and disk mass.
   - Generate planet mass/radius/orbit distributions.
   - Orbital stability checks.

3. **Implement environment model**
   - Temperature equilibrium approximation.
   - Atmosphere retention proxy.
   - Liquid-solvent analogue criterion.
   - Tidal/radiation stress metric.

4. **Implement geochemical cycling placeholder**
   - Volcanism/tectonics analogue optional.
   - Surface reaction cycling.
   - Long-term climate stability proxy.

5. **Add habitability observer**
   - stable energy gradient duration;
   - chemical diversity at surface;
   - solvent stability window;
   - radiation hazard;
   - catastrophic event rate.

6. **Add examples**
   - rich planetary universe;
   - no heavy elements → no rocky planets;
   - unstable stars → short habitability windows;
   - altered gravity → different atmosphere retention.

### Self-check for missing facts

- Does planet formation depend on earlier enrichment outputs?
- Does habitability fail when chemistry is too simple?
- Are Earth-specific assumptions clearly marked?
- Can a universe produce life in non-Earth-like chemical windows if configured?
- Are orbital units consistent with gravity law?

### Deliverables

- planetary process package;
- planet catalog;
- habitability metrics;
- examples and tests.

### Evidence and acceptance

- No-enrichment universe produces few/no complex planets.
- Stable long-lived stars increase habitable duration metrics.
- Changing gravity changes orbital/atmospheric stability metrics.
- Planet catalog is saved and linked to parent star/galaxy IDs.

### Do not proceed until

The engine can produce reproducible planet catalogs whose properties depend on earlier physics layers.

---

## M10 — Life and evolution modules

### Goal

Add a life-emergence layer based on chemistry, energy gradients, replication, mutation, selection, ecology, and extinction.

### Why it matters

The user’s final target includes biological emergence. This must not be a decorative random label; it must depend on chemical and environmental constraints produced by earlier modules.

### Implementation plan

1. **Define `BiosphereBridge`**
   - planet environment history;
   - chemical network;
   - available energy gradients;
   - solvent/temperature windows;
   - catastrophe rates;
   - prebiotic reaction opportunities.

2. **Implement prebiotic chemistry module**
   - Search for autocatalytic cycles in reaction network.
   - Compute energy feasibility.
   - Create proto-replicator candidates only if cycles exist.

3. **Implement replicator model**
   - Replicators have sequence/trait vector.
   - Replication rate depends on environment and resources.
   - Mutation rate configurable.
   - Heritability and error threshold.

4. **Implement selection/ecology**
   - Resource competition.
   - Predation/cooperation optional.
   - Spatial niches.
   - Extinction events.
   - Diversity metrics.

5. **Implement complexity growth metrics**
   - genome length analogue;
   - metabolic network size;
   - ecological trophic levels;
   - information storage;
   - adaptation rate.

6. **Add examples**
   - no-autocatalysis universe → no life;
   - high mutation universe → error catastrophe;
   - stable planet universe → persistent biosphere;
   - frequent catastrophes → punctuated evolution.

### Self-check for missing facts

- Does life require chemical cycles generated by the chemistry module?
- Does life fail gracefully when conditions are not met?
- Are we avoiding guaranteed emergence?
- Is biological complexity measured, not asserted?
- Are stochastic outcomes evaluated over ensembles, not single seeds only?

### Deliverables

- biology process package;
- biosphere bridge;
- prebiotic autocatalysis detector;
- replicator/evolution model;
- life outcome observer;
- examples and tests.

### Evidence and acceptance

- A planet with no energy gradient produces no life events.
- A reaction network with autocatalytic cycles can seed replicators.
- Same seed reproduces life history.
- Ensemble scan reports probability of life emergence under a law family.
- Complexity metrics are saved over time.

### Do not proceed until

Life emergence depends on lower-scale chemistry and environment, not on arbitrary random spawning.

---

## M11 — Intelligence, agents, and civilization modules

### Goal

Model the possible emergence of intelligence and civilization from biosphere outputs through agents, cognition, communication, culture, technology, energy use, cooperation/conflict, and societal evolution.

### Why it matters

The long-term “创世” vision includes not only cosmic structure but also living, intelligent, social worlds. This phase must be modular, cautious, and evidence-based.

### Implementation plan

1. **Define `IntelligenceBridge`**
   - biosphere diversity;
   - ecological stability;
   - candidate intelligent species traits;
   - energy availability;
   - environmental pressures;
   - sociality opportunities;
   - catastrophe risks.

2. **Implement agent trait model**
   - cognition capacity;
   - learning rate;
   - communication ability;
   - cooperation tendency;
   - tool-use potential;
   - reproduction/lifecycle;
   - energy needs.

3. **Implement cultural transmission**
   - Memory/knowledge store.
   - Teaching/imitation.
   - Innovation events.
   - Loss of knowledge under collapse.

4. **Implement technology tree**
   - Technology nodes require resources, energy, knowledge, population, and stability.
   - Examples: fire-like energy control, agriculture-like resource amplification, writing-like memory externalization, industry-like energy scaling, computing-like cognition extension, spaceflight-like expansion.
   - Keep technology tree configurable, not Earth-deterministic.

5. **Implement society dynamics**
   - groups, settlements, networks;
   - trade and exchange;
   - conflict/cooperation;
   - institutions;
   - resource depletion;
   - collapse and recovery.

6. **Implement civilization observers**
   - population history;
   - technology level;
   - energy use;
   - network connectivity;
   - knowledge complexity;
   - conflict/collapse events;
   - expansion beyond home planet.

7. **Add examples**
   - high cooperation civilization;
   - high conflict collapse;
   - resource-poor stagnation;
   - unstable biosphere prevents civilization;
   - altered physics reduces energy extraction pathways.

### Self-check for missing facts

- Does intelligence depend on biosphere history and environment?
- Is civilization treated as stochastic and contingent, not guaranteed?
- Are ethical concerns documented when simulating agents/civilizations?
- Are social models clearly toy models?
- Does the module avoid real-world political prescriptions or deterministic claims?

### Deliverables

- agent/civilization process package;
- civilization bridge;
- technology tree config;
- society observer;
- examples and tests.

### Evidence and acceptance

- A biosphere with insufficient complexity cannot create intelligence candidates.
- Same seed reproduces civilization event timeline.
- Changing environmental energy availability changes technology progression.
- Collapse/recovery events are recorded with causes.
- Civilization outcome distributions are reported over multiple seeds.

### Do not proceed until

Civilization modules consume biosphere and planetary constraints rather than running as an isolated game simulation.

---

## M12 — Law-space scans and AI inverse design

### Goal

Enable systematic exploration of law space: change constants, symmetries, interactions, potentials, and process rules; run ensembles; measure outcomes; use optimization/ML to search for universes with target properties.

### Why it matters

The signature feature is that changing fundamental physics generates different micro/macro universes. This phase turns QuantaEngine into a discovery engine.

### Implementation plan

1. **Define scan config**
   - Parameter ranges.
   - Discrete law variants.
   - Mutation operators.
   - Seed ensembles.
   - Budget limits.
   - Metrics to optimize.

2. **Add scan runner**
   - Local multiprocessing first.
   - Resume incomplete scans.
   - Store results table.
   - Deduplicate repeated law hashes.

3. **Add comparison metrics**
   - microphysics: stable species, event rates;
   - matter: chemistry complexity;
   - cosmology: structure metrics;
   - astronomy: star/galaxy abundance;
   - planets: habitability windows;
   - biology: life emergence probability;
   - civilization: technology/collapse/expansion metrics.

4. **Add law mutation operators**
   - constant scaling;
   - coupling perturbation;
   - field addition/removal;
   - symmetry breaking scale change;
   - potential shape change;
   - interaction enable/disable;
   - gravity law variant.

5. **Add optimization tools**
   - random search;
   - grid search;
   - Bayesian optimization later;
   - evolutionary search over LawBooks;
   - surrogate models trained on scan outputs.

6. **Add inverse design examples**
   - Find universes with stable matter.
   - Find universes with rich chemistry.
   - Find universes with long-lived stars.
   - Find universes with high probability of life.
   - Find universes with civilization emergence.

### Self-check for missing facts

- Are scans comparing law changes or only seed changes?
- Are metrics robust across random seeds?
- Are failed universes recorded, not ignored?
- Does optimization exploit bugs or invalid states?
- Are validators used as hard constraints in search?

### Deliverables

- `quantaengine scan` CLI.
- scan result schema.
- law mutation package.
- comparison dashboard script.
- inverse design examples.

### Evidence and acceptance

- A scan over gravity/coupling constants produces a table where micro/macro metrics change systematically.
- Failed universes are included with failure reasons.
- Re-running a scan with same seeds reproduces result hashes.
- Optimization can recover a known target region in a toy benchmark.

### Do not proceed until

The scan system can prove, with saved data, that law changes produce different universe outcomes.

---

## M13 — Validation, benchmarks, and uncertainty

### Goal

Build a validation culture: every module has tests, every physical claim has a benchmark or limitation statement, every stochastic result has uncertainty, and every generated artifact is reproducible.

### Why it matters

A universe generator can easily become fantasy. Validation is what makes it a scientific engine.

### Implementation plan

1. **Create benchmark suite**
   - scalar field convergence toy benchmark;
   - decay exponential distribution;
   - Poisson event counts;
   - expansion known limiting cases;
   - N-body two-body or Zel'dovich-like toy check;
   - reaction network analytic cases;
   - replicator equation known regimes;
   - agent model controlled scenario.

2. **Create validation report format**
   - pass/warn/fail;
   - tolerance;
   - measured value;
   - expected value;
   - evidence file path;
   - module and law hash;
   - severity.

3. **Add uncertainty handling**
   - ensemble seeds;
   - bootstrap confidence intervals;
   - sensitivity to time step/resolution;
   - parameter uncertainty ranges;
   - stochastic variance.

4. **Add regression tests**
   - golden outputs for small demos;
   - statistical regression for stochastic modules;
   - image hashes only for diagnostics, not science.

5. **Add validation CLI**
   - `quantaengine validate --run runs/demo`.
   - `quantaengine benchmark --suite microphysics`.
   - `quantaengine compare --runs a b`.

### Self-check for missing facts

- Does a module have a benchmark in its validity domain?
- Is a warning enough, or should invalid outputs stop the run?
- Are tolerances justified or arbitrary?
- Do visual artifacts fool reviewers?
- Are results stable under reasonable resolution/time-step changes?

### Deliverables

- validation package;
- benchmark datasets/configs;
- validation report files;
- CLI validation commands;
- docs explaining limitations.

### Evidence and acceptance

- CI runs quick validation suite.
- Full validation suite can run locally.
- Each module page lists assumptions and validation status.
- Invalid LawBook or unstable numerical run fails loudly.

### Do not proceed until

The project can distinguish “physically validated,” “toy but internally consistent,” “experimental,” and “invalid.”

---

## M14 — Performance, parallelism, and production runs

### Goal

Make QuantaEngine capable of large parameter scans and multi-scale simulations with reproducible performance.

### Why it matters

Law-space exploration requires many universes, not one universe. Performance must not destroy reproducibility.

### Implementation plan

1. **Profile current bottlenecks**
   - field evolution;
   - FFTs;
   - N-body deposition;
   - reaction networks;
   - agent simulation;
   - I/O.

2. **Add backend acceleration**
   - JAX optional backend for differentiable/scannable kernels.
   - CuPy optional backend for GPU arrays.
   - PyTorch optional backend for ML-related modules.

3. **Add parallel scan runner**
   - local multiprocessing;
   - joblib/dask/ray optional;
   - SLURM template for clusters;
   - reproducible seed splitting.

4. **Add chunked I/O**
   - Zarr/HDF5 for large arrays.
   - Parquet for catalogs.
   - Compression settings in config.

5. **Add performance benchmarks**
   - fixed-size benchmark runs;
   - memory use tracking;
   - output size tracking;
   - CI small benchmark with threshold.

### Self-check for missing facts

- Does parallel execution change random results?
- Does GPU backend produce acceptable numerical differences?
- Are output files too large for typical users?
- Is checkpointing efficient enough for long runs?
- Can interrupted scans resume safely?

### Deliverables

- backend plugins;
- scan scheduler;
- benchmark scripts;
- HPC docs;
- reproducible seed splitting tests.

### Evidence and acceptance

- Parallel scan with same config produces same result table as serial scan.
- Backend comparison reports numerical differences within documented tolerance.
- Large run can checkpoint and resume.
- Performance report generated for release.

### Do not proceed until

The project can run law scans without sacrificing reproducibility.

---

## M15 — Observatory, visualization, and public-facing exploration

### Goal

Create a user-facing layer for exploring generated universes: maps, timelines, catalogs, parameter comparisons, civilization histories, and law-difference dashboards.

### Why it matters

The project needs to be understandable to physicists, developers, educators, science-fiction creators, and general users. Visualization must explain the causal chain from laws to outcomes.

### Implementation plan

1. **Create observatory data model**
   - loads run metadata;
   - discovers data products;
   - links outputs across scales;
   - displays validation status.

2. **Add visualization scripts**
   - early field maps;
   - power spectra;
   - density/cosmic web maps;
   - halo/galaxy catalogs;
   - chemical network graphs;
   - biosphere diversity timelines;
   - civilization event timelines;
   - law-change comparison panels.

3. **Add notebooks or static reports**
   - `notebooks/01_first_universe.ipynb`;
   - `notebooks/02_change_gravity.ipynb`;
   - `notebooks/03_from_law_to_life.ipynb`;
   - static markdown alternatives for non-notebook users.

4. **Add web dashboard later**
   - Streamlit or Panel prototype.
   - Run browser for local artifacts.
   - No cloud dependency required.

5. **Add storytelling mode**
   - Generate a human-readable universe history from saved observables.
   - Explicitly mark generated narrative as interpretation of simulation outputs.

### Self-check for missing facts

- Are plots reproducible from saved numeric data?
- Does visualization hide failed validators?
- Are narratives grounded in actual outputs?
- Can a user compare two LawBooks side by side?
- Are scientific limitations visible in the dashboard?

### Deliverables

- observatory package;
- static report generator;
- comparison plots;
- timeline outputs;
- example notebooks/reports.

### Evidence and acceptance

- `quantaengine report --run runs/demo` creates a static HTML or Markdown report.
- Report includes config hash, law hash, validation status, key metrics, and plots.
- Comparing two law variants shows which constants changed and which outcomes changed.
- Narrative timeline is traceable to saved data products.

### Do not proceed until

The observatory helps users understand how microscopic law changes caused macroscopic outcome differences.

---

# Final integration target

The complete QuantaEngine vision is achieved when a user can run:

```bash
quantaengine run --config examples/full_stack/standard_toy_universe.yaml --out runs/standard
quantaengine run --config examples/full_stack/low_alpha_universe.yaml --out runs/low_alpha
quantaengine compare --runs runs/standard runs/low_alpha --report reports/law_difference.html
```

and obtain evidence that includes:

1. fundamental constants and law hashes differ;
2. microphysical stability and interaction tables differ;
3. matter/chemistry networks differ;
4. star/galaxy formation histories differ;
5. planet/habitability windows differ;
6. life emergence probabilities differ;
7. intelligence/civilization outcomes differ or fail for documented reasons;
8. every result is reproducible from config, code version, and seed;
9. validators report which claims are toy, validated, warning, or invalid.

This is the concrete engineering expression of the project idea:

```text
Change the fundamental laws → change the microscopic rules → change matter → change cosmic structure → change life and civilization outcomes.
```
