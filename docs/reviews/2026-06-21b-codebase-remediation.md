# QuantaEngine 代码库修复复审（独立评估 B）

## 复审元数据

| 字段 | 值 |
|---|---|
| Review ID | `QE-REVIEW-2026-06-21B` |
| 原始评估基线 | `2ab9917708b2ba1574301d48196743c4771a2282`（保持不变） |
| 原始评估 | [`2026-06-21b-codebase-assessment.md`](2026-06-21b-codebase-assessment.md) |
| 修复方案 | [`plans/codebase-remediation-2026-06-21b`](../../plans/codebase-remediation-2026-06-21b/README.md) |
| 实现提交 | `7b798a7`、`d16336f`、`e1a2188`、`6772b38` |
| 独立验收记录 | [`remediation-evidence.json`](../../plans/codebase-remediation-2026-06-21b/records/remediation-evidence.json) |
| 结论 | **10/10 findings verified；0 open；no-merge 与确定性不变量保持** |

复审基于实现后的独立门禁重跑，不改写原始评估事实。证据记录生成于巴黎本机偏移
`2026-06-21T14:03:35+02:00`，对应实现 HEAD `6772b38`。

## 验收总览

| 门禁 | 结果 |
|---|---|
| Round-B 定向回归 | 22 passed |
| 全量 pytest | 119 passed |
| 覆盖率合约 | 总 `95.29%`；`patchgate.py` `100%`；CLI `94.32%` |
| Ruff lint / format | 通过；125 files formatted |
| Mypy | 通过；93 source files |
| `pip check` | 无损坏依赖 |
| sdist / wheel build | 通过 |
| 隔离 wheel smoke | 通过；三个 scheme 可自动发现，CLI theory-list 可运行 |

## Finding 逐项复审

### QE-2026-101 — verified

- 修复提交：`7b798a70153aca3e0fe531e8ba756ec2ac7a233b`
- 实现：挑战建议进入接收方 `consider`，接收方仅以自身 objective 复核并决定是否更新
  自身冠军；`ConsiderationCard` 与 ledger 保留 before/after/delta/reason 证据。
- 独立证据：改进建议被采纳、劣化建议被拒、fresh-engine 结果确定；duel 全程
  `allow_merge=False`，不存在 merged theory。
- 回归：`test_suggestion_adopted_when_self_verified_improvement`、
  `test_suggestion_rejected_when_no_self_verified_improvement`、
  `test_duel_records_independent_considerations`。
- 剩余风险：当前建议优化预算仍是启发式，但不会绕过接收方自身判定。

### QE-2026-102 — verified

- 修复提交：`7b798a70153aca3e0fe531e8ba756ec2ac7a233b`
- 实现：efficiency 来自引擎 `compute_cost`，simplicity 来自实际 `free_parameters`，
  不再由 theory YAML 自报值进入硬评分。
- 独立证据：篡改自报 efficiency 为 `0.01/0.99` 均不改变分数；minimal-axiom 的实测
  efficiency/simplicity 均高于完整 analytic pipeline。
- 回归：`test_efficiency_is_engine_derived_not_self_declared`、
  `test_efficiency_differs_across_paradigms`、`test_simplicity_reflects_real_free_parameters`。
- 剩余风险：display 权重仍是产品启发式，已与物理事实明确分层。

### QE-2026-103 — verified

- 修复提交：`d16336fdb1fc0be1b9ea1632a08c2983c78017e6`
- 实现：每个 logistic/falling 窗口具有 `CalibrationThreshold` 名义值、区间、单位、类型
  与依据；`threshold_sensitivity()` 逐项在区间两端重算。
- 独立证据：标准分数 analytic `0.9997237`、variational `0.8614355`、minimal
  `0.9232608`，均在登记锚点内。最大单阈值变化：variational `0.03635`
  （nuclear low），minimal `0.03035`（seed high）；analytic 标准点在其恒星寿命区间
  内变化为 `0`，说明锚点远离该硬边界。
- 回归：`test_standard_universe_within_calibrated_ranges`。
- 剩余风险：这是 toy/analytic 模型不确定性包络，不是论文级似然或实验误差；边界已在
  [`PHYSICS_CALIBRATION.md`](../design/PHYSICS_CALIBRATION.md) 明示。

### QE-2026-104 — verified

- 修复提交：`e1a218807122d758b94ac606d6df7dbe1db0d70b`
- 实现：线程安全、LRU 有界 assess 缓存，键为
  `(theory_id, version, rounded-vector)`，缓存值深拷贝隔离调用方修改。
- 独立证据：同版本且仅有 `1e-13` 浮点噪声的第二次评估不再构建 engine（调用数保持
  `1`）；版本 bump 后调用数升至 `2`。一次完整评分实测 `17 misses / 4 hits`，重复
  评分复用全部既有键。
