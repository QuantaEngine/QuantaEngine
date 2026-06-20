# 说明文档映射

## 本方案包内

- `README.md`：方案入口、状态和复验命令。
- `PLAN_MANIFEST.yaml`：机器可读执行契约。
- `EXECUTION_REPORT.md`：详细执行说明和决策。
- `TRACEABILITY_MATRIX.md`：需求、代码、测试和证据映射。
- `ITERATION_GUIDE.md`：同方案优化和新方案分叉流程。

## 仓库级文档

| 文档 | 与本方案的关系 |
|---|---|
| `README.md` | 用户安装、运行、比较和扫描入口 |
| `docs/physics_assumptions.md` | 标准公式、toy model、heuristics 和禁止过度解读项 |
| `docs/api_reference.md` | 当前公开 Python API |
| `docs/examples.md` | 标准和失败型宇宙案例 |
| `docs/MVP_COMPLETION.md` | 阶段级完成和验证摘要 |
| `docs/architecture.md` | 原型架构背景 |
| `docs/design/module_api_contracts.md` | 更长期模块契约设计 |
| `docs/implementation/physics_scale_roadmap.md` | 超出 MVP 的多尺度路线 |
| `docs/validation/evidence_and_acceptance.md` | 长期证据等级设计 |

## 源码与执行入口

| 目录 | 用途 |
|---|---|
| `src/quanta_engine/` | 本方案的主管线实现 |
| `src/quantaengine/` | 保留兼容的旧格点原型 |
| `configs/` | 标准宇宙和变体输入 |
| `tests/` | 单元、集成、CLI、扫描和 E2E 验证 |
| `examples/` | 面向开发者的运行示例 |
| `reports/` | 可提交的参考输出 |
| `.github/workflows/tests.yml` | 远端持续验证 |

文档修改若改变了阈值或行为，必须同步更新 manifest、追踪矩阵、测试和验收证据。
