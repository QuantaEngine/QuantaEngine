# QuantaEngine Code Execution Plan

This is the top-level entry point for the detailed implementation plan.

The full plan is split across several documents so that each part can become GitHub milestones and issues without overloading the README.

Start here:

- [`docs/IMPLEMENTATION_INDEX.md`](docs/IMPLEMENTATION_INDEX.md)
- [`docs/implementation/master_execution_checklist.md`](docs/implementation/master_execution_checklist.md)
- [`docs/design/geant4_style_architecture.md`](docs/design/geant4_style_architecture.md)
- [`docs/design/module_api_contracts.md`](docs/design/module_api_contracts.md)
- [`docs/implementation/physics_scale_roadmap.md`](docs/implementation/physics_scale_roadmap.md)
- [`docs/implementation/law_variation_protocol.md`](docs/implementation/law_variation_protocol.md)
- [`docs/validation/evidence_and_acceptance.md`](docs/validation/evidence_and_acceptance.md)
- [`docs/experiments/flagship_experiment_from_quanta_to_civilization.md`](docs/experiments/flagship_experiment_from_quanta_to_civilization.md)

## Chinese summary

这份执行计划的核心目标是把 QuantaEngine 从当前的最小可运行科学计算种子框架，逐步扩展成类似 Geant4 风格的模块化物理引擎。

最终目标不是一个单一脚本，而是一个可组合工具包：

```text
基础物理定律 / LawBook
  → 量子涨落与微观混沌
  → 场、粒子、相互作用、衰变、散射
  → 稳定物质、原子/分子类结构、化学网络
  → 宇宙膨胀、引力聚集、星系结构
  → 恒星、重元素、行星、宜居环境
  → 生命、演化、生态系统
  → 智慧生命、技术、文明社会
  → 可观测宇宙历史与跨宇宙对比
```

改变基础物理定律时，系统必须能通过保存的数据和验证报告证明：微观规则改变如何逐层传递到宏观结构、物质复杂度、生命概率和文明演化结果。

## How to use this in GitHub

Recommended milestone creation order:

```text
M0  Repository hardening
M1  Geant4-style kernel
M2  Units, dimensions, constants, and LawBook DSL
M3  State spaces and numerical backends
M4  Microphysics plugin layer
M5  Quantum/field/vacuum/phase-transition layer
M6  Cosmology and structure formation layer
M7  Matter, nuclear, atomic, chemistry layer
M8  Stars, galaxies, black holes, feedback layer
M9  Planetary systems and environments
M10 Life and evolution modules
M11 Intelligence, agents, and civilization modules
M12 Law-space scans and AI inverse design
M13 Validation, benchmarks, and uncertainty
M14 Performance, parallelism, and production runs
M15 Observatory, visualization, and reports
```

Each milestone should be broken into issues using the templates under `.github/ISSUE_TEMPLATE/`.