- 回归：`test_assess_memoized_and_deterministic`。
- 剩余风险：理论物理语义变更必须同时 bump version；该规则已成为缓存契约。

### QE-2026-105 — verified

- 修复提交：`e1a218807122d758b94ac606d6df7dbe1db0d70b`
- 实现：`NoveltyArchive` 具有容量、按 generation 的确定性过期与圆整特征去重；不使用
  wall-clock。
- 独立证据：30 代压力回归中 archive 从未超过容量 8；3 代年龄窗口下最终仅 4 项；
  重复 feature 只刷新不增长；末 10 代 novelty 全部大于 0。
- 回归：`test_novelty_archive_bounded_no_collapse`。
- 剩余风险：capacity/max-age 是运行参数，超大特征维度仍需调用方控制。

### QE-2026-106 — verified

- 修复提交：`e1a218807122d758b94ac606d6df7dbe1db0d70b`
- 实现：内置 scheme 子包通过 `pkgutil` 自动发现，外部插件通过
  `quanta_engine.schemes` entry point；PatchGate 冲突映射抽为可注入 `ConflictStrategy`。
- 独立证据：测试临时放入 `drop_in_test` 子包，无中心文件编辑即可 build；自定义策略可
  把通常会 patch 的裁决改为 unchanged，同时默认策略的现有 patch/fork/no-merge 测试全绿。
- 回归：`test_new_scheme_discovered_without_central_edit`、
  `test_patchgate_uses_injected_conflict_strategy`。
- 剩余风险：恶意或损坏的第三方 entry point 会在发现阶段显式失败，而不是静默跳过。

### QE-2026-107 — verified

- 修复提交：`6772b3851f4a8d0adcc867d18fbd43b0f9758342`
- 实现：`quantaengine_lattice` 定位为 frozen legacy archive；`quantaengine` compatibility
  namespace 在 1.0.0 且不早于 2027-06-21 移除，含 Python/CLI migration。
- 独立证据：文档回归检查 frozen、namespace、1.0 removal 与 migration 字段；现有兼容
  namespace 仍发出 `DeprecationWarning`。
- 回归：`test_deprecation_schedule_documented`。
- 剩余风险：1.0 前仍需在每个发布说明重复迁移通知。

### QE-2026-108 — verified

- 修复提交：`e1a218807122d758b94ac606d6df7dbe1db0d70b`
- 实现：EvolutionReport 记录 Pareto 稳定、family 稳定、最大分数增量与停止原因；早停
  必须显式开启。
- 独立证据：稳定场景请求 10 代、实际 2 代后以
  `stable_pareto_scores_and_families` 停止；同容差但 `early_stopping=False` 时完整执行 3 代。
- 回归：`test_evolution_early_stops_on_stable_ecosystem`、
  `test_evolution_early_stopping_is_opt_in`。
- 剩余风险：容差过宽会提前停止；报告保留全部指标供审计。

### QE-2026-109 — verified

- 修复提交：`6772b3851f4a8d0adcc867d18fbd43b0f9758342`
- 实现与证据：历史 GenesisArena v2 计划首屏含 `SUPERSEDED / 已取代` 横幅，链接
  `docs/design/REPO_STRUCTURE.md` 并禁止继续按旧 `genesis_arena` 结构扩展。
- 回归：文档首屏人工/路径检查。
- 剩余风险：历史正文为可追溯性保留，读者必须遵循横幅指向的权威规范。

### QE-2026-110 — verified

- 修复提交：`d16336fdb1fc0be1b9ea1632a08c2983c78017e6`
- 实现：Hypothesis 属性测试覆盖单位往返、平直密度预算、引力—恒星寿命单调性、
  电磁—氢结合/Bohr 半径单调性与标准锚点。
- 独立证据：40 组单位样本、各 30 组守恒/单调样本全绿；标准氢结合
  `13.5–13.7 eV`、Bohr 半径 `5.2–5.4e-11 m`、宇宙年龄 `13.0–14.5 Gyr`。
- 回归：`tests/test_physics_invariants.py`。
- 剩余风险：属性测试验证模型内部不变量，不替代真实观测校准。

## 最终结论

评估 B 的 3 个 P1、4 个 P2、3 个 P3 finding 均已实现并通过独立回归。原始基线
`2ab9917` 保持不变；修复轨迹、数值敏感性、门禁输出和 wheel 安装证据均可复算。
`allow_merge=False`、接收方自身 objective 独立判定、稳定 seed、巴黎本机时区记录等全局
不变量未被破坏。评估状态可从 `open` 提升为 **verified**。
