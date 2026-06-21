# 迭代/复审流程（codebase-remediation-2026-06-21b）

本方案包 `status: planned`。实现时按下列流程，每个 finding 独立闭环。

## 实现一个 finding

1. 从 [`PLAN_MANIFEST.yaml`](PLAN_MANIFEST.yaml) 取该 finding 的 `planned_changes` 与 `planned_regression`。
2. 先写回归测试（红），再实现，使其转绿。提交信息引用 finding ID，例如 `Fix QE-2026-101`。
3. 保持全局不变量：`allow_merge` 恒 False；采纳建议必由接收方自身模型独立判定；不降低覆盖率门槛；不破坏跨进程/串并行确定性。

## Phase 顺序

A（对抗回路 101/102）→ B（科学校准 103/110）→ C（性能扩展 104/105/106/108）→ D（维护文档 107/109）。
A 为最高优先：它决定"多方案对抗演化"结论是否可信。

## 验收门禁

```bash
python -m pytest
python -m ruff check src tests
python -m ruff format --check src tests
python -m mypy src
python plans/codebase-remediation-2026-06-21/execution/check_coverage.py
```

## 复审与归档

1. 全部（或一个 Phase）finding 实现并门禁通过后，新建复审报告
   `docs/reviews/2026-06-21b-codebase-remediation.md`，逐 finding 记录：修复提交、
   **独立验证证据**（接收方自身模型判定/实测数值/对比）、新增回归测试、CI URL、剩余风险。
2. 在 [`docs/reviews/index.yaml`](../../docs/reviews/index.yaml) 把对应 finding 的 `status`
   从 `open` 更新为 `verified`，并填 `fixed_in`。
3. 在 [`docs/reviews/README.md`](../../docs/reviews/README.md) 评估记录表更新该 review 状态。
4. 把本 `PLAN_MANIFEST.yaml` 的 `status` 更新为 `verified` 并补 `remediation_report` 路径。

## 独立性红线（务必遵守用户意图）

- 接收方对建议的采纳判定，**只能用自己的 `objective`**，不得直接采用攻击方的分数。
- 采纳只更新接收方**自身谱系**的 champion，**绝不**把两方案合并成一个。
- 拒绝也要记录理由（独立验证结论），保证可回溯。
