# Future Module API Contracts

This document defines the contracts that QuantaEngine should converge toward. The current seed repository is intentionally simple; these contracts are the target for the Geant4-style modular engine.

The rule is simple: every major physical or emergent behavior must be a replaceable module with declared inputs, outputs, assumptions, validation hooks, and reproducibility metadata.

## 1. `LawBook`

### Purpose

A `LawBook` is the complete machine-readable definition of a generated universe's fundamental and effective laws.

It should include:

- dimensional system and unit convention;
- fundamental constants;
- fields;
- particles or quasi-particles;
- symmetries;
- couplings;
- allowed interactions;
- potentials/actions;
- phase-transition rules;
- gravity/cosmology assumptions;
- effective chemistry/matter rules if lower layers are approximated;
- allowed biological and agent-level abstractions if higher layers are active.

### Minimal target interface

```python
class LawBook(Protocol):
    name: str
    version: str
    law_hash: str

    def constants(self) -> ConstantTable: ...
    def fields(self) -> list[FieldDefinition]: ...
    def species(self) -> list[SpeciesDefinition]: ...
    def interactions(self) -> list[InteractionDefinition]: ...
    def symmetries(self) -> list[SymmetryDefinition]: ...
    def parameters_for(self, module_name: str) -> Mapping[str, Any]: ...
    def validate(self) -> ValidationReport: ...
    def to_config(self) -> dict[str, Any]: ...
```

### Required invariants

- Every constant has units or is explicitly dimensionless.
- Every field/species has a stable ID.
- Every interaction references existing species/fields.
- Every module-specific parameter is namespaced.
- `law_hash` changes whenever any law-defining value changes.
- The law file can be round-tripped from YAML/JSON without losing meaning.

### Common traps

- Calling something a different universe while only changing a numerical seed.
- Mixing SI units, natural units, and dimensionless toy units without metadata.
- Allowing hidden defaults to define physical laws.
- Using constants hard-coded inside solvers.

## 2. `State`

### Purpose

A `State` stores the complete dynamic state of a universe at a time/scale step.

QuantaEngine will need multiple state representations:

- dense lattice fields;
- adaptive mesh fields;
- particle clouds;
- interaction graphs;
- reaction networks;
- agent populations;
- civilization event histories;
- hybrid combinations.

### Minimal target interface

```python
class State(Protocol):
    step_index: int
    time: float
    scale_factor: float | None
    law_hash: str

    def copy(self) -> "State": ...
    def variables(self) -> Mapping[str, Any]: ...
    def get(self, key: str) -> Any: ...
    def set(self, key: str, value: Any) -> None: ...
    def summary(self) -> dict[str, float | int | str]: ...
    def checksum(self) -> str: ...
```

### Required invariants

- State checksum is deterministic for the same content.
- State knows the `law_hash` that created it.
- State cannot silently switch units.
- State can be serialized to a checkpoint.
- State summary contains enough metadata to debug a run.

## 3. `StateSpace`

### Purpose

A `StateSpace` defines where the state lives: grid, graph, manifold, particle phase space, planet surface, ecology map, or social network.

### Minimal target interface

```python
class StateSpace(Protocol):
    name: str
    dimensions: int

    def coordinates(self) -> Any: ...
    def topology(self) -> Topology: ...
    def volume_element(self) -> Any: ...
    def neighbors(self, index: Any) -> Iterable[Any]: ...
    def validate_state(self, state: State) -> ValidationReport: ...
```

### Needed implementations

- `UniformLatticeStateSpace`
- `AdaptiveMeshStateSpace`
- `ParticlePhaseSpace`
- `ReactionNetworkStateSpace`
- `HabitatGridStateSpace`
- `AgentNetworkStateSpace`
- `HybridStateSpace`

## 4. `Process`

### Purpose

A `Process` is the central Geant4-like abstraction. It represents one physical, chemical, biological, or social mechanism that can update the state.

### Minimal target interface

