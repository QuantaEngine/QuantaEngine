# QuantaEngine 代码库评估报告（独立·第二轮）

## 1. 评估元数据

| 字段 | 值 |
|---|---|
| Review ID | `QE-REVIEW-2026-06-21B` |
| 评估日期 | 2026-06-21 |
| 基线提交 | `2ab9917708b2ba1574301d48196743c4771a2282` |
| 分支 | `main` |
| 评估性质 | **独立评估**：先基于审查者对当前代码的精读独立得出问题，再与既有评估交叉标注关系 |
| 评估范围 | `cosmogenesis`（core / schemes / arena）、评分与对抗回路、优化与演化、持久化、文档与依赖 |
| 评估方式 | 静态精读 + 行级证据；动态门禁实测（pytest / coverage / ruff / mypy / build / CLI smoke） |
| 代码修改 | 无；本报告仅记录评估结果 |
| 与前轮关系 | 前轮 `QE-REVIEW-2026-06-21`（基线 `6050e48`）8 项**工程** finding 已全部 `verified`；本轮聚焦其之上**更深一层**的对抗回路、评分可信度与科学校准 |
| 总体结论 | 工程基线健康（门禁全绿、覆盖率 95%+），但**对抗回路与多目标评分的可信度**尚不足以支撑"多方案对抗演化"结论可被信赖，物理模型仍未校准 |

## 2. 摘要

经独立精读，仓库的工程质量在前一轮修复后确实达标：97 项测试通过，Ruff/Mypy/格式与覆盖率门禁全绿，复现性与并发问题已闭环。

但站在"**从基本物理出发、让多个方案对抗式迭代优化生成宇宙**"这一项目主张上，当前仍有三处核心短板，且均**非前轮覆盖**：

1. **对抗只影响"选择分数"，从不进入对方的优化器**——各方案独立最大化自身目标，挑战/裁决只在评分上加惩罚或偶发 fork，缺少用户期望的"**接收方独立复核建议、自证正确后才采纳**"回路（`QE-2026-101`）。
2. **多个评分目标可被"声明"而非测量**——`computational_efficiency` 直接取自理论自报常数、`simplicity` 近似二值、`display_score` 权重为手设魔数；8 维 Pareto 因此被稀释，"不合并"退化为"几乎都存活"（`QE-2026-102`）。
3. **物理阈值与权重全手设、无外部校准与不确定性**——决定"宇宙生成"结论的可信度（`QE-2026-103`）。

其余为性能（assess 无缓存）、扩展（硬编码方案注册）、维护（lattice/旧 namespace）、文档与测试深度等支撑性问题。

## 3. 验证基线（本轮实测）

| 检查 | 结果 | 说明 |
|---|---|---|
| `python -m pytest` | 通过 | `97 passed` |
| 覆盖率合约 | 通过 | 总 95.41%（门槛 90%）；`patchgate` 100%；`cosmogenesis.cli` 94.32% |
| `ruff check src tests` | 通过 | 无 lint 错误 |
| `ruff format --check` | 通过 | 113 个文件已格式化 |
| `mypy src` | 通过 | 93 个源文件无问题 |
| `python -m cosmogenesis theory-list / score` | 通过 | 三理论可列出/评分 |
| 工作区 | 干净 | `main`，HEAD `2ab9917` |

> 结论：本轮 finding **均非回归或门禁失败**，而是前瞻性的设计、可信度与科学性问题。工程门禁已不足以暴露它们——这正是需要独立评估的原因。

## 4. Findings 总表

| ID | 严重度 | 状态 | 问题 | 主要影响 | 与前轮关系 |
|---|---|---|---|---|---|
| `QE-2026-101` | P1 | open | 对抗建议不进入对方优化器，缺"独立复核后采纳"回路 | 对抗未真正驱动各方案迭代优化 | 全新 |
| `QE-2026-102` | P1 | open | 多个评分目标可自报/近似二值/权重手设 | Pareto 选择被稀释，结论不可信 | 全新 |
| `QE-2026-103` | P1 | open | 物理阈值/权重无外部校准与不确定性 | "宇宙生成"可信度受限 | 参考 remediation §6/§7.1 |
| `QE-2026-104` | P2 | open | `bridge.assess` 无记忆化，单理论单代重算 20+ 次 | 随方案×代二次增长 | 全新（量化） |
| `QE-2026-105` | P2 | open | novelty archive 无界无衰减 | 后代 novelty 系统性下降 + 成本随代增长 | 全新 |
| `QE-2026-106` | P2 | open | 方案注册硬编码 dict；reducer 无冲突策略对象 | 新增方案需改中心文件 | 参考 remediation §7.2 |
| `QE-2026-107` | P2 | open | lattice/旧 namespace 无定位与移除时间表 | 长期并行维护负担 | 参考 remediation §6/§7.3 |
| `QE-2026-108` | P3 | open | `evolve` 固定代数，无收敛/早停 | 长期迭代缺自然节奏 | 全新 |
| `QE-2026-109` | P3 | open | v2 计划文档仍描述已废弃 `genesis_arena` 结构 | 文档误导 | 全新 |
| `QE-2026-110` | P3 | open | 缺物理不变量属性化测试 | 物理可信度无回归锚 | 全新 |

