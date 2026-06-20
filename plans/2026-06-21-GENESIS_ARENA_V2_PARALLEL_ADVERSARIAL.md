# GenesisArena v2 — 并行多理论对抗式创世平台（改进版实现方案）

文件名：`2026-06-21-GENESIS_ARENA_V2_PARALLEL_ADVERSARIAL.md`
版本：v2.0（取代并吸收 `2026-06-21-ADVERSARIAL_SELF_PLAY_IMPLEMENTATION.md` v1.1）
适用项目：QuantaEngine
一句话：让**多个**从基本物理生成宇宙的方案作为独立谱系**并行存在、互相挑战、独立裁决、局部修正或分叉、长期进化**，而**不合并成单一赢家**。

---

## 0. 与 v1.1 的关系：吸收什么、改进什么

### 吸收（v1.1 的优点，全部保留）
1. **并行多理论谱系，不强制合并**（no-merge）——核心哲学。
2. **结构化对抗管线**：Challenge → Defense → 独立 Verifier → Judge → PatchGate。
3. **TheorySpec 文件化身份**：philosophy / axioms / physics_engine / claims / defense_prior / lineage_policy。
4. **多目标评分 + Pareto front + family niche + novelty archive**，不靠单一总分淘汰。
5. **独立确定性 Verifier**：复现硬错误、跑 benchmark，不做哲学判断。
6. **Patch vs Fork vs 不改**：硬 bug→patch，哲学变化→fork，纯偏好→不改。
7. **可辨识命名**：`T-XXXX` + family + 语义化版本 + parent_id 谱系。

### 改进（v1.1 的不足）
1. **过度工程**：v1.1 列出 40+ 文件，大多是空壳，难以一次落地、易腐烂。
   → v2 **收敛到 ~12 个聚焦模块**，每个都真实可运行、有测试，宁可少而全可跑。
2. **缺第三个真正不同的物理范式**：v1.1 的 T-0001/T-0002 在引擎层其实共享同一 pipeline，差别主要在配置/措辞。
   → v2 提供**三个范式上真正不同的引擎**（见 §3），让"多个方案"名副其实。
3. **"共识宇宙"反模式**：上一版 `cosmogenesis.Arena` 产出单一 consensus，与 no-merge 哲学冲突。
   → v2 **取消单一 consensus**，产出 **Pareto front + 每族冠军 + novelty archive** 的"理论生态快照"。
4. **并行只停留在伪代码**：v1.1 写了 `run_all_theories_parallel` 但无实现。
   → v2 用 `concurrent.futures` **真正并行**执行各理论的优化与对决（numpy 重计算释放 GIL；Windows 安全）。
5. **LLM Agent 的不确定性风险**：v1.1 把它列为 Phase 10。
   → v2 **只实现规则型确定性 Agent**，LLM 留作后续可选接口（schema 校验门槛保留）。

---

## 1. 命名方案（可辨识）

| 维度 | 命名规则 | 示例 |
|---|---|---|
| 平台 | GenesisArena | 包 `src/genesis_arena/` |
| 理论身份 | `T-NNNN` | `T-0001` |
| 理论族 | `family` 蛇形名 | `conservative_eft` |
| 版本 | 语义化 `vMAJOR.MINOR.PATCH` | `v0.1.0`→`v0.1.1`(patch)→`v0.2.0`(fork/大改) |
| 谱系 | `parent_id` 链 | `T-0006.parent_id = T-0001` |
| 物理引擎 | 形容词+机制 | `AnalyticCompiler` / `VariationalRelaxer` / `MinimalAxiomDimensional` |

理论生态（初始三族，可扩展）：
```
T-0001 conservative_eft      引擎 AnalyticCompiler        保守、贴近标准宇宙、白盒
T-0002 exploratory_generative 引擎 VariationalRelaxer      自洽残差、软窗口、探索多样宇宙
T-0003 minimal_axiom          引擎 MinimalAxiomDimensional 最少公理/最少参数、纯量纲分析+人择不等式
```

---

## 2. 分层架构（精简自 v1.1 的 8 层）

```
L0 物理基座   quanta_engine（既有有效物理 pipeline）
L1 范式引擎   cosmogenesis：三个不同范式的 Engine，统一 assess(vector)->UniverseAssessment
L2 理论身份   genesis_arena.theory：TheorySpec / 注册表 / 谱系 / 版本
L3 评分       genesis_arena.scoring：TheoryScoreVector(8 目标+penalty) / Pareto / niche / novelty
L4 对抗       genesis_arena.agents：规则型 attack/defend → Challenge/Defense 卡
L5 裁决       genesis_arena.verifier(确定性) + judge：复现+benchmark → JudgeResult
L6 谱系门     genesis_arena.patchgate：patch / fork / 不改 / 失效，永不 merge，写 history
L7 编排       genesis_arena.duel / tournament / evolution：并行多理论迭代
```

---

## 3. 三个真正不同的物理范式（L1）

所有引擎吃同一 `ParameterVector`（α/引力/强/Λ/扰动幅度），返回同一 `UniverseAssessment`（score, feasible, margins, residual, diagnostics）。

1. **AnalyticCompiler（保守）**：包装 `quanta_engine` 前馈闭式 pipeline，硬窗口布尔，目标 = civilization_potential_score。白盒、可解释。优化器=灵敏度坐标爬山。
2. **VariationalRelaxer（探索）**：把宇宙当耦合约束的**不动点**，软 logistic 窗口 + **跨层自洽残差** + 不动点松弛；能判"每窗口都过但整体不自洽"。优化器=进化策略。
3. **MinimalAxiomDimensional（极简，新增）**：只从**最少量纲量**出发——精细结构常数 α、引力耦合 α_G=G m_p²/(ħc)、电子/质子质量比——用 Carr–Rees 型**人择不等式**直接判定可行性，自由参数与公理最少。既不分层（异于 1），也不做不动点（异于 2）。