```python
class Process(Protocol):
    name: str
    version: str
    domain: str
    required_state_variables: set[str]
    produced_state_variables: set[str]

    def configure(self, lawbook: LawBook, config: Mapping[str, Any]) -> None: ...
    def validate_inputs(self, state: State) -> ValidationReport: ...
    def propose_step(self, state: State, context: StepContext) -> StepProposal: ...
    def apply(self, state: State, proposal: StepProposal, context: StepContext) -> State: ...
    def observables(self, state: State) -> Mapping[str, Any]: ...
```

### Process metadata

Every process must declare:

```yaml
name: gravity.particle_mesh
version: 0.1.0
domain: cosmology
assumptions:
  - Newtonian weak-field approximation
  - periodic boundary conditions
valid_range:
  redshift_min: 0
  redshift_max: 1000
  density_contrast_max: 1000
requires:
  state_variables: [density, velocity, scale_factor]
produces:
  state_variables: [gravitational_potential, acceleration]
validation:
  - poisson_residual
  - momentum_conservation
```

### Process categories and examples

| Domain | Example process | Update style |
|---|---|---|
| fields | scalar field propagation | deterministic PDE step |
| particles | two-body scattering | Monte Carlo event |
| vacuum | bubble nucleation | stochastic event rate |
| cosmology | scale factor evolution | ODE step |
| gravity | particle-mesh gravity | PDE + particle update |
| chemistry | reaction network | stochastic/deterministic kinetics |
| biology | mutation/selection | stochastic agent/population update |
| society | cooperation/conflict | agent/network update |

### Required invariants

- `configure()` must fail early if the LawBook does not contain required constants.
- `propose_step()` must not mutate state.
- `apply()` must be deterministic given state, proposal, context, and random seed.
- Every stochastic process uses the shared `RandomService`, never `np.random` directly.
- Every process must expose observables for validation.

## 5. `Scheduler`

### Purpose

The scheduler determines how processes are ordered, synchronized, and stepped.

### Target modes

- fixed time step;
- adaptive time step;
- scale-factor step;
- event-driven Gillespie-like stochastic scheduling;
- operator splitting;
- hierarchical multi-scale stepping;
- asynchronous agent updates.

### Minimal target interface

```python
class Scheduler(Protocol):
    def initialize(self, processes: list[Process], state: State) -> None: ...
    def next_context(self, state: State) -> StepContext: ...
    def active_processes(self, context: StepContext) -> list[Process]: ...
    def done(self, state: State, context: StepContext) -> bool: ...
```

### Multi-scale scheduling rule

No high-level module should run faster than the lower-level bridge it depends on can justify. If biology consumes a chemistry bridge, the biology step must know when the chemistry bridge is stale.

## 6. `Observer`

### Purpose

Observers record outputs without changing state.

### Minimal target interface

```python
class Observer(Protocol):
    name: str
    cadence: int | str

    def configure(self, lawbook: LawBook, config: Mapping[str, Any]) -> None: ...
    def record(self, state: State, context: StepContext) -> DataProduct | None: ...
    def finalize(self) -> list[DataProduct]: ...
```

### Observer examples

- field snapshots;
- power spectra;
- correlation functions;
- halo catalogs;
- star catalogs;
- chemical network complexity;
- biosphere diversity;
- agent population metrics;
- technology level;
- civilization collapse/expansion events;
- synthetic sky maps.

## 7. `Validator`

### Purpose

Validators enforce scientific discipline. They decide whether a result is acceptable, suspicious, or invalid.

### Minimal target interface

```python
class Validator(Protocol):
    name: str
    severity: Literal["info", "warning", "error", "fatal"]

    def check(self, state: State, context: StepContext) -> ValidationReport: ...
    def finalize(self) -> ValidationReport: ...
```

### Validator classes

- units validator;
- conservation validator;
- positivity validator;
- stability/CFL validator;
- symmetry validator;
- statistical regression validator;
- benchmark comparison validator;
- law consistency validator;
- outcome plausibility validator;
- bridge freshness validator.

## 8. `ScaleBridge`

### Purpose

A `ScaleBridge` transfers validated lower-scale results to higher-scale modules.

