# Geant4-Style Architecture for QuantaEngine

## 1. Why Geant4 is the right architectural analogy

Geant4 is successful not because it is a single equation solver, but because it is a toolkit: geometry, materials, particles, physics processes, tracking, run/event management, visualization, and analysis are separated behind stable interfaces. Users can replace pieces without rewriting the whole program.

QuantaEngine needs the same spirit, but for universe generation rather than particle transport through matter.

The analogy is not one-to-one:

| Geant4 concept | Detector simulation meaning | QuantaEngine analogue | Universe-generation meaning |
|---|---|---|---|
| Run manager | Controls simulation run lifecycle | `UniverseRunManager` | Owns config, seeds, module graph, run metadata, checkpointing |
| Detector construction | Defines geometry and materials | `WorldConstruction` / `StateSpaceBuilder` | Defines lattice, manifold, topology, domains, cells, agents, environments |
| Physics list | Selects particles and processes | `LawBook` + `PhysicsProcessList` | Selects fundamental constants, fields, particles, interactions, cosmology, chemistry, life rules |
| Primary generator | Injects initial particles/events | `InitialConditionGenerator` | Creates vacuum state, fluctuations, fields, particles, density perturbations, biological seeds |
| Track | Particle trajectory | `EntityHistory` / `WorldLine` | History of particles, structures, organisms, agents, civilizations, fields, halos |
| Step | Local evolution increment | `EvolutionStep` | One time step, event step, scale-factor step, or adaptive causal update |
| Process | Interaction/decay/transport | `Process` plugin | Field update, scattering, gravity, chemistry, mutation, selection, social exchange, collapse |
| Sensitive detector | Records hits | `Observer` / `Probe` | Records fields, spectra, halos, stars, chemistry, organisms, technologies, societies |
| Hits/ntuples | Output measurements | `DataProduct` | Reproducible outputs: arrays, catalogs, event histories, observables, maps |
| Visualization | Visualize geometry and tracks | `Observatory` | Visualize universe fields, networks, phase transitions, galaxies, biospheres, civilizations |

The key principle is that a universe is not one simulation object. It is a coordinated run of many scale-specific modules connected by common contracts.

## 2. Architectural target

The future QuantaEngine should have this high-level structure:

```text
quantaengine/
  kernel/
    run_manager.py
    module_registry.py
    scheduler.py
    event.py
    state.py
    step.py
    random.py
    checkpoint.py
    metadata.py
  law/
    lawbook.py
    constants.py
    dimensions.py
    units.py
    symmetries.py
    actions.py
    couplings.py
  processes/
    base.py
    field_processes.py
    particle_processes.py
    gravity_processes.py
    chemistry_processes.py
    biology_processes.py
    society_processes.py
  state_spaces/
    lattice.py
    particle_cloud.py
    graph.py
    manifold.py
    hybrid_state.py
  initial_conditions/
    vacuum.py
    inflation.py
    thermal.py
    particle_source.py
    biosphere_seed.py
  solvers/
    ode.py
    pde.py
    monte_carlo.py
    nbody.py
    reaction_network.py
    agent_based.py
  observers/
    field_observer.py
    spectrum_observer.py
    structure_catalog.py
    biosphere_observer.py
    civilization_observer.py
  validation/
    invariants.py
    benchmark_suite.py
    regression.py
    uncertainty.py
  backends/
    numpy_backend.py
    jax_backend.py
    cupy_backend.py
    torch_backend.py
  io/
    config.py
    hdf5.py
    zarr.py
    metadata.py
  cli/
    run.py
    scan.py
    validate.py
    compare.py
    visualize.py
```

The repository does not need all of this immediately, but all future code should move toward these boundaries.

## 3. Core runtime cycle

A Geant4-style universe run should look like this:

```text
1. Load configuration
2. Build LawBook
3. Build state space
4. Register processes
5. Build initial conditions
6. Initialize observers and validators
7. Run scheduler loop
8. At each step:
   a. Ask processes for proposed updates or event rates
   b. Select deterministic/adaptive/Monte-Carlo update order
   c. Apply updates to the state
   d. Enforce constraints and units
   e. Record observables
   f. Run validation hooks
   g. Checkpoint if needed
9. Finalize run metadata
10. Produce reproducible data products
11. Run postprocessing and comparison tests
```

In pseudocode:

```python
manager = UniverseRunManager.from_config("universe.yaml")
manager.initialize()
while not manager.done:
    step_context = manager.scheduler.next_step(manager.state)
    for process in manager.process_list.active_processes(step_context):
        proposal = process.propose(manager.state, step_context)
        manager.state = process.apply(manager.state, proposal, step_context)
    manager.observers.record(manager.state, step_context)
    manager.validators.check(manager.state, step_context)
    manager.checkpoint_if_needed()
manager.finalize()
```

## 4. Scale separation and coupling

The hardest design problem is not implementing one module. The hard part is coupling scales without making everything untestable.

QuantaEngine should use explicit interfaces between scales:

