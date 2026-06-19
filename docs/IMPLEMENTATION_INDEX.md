# QuantaEngine Implementation Index

This directory contains the long-form execution plan for turning QuantaEngine from a compact seed repository into a Geant4-style modular universe-generation engine.

The documents are intentionally written as engineering checklists rather than marketing notes. Each phase specifies the target, implementation plan, self-check questions, missing-fact traps, usable deliverables, and evidence required before the phase can be considered complete.

## Read order

1. [`design/geant4_style_architecture.md`](design/geant4_style_architecture.md)  
   Explains the Geant4-inspired architecture and how detector-simulation concepts map onto universe generation.

2. [`design/module_api_contracts.md`](design/module_api_contracts.md)  
   Defines the future plugin interfaces: `LawBook`, `Process`, `State`, `Stepper`, `Observer`, `Validator`, backends, registries, and run managers.

3. [`implementation/master_execution_checklist.md`](implementation/master_execution_checklist.md)  
   The main step-by-step execution plan. This is the document to turn into GitHub issues and milestones.

4. [`implementation/physics_scale_roadmap.md`](implementation/physics_scale_roadmap.md)  
   The physical-scale roadmap from microscopic laws to macroscopic universes, matter, stars, planets, life, intelligence, and civilization.

5. [`implementation/law_variation_protocol.md`](implementation/law_variation_protocol.md)  
   A protocol for changing fundamental laws and constants in a controlled way so different microphysics can produce genuinely different macro-universes.

6. [`validation/evidence_and_acceptance.md`](validation/evidence_and_acceptance.md)  
   Defines what counts as evidence: unit tests, conservation checks, benchmark recovery, statistical regression, reproducibility, and generated observables.

7. [`experiments/flagship_experiment_from_quanta_to_civilization.md`](experiments/flagship_experiment_from_quanta_to_civilization.md)  
   The long-term flagship experiment: generate universes from fundamental rules, evolve structure, matter, planets, biospheres, agents, and civilizations, then compare outcomes under law changes.

## Core principle

QuantaEngine should not become a single monolithic simulation. It should become a toolkit in the same spirit as Geant4: a small number of stable orchestration abstractions, many replaceable physics modules, strict reproducibility, explicit validation, and configuration-driven experiments.

The ambition is broader than detector transport: QuantaEngine aims to model causal chains across scales.

```text
Fundamental law choices
    → quantum / field / particle microphysics
    → effective matter and interaction rules
    → cosmological expansion and structure formation
    → stars, heavy elements, chemistry, planets
    → prebiotic chemistry, life, ecology
    → intelligence, technology, civilization dynamics
    → observable universe histories and outcome distributions
```

## Naming convention for future milestones

Use milestone IDs in issues, pull requests, and docs:

```text
M0   Repository hardening
M1   Geant4-style kernel
M2   Units, dimensions, constants, and LawBook DSL
M3   State spaces and numerical backends
M4   Microphysics plugin layer
M5   Quantum/field/vacuum/phase-transition layer
M6   Cosmology and structure formation layer
M7   Matter, nuclear, atomic, chemistry layer
M8   Stars, galaxies, black holes, and feedback layer
M9   Planetary systems and environments
M10  Life and evolution modules
M11  Intelligence, agents, and civilization modules
M12  Law-space scans and AI inverse design
M13  Validation, benchmarks, and uncertainty
M14  Performance, parallelism, and reproducible production runs
M15  User-facing observatory, visualization, and data products
```

## Practical rule

A feature is not done when it produces a pretty image. A feature is done only when:

1. it has an explicit model assumption document;
2. it has a config example;
3. it has a deterministic seed test;
4. it has at least one physical, mathematical, or statistical validation check;
5. it produces a saved artifact that another user can reproduce;
6. it is connected to the documentation and CLI.