> 三者在**机制**上不同（前馈/不动点/量纲不等式），因此对同一宇宙会给出**不同排序**——这正是对抗压力的来源。

---

## 4. 多目标评分与不坍缩选择（L3）

`TheoryScoreVector`（沿用 v1.1 §14，落地实现）：
`validity, physical_consistency, benchmark_fit, generative_power, robustness, novelty, simplicity, computational_efficiency, unresolved_challenge_penalty`。

- `display_score`：加权和，仅用于展示。
- **选择**：`pareto_front()` + `family_elites(K)` + `novelty_archive`。**绝不**按单一总分淘汰。
- 反坍缩：每代至少保留 `min_families` 个族；冠军不得替换整个种群；fork 不删父理论。

---

## 5. 对抗管线（L4–L6）

单轮 Duel（A,B）：
```
1. 并行 run engine(A), engine(B) → UniverseAssessment
2. B.agent.attack(A) → [ChallengeCard];  A.agent.defend(challenges) → [DefenseCard]
3. Verifier.reproduce(challenge, A) → VerificationResult（确定性：复现失败模式+跑 benchmark）
4. Judge.decide(challenge, defense, verification) → JudgeResult
5. PatchGate.process(A, judge_results) → A 不变 / A patch 到新版本 / fork 出 A' / A 失效（永不 merge）
6. 反向 A 攻 B，重复
7. 记录 DuelReport + 各自 history.jsonl
```

Judge 规则（确定性）：无对象→reject；无证据但可测→needs_more_tests；不可复现→reject；复现硬错误→patch_required；软问题→upheld_no_patch / fork_recommended；改哲学→fork_recommended；理论不可运行→invalidated。

PatchGate 规则：CRITICAL 硬错误必 patch 或失效；MAJOR 可 patch 或 fork；软问题不强制；patch 必须最小且过 regression；改哲学→fork 保父；**allow_merge 恒 False**。

---

## 6. 并行进化（L7）

```
evolve(population, generations):
  每代：
    1. ThreadPool 并行：各理论独立优化其参数（各自引擎+优化器）
    2. ThreadPool 并行：Swiss/round-robin 配对跑 Duel
    3. 收集 patch/fork（保父）
    4. 重新评分 → Pareto front + family_elites + novelty_archive
    5. 反坍缩选择下一代（min_families、冠军不独占）
  产出 EvolutionReport（生态快照，非单一赢家）
```

---

## 7. 代码结构（精简版，~12 模块）

```
src/cosmogenesis/                  # L1 范式引擎库（既有，新增 scheme_c）
  parameters.py / assessment.py
  scheme_a.py (AnalyticCompiler) / scheme_b.py (VariationalRelaxer) / scheme_c.py (MinimalAxiom, 新增)

src/genesis_arena/                 # L2–L7 平台（新增）
  __init__.py
  cards.py        枚举 + Challenge/Defense/Evidence/Judge/Patch 的 Pydantic 模型
  theory.py       TheorySpec / Philosophy / DefensePrior / LineagePolicy / 加载 / 注册表
  engines.py      引擎注册：name -> Engine(assess/optimize)；novelty 特征提取
  scoring.py      TheoryScoreVector / display_score / pareto / family_elites / novelty
  verifier.py     确定性 Verifier：benchmark suite + 硬约束复现
  agents.py       规则型 per-family attack/defend
  judge.py        Judge 决策
  patchgate.py    patch/fork/no-merge + history.jsonl
  duel.py         单场对决（含并行 run）
  tournament.py   round-robin + 评分
  evolution.py    并行多代演化（ThreadPool）+ 反坍缩选择
  cli.py / __main__.py   genesis-arena theory/duel/tournament/evolve

theories/                          # 文件化理论身份
  T-0001_conservative_eft/theory.yaml
  T-0002_exploratory_generative/theory.yaml
  T-0003_minimal_axiom/theory.yaml
  registry.yaml

tests/test_genesis_arena.py        # schema/verifier/judge/patchgate(no-merge)/pareto/duel/tournament/evolution/e2e
```

---

## 8. 成功标准（对齐 v1.1 §26，可机检）

1. ≥3 个范式不同的理论并行存在且可单独运行。
2. 理论间产生**可复现**的结构化 challenge，Verifier 能复现/驳回。
3. 防守默认成立，软偏好被驳回，硬错误被 patch。
4. **no-merge** 全程成立（断言 `allow_merge is False`，无 merged_theory_id）。
5. 改哲学时 **fork** 而非覆盖，父理论保留。
6. 选择产出 **Pareto front + 每族冠军 + novelty archive**，非单一赢家。
7. 演化**并行**执行，多代后仍 ≥ min_families 个族。
8. 全流程有 report/json + history.jsonl，测试全绿。

---

## 9. 落地顺序（一次性交付，不分 10 期）

1. `cosmogenesis/scheme_c.py`（第三范式）+ 单测。
2. `genesis_arena/cards.py` + `theory.py` + `theories/*.yaml`。
3. `engines.py` + `scoring.py`（Pareto/niche/novelty）。
4. `verifier.py` + `agents.py` + `judge.py` + `patchgate.py`。
5. `duel.py` + `tournament.py` + `evolution.py`（并行）+ `cli.py`。
6. `tests/test_genesis_arena.py` 全绿 + 端到端跑 `evolve` 产出报告。
7. 更新 README，提交并上传。
```