## 5. 详细问题

### QE-2026-101：对抗建议未进入优化，缺"独立复核后采纳"回路

**严重度：P1　状态：open　类别：adversarial-core**

相关代码：

- [`arena/evolution.py`](../../src/cosmogenesis/arena/evolution.py#L41-L44) `_optimize_one` 仅用理论自身 `bridge.optimize`。
- [`arena/scoring.py`](../../src/cosmogenesis/arena/scoring.py#L124-L150) `adversarial_outcome` 把裁决汇成 `unresolved_challenge_penalty`，只影响**评分/选择**。
- [`arena/agents.py`](../../src/cosmogenesis/arena/agents.py#L47-L60) 挑战由 philosophy 阈值触发，挑战卡带 `probe_vector`，但其建议**从未回到对方优化器**。

当前对抗的全部作用是：触发 patch/fork、或在 display score 上扣分。各方案的**优化轨迹相互独立**，对方的建议（"我认为你在这个方向更鲁棒/更自洽"）没有任何机制让接收方去**独立评估并选择性采纳**。

这与用户明确的设计意图不符：

> 每个方案保持独立；对抗的产出是给对方的**建议**；接收方不是盲目听众，要用自己的标准**谨慎独立复核**，**只有自己独立确认正确才采纳进优化**，否则拒绝。**绝不合并。**

建议修复（详见修复方案包）：在 `UniverseScheme`/`BaseEngine` 增加 `consider(suggestion)`——接收方在**自身 objective** 下独立评估攻击方给出的 `suggestion`（具体参数向量），仅当独立确认能改进自身目标时采纳为 warm-start，否则拒绝并记录理由。可复用已退役 `cosmogenesis/scheme_a.py::consider()`（git 历史）"再优化后只在自身目标不退化时接受"的模式，但去掉共识/合并语义。

验收标准：

- 当建议在接收方自身模型下确能改进目标时，被采纳并改变其后续优化结果。
- 当建议无改进时被拒绝，history 记录 `adopted=false` 与独立验证理由。
- 全过程无合并：两方案冠军始终各自独立判定。

### QE-2026-102：多个评分目标可被"声明"而非测量

**严重度：P1　状态：open　类别：scoring-integrity**

相关代码：[`arena/scoring.py`](../../src/cosmogenesis/arena/scoring.py#L43-L55)、[L88-L93](../../src/cosmogenesis/arena/scoring.py#L88-L93)、[L117](../../src/cosmogenesis/arena/scoring.py#L117)。

- `computational_efficiency` 直接取自 `theory.philosophy.computational_efficiency`——一个写在 theory.yaml 里的**自报常数**，可被理论单方面声明为高，未做任何实测（如计时/调用次数）。
- `simplicity` 仅由 `free_parameters` 决定，而该字段只有 `minimal_axiom` 设为 3，其余 scheme 回退为参数维数 5，导致该目标近似**二值**，并不反映真实公理/假设数量。
- `display_score` 的 8 个权重（0.20/0.15/...）为**手设魔数**，无依据、无敏感性分析。

后果：`pareto_dominates` 在 8 个目标上比较，其中含可自报、近似二值的弱目标，使非支配集被稀释——一个理论只要在自报的 `computational_efficiency` 上最高即可进入 Pareto front，"永不合并/保留多样性"在实践中退化为"几乎所有理论都存活"，selection 失去区分力。

建议修复：把"目标"区分为**可测量**（运行实测 efficiency、按假设/参数真实计数的 simplicity）与**声明先验**（明确标注且不进入硬 Pareto，仅作展示或权重）；对 `display_score` 权重给出依据或做敏感性报告；考虑对弱目标设最小区分阈值或从 Pareto 维度中剔除。

验收标准：efficiency 来自实测且不同 scheme 有可区分值；simplicity 反映真实假设数；移除可自报目标后 Pareto front 规模显著收敛且能解释。

### QE-2026-103：物理阈值与权重无外部校准与不确定性

**严重度：P1　状态：open　类别：scientific-validity**

相关代码：`schemes/analytic_compiler/engine.py`、`schemes/variational_relaxer/engine.py`、`schemes/minimal_axiom/engine.py` 中 10+ 处 logistic 窗口 `lo/hi/threshold`（如 binding `lo=1.0,hi=120.0`、nuclear `lo=0.8,hi=1.45`、stellar `lo=1e9,hi=1e13` 等）。

这些窗口边界与评分权重全部手工设定，无引用来源、无不确定性传播、无敏感性分析。对一个以"从基本物理生成宇宙"为主张的项目，结论可信度直接受限于这些未经校准的阈值。

前轮 remediation §6/§7.1 已把"物理仍是 toy/analytic、未做论文级校准"列为遗留边界；本轮独立确认其影响并定级为 **P1**——因为它决定项目核心主张的可信度，而非仅是工程细节。

建议修复：建立校准基准集（标准宇宙数值锚点 + 文献区间），对窗口阈值/权重做敏感性与不确定性报告，并在报告与文档中明确"物理事实"与"启发式权重"的边界。

验收标准：每个关键阈值给出来源/区间；对阈值扰动给出分数敏感性；标准宇宙锚点在文献区间内。

### QE-2026-104：assess 无记忆化导致重复求值

**严重度：P2　状态：open　类别：performance**

相关代码：[`arena/bridge.py`](../../src/cosmogenesis/arena/bridge.py#L18-L26) 仅对 `_load(config)` 做 `lru_cache`；`assess(theory, vector)` 未缓存。[`arena/scoring.py`](../../src/cosmogenesis/arena/scoring.py#L58-L93)。

单个理论单代 `score_theory` 即触发 `bridge.assess` 20+ 次：benchmark 1 次、generative_power 6 次、robustness 经 `fragility_profile` 约 10 次、simplicity 2 次；tournament 再叠加每对 duel 的评估。随方案数与代数二次增长。

建议修复：对 `assess` 按 `(theory_id, version, vector)` 做记忆化（或在一代内复用 duel 已算结果）；`fragility_profile` 可批量/向量化。

验收标准：相同输入下 assess 调用次数显著下降；演化耗时随规模近线性；结果与未缓存一致（确定性不变）。

### QE-2026-105：novelty archive 无界无衰减

**严重度：P2　状态：open　类别：scaling**

相关代码：[`arena/evolution.py`](../../src/cosmogenesis/arena/evolution.py#L176-L180) 每代对每个理论 `novelty_archive.append(...)`；[`arena/scoring.py`](../../src/cosmogenesis/arena/scoring.py#L186-L195) `novelty_score` 对全 archive 求最近邻。

archive 单调增长、无 dedup/decay/cap，导致两个问题：随代数增加 novelty 普遍下降（空间被填满），且每次 novelty 计算成本随 archive 线性增长。长期演化下 novelty 目标逐渐失效。

建议修复：archive 加容量上限或时间衰减；按特征去重；明确"当代 novelty"与"跨代 novelty"语义并分别归一化。

验收标准：长跑下 novelty 不单调塌缩；archive 大小有界；novelty 计算成本可控。

### QE-2026-106：方案注册硬编码，reducer 无冲突策略对象

**严重度：P2　状态：open　类别：extensibility**

相关代码：[`schemes/__init__.py`](../../src/cosmogenesis/schemes/__init__.py#L20-L40) `SCHEME_REGISTRY` 为硬编码 dict，新增方案须修改此中心文件；patch 合并无显式冲突策略对象（前轮 remediation §7.2 已提及）。

建议修复：改为子包自动发现或 entry-point 插件式注册；抽出 reducer 冲突策略对象以支持未来更多 patch 类型。验收：放入一个新 scheme 子包即被发现并参与对抗，无需改注册中心。

### QE-2026-107：历史原型与旧 namespace 的维护负担

**严重度：P2　状态：open　类别：maintenance**

`quantaengine_lattice`（~900 LOC）与主线无功能耦合，纯历史原型并行维护；兼容 namespace `quantaengine` 在 0.x 长期保留但无使用统计与 1.0 移除时间表（前轮 §6/§7.3）。

建议修复：明确 lattice 定位（冻结/归档/独立包）；统计旧 namespace 使用并制定 1.0 移除计划与迁移说明。

### QE-2026-108：演化缺收敛/早停判据

**严重度：P3　状态：open　类别：loop-control**

[`arena/evolution.py`](../../src/cosmogenesis/arena/evolution.py#L150) 固定 `generations` 循环，无生态稳定检测、早停或自适应节奏，与"不断迭代对抗优化"的长期目标不匹配。

建议修复：增加收敛指标（如 Pareto front 稳定、分数增量阈值、family 组成稳定）与可选早停。

### QE-2026-109：v2 计划文档结构漂移

**严重度：P3　状态：open　类别：docs-drift**

[`plans/2026-06-21-GENESIS_ARENA_V2_PARALLEL_ADVERSARIAL.md`](../../plans/2026-06-21-GENESIS_ARENA_V2_PARALLEL_ADVERSARIAL.md) 仍按已废弃的 `src/genesis_arena/` 描述目录，与现 `cosmogenesis/{core,schemes,arena}` 不符。

建议修复：加"已被 `docs/design/REPO_STRUCTURE.md` 取代"横幅，或归档为历史快照。

### QE-2026-110：缺物理不变量属性化测试

**严重度：P3　状态：open　类别：test-depth**

现有测试以行为/确定性为主，缺少守恒、量纲、单调性、标准宇宙数值锚点等**物理不变量**的属性化测试；`hypothesis` 已是依赖却未用于物理性质。

建议修复：用 property-based 测试锚定物理不变量（如重力增大→恒星寿命单调下降、标准宇宙在锚点区间内），作为物理可信度的回归基线。

## 6. 优化路线

### Phase A：可信的对抗回路（最高优先）

目标 finding：`QE-2026-101`、`QE-2026-102`。

1. 实现"独立考虑建议"回路：接收方在自身 objective 下独立复核 `suggestion`，自证改进才采纳，history 记录采纳/拒绝与理由；绝不合并。
2. 评分目标去"自报化"：efficiency 实测、simplicity 真实计数、弱目标退出硬 Pareto；display 权重给依据或敏感性。
3. 一致性/确定性测试：采纳建议前后由各自模型独立判定；移除可自报目标后 Pareto 收敛可解释。

### Phase B：科学可信度

目标 finding：`QE-2026-103`、`QE-2026-110`。

1. 物理阈值校准基准集 + 敏感性/不确定性报告。
2. 物理不变量属性化测试。

### Phase C：性能与可扩展

目标 finding：`QE-2026-104`、`QE-2026-105`、`QE-2026-106`、`QE-2026-108`。

1. assess 记忆化/批处理；novelty archive 衰减与上限。
2. 插件式方案注册 + reducer 冲突策略对象；演化收敛判据。

### Phase D：维护与文档

目标 finding：`QE-2026-107`、`QE-2026-109`。

1. lattice/旧 namespace 退役时间表。
2. v2 计划文档归档/加横幅。

## 7. 正向评价（独立确认）

- 工程基线确实健康：97 测试、95%+ 覆盖、Ruff/Mypy/格式/build/CLI 全绿，前轮修复经独立复跑成立。
- `core / schemes / arena` 边界清晰，新增 scheme 的扩展点明确（虽注册仍需手动）。
- 复现性元数据（run_id/seed/commit/fingerprint）与持久化历史链路完善，利于回溯。
- 三种 scheme 计算路径确实不同，非简单换权重。

## 8. 评估限制

- 未做物理模型的论文级外部数值校准（属本轮 finding `QE-2026-103` 范畴）。
- 未运行长时多代/多进程压力与故障注入。
- 未审查 GitHub 权限、分支保护与发布签名。
- 复现实验针对核心代码路径，未修改仓库源码。

## 9. 后续复审模板

每个 finding 修复后记录：

```text
Finding ID:
修复提交:
状态: fixed / verified / accepted-risk
实现摘要:
独立验证证据（接收方自身模型判定/实测数值/对比）:
新增回归测试:
CI URL:
剩余风险:
```

复审应创建新报告并链接本文件，保留 `2ab9917` 基线事实不变。配套修复方案包见
[`plans/codebase-remediation-2026-06-21b/`](../../plans/codebase-remediation-2026-06-21b/README.md)。