```text
Microphysics module outputs:
  - particle masses
  - lifetimes
  - interaction strengths
  - scattering/decay rates
  - stable bound states
  - effective equations of state
  - radiative properties

Matter/chemistry module consumes:
  - stable charges and masses
  - binding rules
  - reaction rates
  - atomic/molecular analogues

Astrophysics module consumes:
  - gravity law
  - radiation transport approximations
  - nuclear/energy-generation rules
  - cooling functions
  - matter composition

Biology module consumes:
  - available chemical networks
  - energy gradients
  - environmental stability
  - mutation/inheritance rules
  - spatial habitats

Civilization module consumes:
  - agent cognition capacity
  - communication networks
  - resource distributions
  - energy extraction pathways
  - cooperation/conflict dynamics
```

Each module should export a `ScaleBridge` object: a compressed, validated representation of lower-scale behavior suitable for the next scale.

Example:

```python
@dataclass
class MicrophysicsBridge:
    law_hash: str
    stable_species: list[Species]
    interaction_table: InteractionTable
    decay_table: DecayTable
    effective_constants: dict[str, float]
    validation: ValidationReport
```

## 5. Process categories

Future `Process` plugins should be grouped by domain.

### Fundamental / microphysical processes

- field propagation
- field self-interaction
- symmetry breaking
- particle creation
- annihilation
- decay
- scattering
- bound-state formation
- vacuum transition
- thermalization

### Cosmological processes

- scale-factor evolution
- perturbation growth
- horizon crossing
- gravitational clustering
- dark-sector evolution
- phase transitions
- reheating analogues

### Matter processes

- nuclear binding analogues
- atomic binding analogues
- molecular network formation
- reaction kinetics
- radiative cooling
- condensed matter approximations

### Astrophysical processes

- N-body gravity
- hydrodynamics approximation
- halo formation
- star formation
- stellar burning analogue
- stellar feedback
- black-hole accretion
- galaxy merger

### Biological processes

- autocatalytic chemistry
- compartment formation
- replication
- mutation
- selection
- metabolism
- ecology
- extinction

### Intelligence and civilization processes

- agent learning
- communication
- tool creation
- cooperation
- conflict
- trade
- cultural transmission
- technology tree
- energy transition
- planetary engineering
- space expansion

## 6. Configuration-driven design

A user should be able to change the universe without editing Python code.

Target configuration style:

```yaml
run:
  name: low_alpha_universe
  seed: 123
  backend: numpy
  output: runs/low_alpha

lawbook:
  constants:
    c: 1.0
    hbar: 1.0
    G: 1.0
    alpha_em: 0.003
    strong_coupling_scale: 0.8
  symmetries:
    gauge_groups: [U1, SU2_like, SU3_like]
    broken_phases:
      - name: electroweak_like
        critical_temperature: 0.4
  fields:
    - name: inflaton_like
      type: scalar
      potential: quadratic_plus_quartic
    - name: photon_like
      type: vector
      gauge: U1

state_space:
  type: adaptive_lattice
  dimensions: 3
  box_size: 100.0
  grid_size: 256

processes:
  - module: expansion.friedmann
  - module: fields.scalar_lattice
  - module: gravity.particle_mesh
  - module: matter.binding_network
  - module: astro.star_formation
  - module: bio.autocatalytic_life
  - module: society.agent_civilization

observers:
  - power_spectrum
  - halo_catalog
  - star_catalog
  - chemistry_complexity
  - biosphere_diversity
  - civilization_events

validation:
  conservation:
    energy_tolerance: 1.0e-3
    charge_tolerance: 1.0e-12
  regression:
    compare_to: baseline_universe
```

## 7. Stability rules for architecture

Do not allow these anti-patterns:

1. **One giant `Universe` class** that knows everything.
2. **Hard-coded constants** inside numerical kernels.
3. **Pretty visualization without saved data**.
4. **Unseeded randomness**.
5. **Physics claims without validation**.
6. **Implicit unit conventions**.
7. **Scale coupling through ad hoc global variables**.
8. **Biology/civilization modules that ignore lower-scale constraints**.
9. **AI modules that optimize impossible worlds because validators are missing**.
10. **New feature PRs without config examples and tests**.

## 8. Minimal acceptable Geant4-style kernel

The first real kernel milestone is complete when QuantaEngine has:

- `UniverseRunManager`
- `ModuleRegistry`
- `LawBook`
- `StateSpace`
- `Process` base class
- `Observer` base class
- `Validator` base class
- `Scheduler`
- deterministic seeded `RandomService`
- checkpoint metadata
- CLI commands: `run`, `validate`, `scan`, `compare`
- at least three independent process plugins using the same process interface
- tests proving process order, seeding, serialization, and registry loading are deterministic

## 9. Evidence that the architecture is working

A contributor should be able to create a new process in one file, register it, add it to YAML, and run it without editing engine internals.

Acceptance demo:

```text
1. Create examples/plugins/toy_cooling.py
2. Register ToyCoolingProcess
3. Add it to examples/toy_cooling_universe.yaml
4. Run `quantaengine run --config examples/toy_cooling_universe.yaml`
5. Output metadata lists ToyCoolingProcess
6. Observer shows expected cooling trend
7. Unit tests verify the process is deterministic for seed=42
8. Removing the process changes the outcome in a predictable way
```

If this demo works, the project has achieved the basic Geant4-style modular pattern.
