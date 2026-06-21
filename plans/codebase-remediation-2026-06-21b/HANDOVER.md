# 交接任务：完成 remediation 方案包 B（Phase B/C/D）

> 这份文档是**下一个 AI 的输入**。目标：完成
> [`plans/codebase-remediation-2026-06-21b`](PLAN_MANIFEST.yaml) 里**尚未实现**的全部
> finding（Phase B/C/D），并按既有归档流程收尾。Phase A（`QE-2026-101`/`QE-2026-102`）
> 已实现并提交（commit `7b798a7`），**不要重做**。

## 0. 一句话目标

按 `PLAN_MANIFEST.yaml` 的 `planned_changes` 与 `planned_regression`，**先写测试（红）→ 再实现 → 全门禁转绿**，逐个修复 `QE-2026-103/104/105/106/107/108/109/110`，每完成一个就把 `docs/reviews/index.yaml` 对应 finding 置 `fixed`；全部完成后写复审报告并把 review 置 `verified`，提交推送 `main`。

## 1. 现状（必读）

- 仓库：`D:\05-universe\01-quanta-engine\quantaengine`，分支 `main`，远端 `origin`(mjincoin) + `quantaengine`(组织)。
- 基线门禁（当前全绿）：`106 passed`、覆盖率 `95.58%`、`ruff check`/`ruff format --check`/`mypy src` 均通过。
- 三层架构见 [`docs/design/REPO_STRUCTURE.md`](../../docs/design/REPO_STRUCTURE.md)：
  `cosmogenesis/core`（契约）、`cosmogenesis/schemes/<name>`（方案=engine.py+optimizer.py）、`cosmogenesis/arena`（平台）。
- 独立评估报告（问题全貌与行级证据）：[`docs/reviews/2026-06-21b-codebase-assessment.md`](../../docs/reviews/2026-06-21b-codebase-assessment.md)。
- 方案包权威清单：本目录 `PLAN_MANIFEST.yaml` / `EXECUTION_REPORT.md` / `TRACEABILITY_MATRIX.md` / `ITERATION_GUIDE.md`。

### Phase A 已完成（参考实现，勿动其语义）

- `QE-2026-101` 独立考虑建议回路：`ChallengeCard.suggestion`；`core/protocol.py::BaseEngine.consider()`（在**自身 objective** 下复核，自证改进才采纳，否则保留自身冠军，**永不合并**）；`bridge.consider()`；`duel.py` 接入并产出 `ConsiderationCard`；`ledger.py` 写入 `considerations` 轨迹。
- `QE-2026-102` 评分去自报化：各 engine 在 `diagnostics` 报 `compute_cost`/`free_parameters`；`scoring._efficiency`/`_simplicity` 改为引擎派生。
- 测试 `tests/test_remediation_b.py`（9 个，全绿）。

## 2. 待办（Phase B/C/D，逐个闭环）

按优先级 B → C → D。每个 finding 的拟改文件/测试见 `PLAN_MANIFEST.yaml` 与 `TRACEABILITY_MATRIX.md`；设计意图见 `EXECUTION_REPORT.md`。

| Finding | Phase | 要点 |
|---|---|---|
| `QE-2026-103` | B | 物理阈值校准：新增 `docs/design/PHYSICS_CALIBRATION.md`（每个 logistic 窗口阈值给来源/区间），engine 暴露阈值敏感性；标准宇宙锚点落在区间内。 |
| `QE-2026-110` | B | `tests/test_physics_invariants.py`：用 `hypothesis` 写守恒/量纲/单调（如引力↑→恒星寿命↓）/标准宇宙锚点属性测试。 |
| `QE-2026-104` | C | `bridge.assess` 按 `(theory_id, version, rounded-vector)` 记忆化；确定性不变、调用数下降。 |
| `QE-2026-105` | C | novelty archive 加**上限/时间衰减/去重**（`evolution.py`/`scoring.py`），长跑 novelty 不塌缩、成本有界。 |
| `QE-2026-106` | C | `schemes/__init__.py` 改**子包自动发现/entry-point** 注册（放入新 scheme 即生效）；`patchgate.py` 抽出冲突策略对象。 |
| `QE-2026-108` | C | `evolve` 加收敛指标（Pareto 稳定/分数增量阈值/family 稳定）+ 可选早停；默认行为不变。 |
| `QE-2026-107` | D | 新增 `docs/design/DEPRECATION.md`：`quantaengine_lattice` 定位（冻结/归档）+ `quantaengine` namespace 1.0 移除时间表与迁移说明。 |
| `QE-2026-109` | D | 给 `plans/2026-06-21-GENESIS_ARENA_V2_PARALLEL_ADVERSARIAL.md` 顶部加"已被 `docs/design/REPO_STRUCTURE.md` 取代"横幅。 |

