# 修复方案包：codebase-remediation-2026-06-21b

针对独立评估 [`QE-REVIEW-2026-06-21B`](../../docs/reviews/2026-06-21b-codebase-assessment.md)
（基线 `2ab9917`）的 10 项 finding 的可执行修复规划。

| 字段 | 值 |
|---|---|
| 状态 | `planned`（仅规划，**本轮不含源码实现**） |
| 基线提交 | `2ab9917708b2ba1574301d48196743c4771a2282` |
| 评估报告 | [2026-06-21b-codebase-assessment.md](../../docs/reviews/2026-06-21b-codebase-assessment.md) |
| Findings | P1×3、P2×4、P3×3 |

## 文件

- [`PLAN_MANIFEST.yaml`](PLAN_MANIFEST.yaml) — 机读：每个 finding 的拟改文件与拟加回归测试、phase、验收门禁、不变量。
- [`EXECUTION_REPORT.md`](EXECUTION_REPORT.md) — 设计说明，重点是 `QE-2026-101`「独立考虑建议」回路。
- [`TRACEABILITY_MATRIX.md`](TRACEABILITY_MATRIX.md) — finding → 拟改代码 → 拟加测试 → 验收。
- [`ITERATION_GUIDE.md`](ITERATION_GUIDE.md) — 实现/复审流程。

## 核心设计原则（用户确认的意图）

> 每个方案保持**独立**；对抗产出是给对方的**建议**；接收方不是盲目听众，要用自己的标准
> **谨慎独立复核**，**只有自己独立确认正确才采纳进优化**，否则拒绝并记录。**绝不合并。**

## Phase 顺序

1. **A 可信对抗回路**：`QE-2026-101`（独立考虑建议）、`QE-2026-102`（评分目标去自报化）。
2. **B 科学可信度**：`QE-2026-103`（物理校准）、`QE-2026-110`（物理不变量测试）。
3. **C 性能与扩展**：`QE-2026-104/105/106/108`。
4. **D 维护与文档**：`QE-2026-107/109`。

## 实现后流程

按 [ITERATION_GUIDE.md](ITERATION_GUIDE.md)：实现 → 跑验收门禁 → 写复审报告
`docs/reviews/2026-06-21b-codebase-remediation.md` → 在 `index.yaml` 把对应 finding 置 `verified`。
