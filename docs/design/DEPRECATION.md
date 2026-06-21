# Deprecation and legacy-retirement policy

This policy separates the frozen lattice prototype from the active effective-physics and
adversarial products. It is a compatibility schedule, not a promise to evolve every historical
API indefinitely.

## Product status

| Surface | Status | New development |
|---|---|---|
| `quanta_engine` | Active | Multi-scale effective-physics pipeline and `quanta` CLI |
| `cosmogenesis` | Active | Multi-scheme adversarial generation and `genesis-arena` CLI |
| `quantaengine_lattice` | **Frozen legacy archive** | Correctness/security/packaging fixes only; no new physics features |
| `quantaengine` | Deprecated compatibility namespace | No direct development; forwards to `quantaengine_lattice` |

The lattice prototype remains useful for reproducing historical scalar-field experiments, but it
is independent of the current universe compiler. New work must use `quanta_engine` or
`cosmogenesis`. A request for new lattice behavior should normally become a separate research
fork rather than expand the frozen package.

## Removal schedule

- **0.3.x (current):** `quantaengine` continues to import and emits `DeprecationWarning`.
  `python -m quantaengine` and the `quantaengine` console command remain compatibility shims.
- **0.4.x through 0.x:** compatibility remains available; release notes repeat the migration.
  Only break/fix changes needed to keep the shim working are accepted.
- **1.0.0, no earlier than 2027-06-21:** remove the `quantaengine` Python namespace and its
  deprecated console shim. The explicit `quantaengine_lattice` archive remains importable for
  historical reproducibility unless a later, separately announced archival release says otherwise.

Any schedule acceleration requires a new review record, a major-version release, and at least one
published release cycle of notice. Silent removal is forbidden.

## Migration

Python imports:

```python
# Before (deprecated)
from quantaengine import UniverseEngine

# Historical lattice API (explicit)
from quantaengine_lattice import UniverseEngine

# Current universe-generation work
from quanta_engine.pipeline import run_universe_pipeline
from cosmogenesis import evolve
```

Command line:

```bash
# Before (deprecated compatibility shim)
python -m quantaengine --help

# Historical lattice CLI (explicit module)
python -m quantaengine_lattice --help

# Active products
quanta --help
genesis-arena --help
```

Downstream packages should change dependency/import checks now; catching or suppressing the
warning is not a migration. Maintainers can verify removal readiness with:

```bash
rg "(^|[^_])quantaengine([^_]|$)" src tests examples
```

## Support boundary

Security and data-corruption fixes remain eligible for the frozen lattice archive. Performance
work, new solvers, new output formats, and expanded scientific claims belong in active packages or
a dedicated fork. Historical reports must record the exact package version and continue to name
`quantaengine_lattice` explicitly.