## 3. 每个 finding 的工作流（务必遵守）

1. 在 `tests/test_remediation_b.py`（或 finding 指定的新测试文件）**先写回归测试**，命名见 `PLAN_MANIFEST.findings[].planned_regression`，确认先失败。
2. 实现最小改动使其转绿。提交信息引用 finding ID（如 `Fix QE-2026-104`）。
3. 跑全部验收门禁（见 §4）必须全绿。
4. 更新 `docs/reviews/index.yaml` 把该 finding `status: open → fixed`，补 `regression` 字段。
5. 该 Phase 全部完成可一并提交、推送 `main`。

## 4. 验收门禁（每次改动后都要全绿）

```bash
python -m pytest
python -m ruff check src tests
python -m ruff format --check src tests
python -m mypy src
python plans/codebase-remediation-2026-06-21/execution/check_coverage.py   # 总≥90% / patchgate≥85% / cli≥85%
```

## 5. 不可触碰的红线（实现期必须保持）

- **永不合并**：`allow_merge` 恒 False；任何"采纳建议"只更新接收方**自身谱系**冠军。
- **独立性**：接收方对建议的采纳只能用**自己的 `objective`** 判定，不得直接采用攻击方分数。
- **确定性**：禁止把 wall-clock/`time.time()` 等非确定量引入评分或种子；随机一律走 `core/reproducibility.py` 的 `stable_seed`/`stable_identifier`（已有）。并行与串行、跨 `PYTHONHASHSEED` 结果必须一致（已有相应回归测试，勿破坏）。
- **覆盖率不得低于门槛**；新代码要带测试。
- **时间戳用巴黎本机偏移**（`datetime.now().astimezone()`，见 `ledger.local_now`），绝不写死 `+08:00`。

## 6. 已知陷阱

- `bridge.build_engine` 每次新建 engine（带固定 seed）→ 这是 `consider`/`assess` 确定性的来源，做缓存（104）时不要破坏它。
- `tournament` 用隔离 registry + 确定性 reducer 保证并行可复现（前轮 `QE-2026-001` 修复）；改 `evolution`/`scoring` 时别在并行路径里共享可变状态。
- Windows 下 `git` 会提示 LF→CRLF，正常，忽略。
- 覆盖率脚本在 Windows 用文件系统源路径 `--cov=src/cosmogenesis`（见前轮 remediation §6 第 4 点）。
- 物理阈值在 `schemes/*/engine.py`，改阈值/加校准时跑标准宇宙锚点确认不回归（analytic 标准宇宙 civ≈1.0、variational≈0.86、minimal≈0.92）。

## 7. 收尾（全部 Phase 完成后）

1. 新建复审报告 `docs/reviews/2026-06-21b-codebase-remediation.md`，逐 finding 记录：修复提交、**独立验证证据**（数值/对比/接收方自身判定）、新增回归测试、剩余风险；引用本评估 `QE-REVIEW-2026-06-21B` 基线 `2ab9917` 不变。
2. `docs/reviews/index.yaml`：把 review B 的 `status` 置 `verified`，全部 finding 置 `verified` 并填 `fixed_in`；`README.md` 评估记录表更新状态。
3. `PLAN_MANIFEST.yaml` 的 `status: in-progress → verified`，补 `remediation_report` 路径。
4. 提交并 `git push origin main`（如需镜像组织远端 `quantaengine` 一并推送）。

## 8. 快速启动命令

```bash
cd /d/05-universe/01-quanta-engine/quantaengine
git log --oneline -3            # 应看到 7b798a7 Phase A
python -m pytest -q             # 确认 106 passed 基线
sed -n '1,80p' plans/codebase-remediation-2026-06-21b/PLAN_MANIFEST.yaml
# 然后从 QE-2026-103 开始按 §3 工作流推进
```