Example bridges:

```text
LawBook → MicrophysicsBridge
MicrophysicsBridge → MatterBridge
MatterBridge → StellarBridge
StellarBridge → PlanetaryBridge
PlanetaryBridge → BiosphereBridge
BiosphereBridge → IntelligenceBridge
IntelligenceBridge → CivilizationBridge
```

### Minimal target interface

```python
class ScaleBridge(Protocol):
    source_scale: str
    target_scale: str
    law_hash: str
    created_from_run: str

    def validity_domain(self) -> dict[str, Any]: ...
    def uncertainty(self) -> dict[str, Any]: ...
    def validate(self) -> ValidationReport: ...
    def to_config_fragment(self) -> dict[str, Any]: ...
```

## 9. `RandomService`

### Purpose

All randomness must be deterministic, stream-safe, and auditable.

### Requirements

- A global seed determines the run.
- Each process gets a named random stream derived from the global seed.
- Random streams are independent and reproducible.
- Parallel runs do not change results unless explicitly configured.
- Metadata records all seeds and stream names.

### Example

```python
rng = random_service.stream("bio.mutation")
mutation_draws = rng.poisson(lambda_mutation, size=n_organisms)
```

## 10. `Backend`

### Purpose

Backends hide numerical array implementations.

### Target backends

- NumPy: default, transparent, CPU.
- JAX: differentiable, JIT, GPU/TPU possible.
- CuPy: GPU arrays with NumPy-like API.
- PyTorch: integration with ML modules.
- Dask/Ray/MPI layer: distributed parameter scans.

### Minimal target interface

```python
class Backend(Protocol):
    name: str
    xp: Any

    def array(self, data: Any) -> Any: ...
    def fftn(self, x: Any) -> Any: ...
    def ifftn(self, x: Any) -> Any: ...
    def random(self, seed: int) -> Any: ...
    def to_numpy(self, x: Any) -> np.ndarray: ...
```

## 11. `DataProduct`

### Purpose

A `DataProduct` is any reproducible result saved by a run.

### Required metadata

- product name;
- product type;
- run ID;
- law hash;
- config hash;
- code version;
- seed;
- time/step range;
- units;
- shape/schema;
- creation process;
- validation status.

### Output formats

- `.npz` for small arrays;
- HDF5 or Zarr for large arrays;
- Parquet for catalogs;
- JSON/YAML for metadata;
- PNG/SVG for diagnostic figures;
- SQLite/DuckDB for local exploratory products.

## 12. CLI contract

The future CLI should support:

```bash
quantaengine run --config examples/universe.yaml --out runs/u001
quantaengine validate --run runs/u001
quantaengine scan --config scans/law_scan.yaml --out scans/s001
quantaengine compare --runs runs/u001 runs/u002 --metrics all
quantaengine inspect law --config examples/universe.yaml
quantaengine inspect modules
quantaengine visualize --run runs/u001 --product density_final
quantaengine reproduce --run runs/u001 --out runs/u001_reproduced
```

Every command should be safe for CI tests using a small demo config.

## 13. Acceptance test for the API layer

The API layer is acceptable when the following minimal external plugin works:

```python
from quantaengine.kernel import Process

class ToyExpansionKick(Process):
    name = "toy.expansion_kick"
    domain = "cosmology"
    required_state_variables = {"scale_factor"}
    produced_state_variables = {"scale_factor"}

    def configure(self, lawbook, config):
        self.kick = config.get("kick", 1.001)

    def propose_step(self, state, context):
        return {"new_a": state.get("scale_factor") * self.kick}

    def apply(self, state, proposal, context):
        new_state = state.copy()
        new_state.set("scale_factor", proposal["new_a"])
        return new_state
```

YAML:

```yaml
processes:
  - module: toy.expansion_kick
    kick: 1.001
```

Evidence:

- plugin is loaded by registry;
- run metadata lists plugin;
- output scale factor changes by expected amount;
- deterministic re-run matches checksum;
- tests pass without editing engine internals.
