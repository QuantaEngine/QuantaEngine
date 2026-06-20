# QuantaEngine 对抗式科学自博弈系统最佳实现方案

文件名：`ADVERSARIAL_SELF_PLAY_IMPLEMENTATION.md`  
版本：v1.1  
适用项目：QuantaEngine / GenesisEngine  
核心目标：让两个或多个“从基本物理理论生成宇宙”的方案并行对抗、并行防守、并行修正、并行进化，而不是最终合并成一个统一方案。

---

## 0. 核心结论

本系统不应设计成：

```text
多个方案互相辩论
→ 选出一个最终赢家
→ 合并成一个统一方案
```

而应设计成：

```text
多个 TheorySpec 并行存在
→ 互相挑战
→ 各自防守
→ 独立验证器裁决
→ 只有目标理论自身出现不可避免错误时才局部修正
→ 方案保留独立谱系
→ 形成多个长期并存的理论族群
```

最终结果应是一个“并行理论生态系统”：

```text
Conservative-EFT Lineage
  保守、可验证、贴近标准宇宙、低风险。

Exploratory-Generative Lineage
  更强调生成丰富宇宙、参数扫描、多样性。

Minimal-Axiom Lineage
  更强调少公理、少参数、从更少假设推出更多结构。

Computational-Efficient Lineage
  更强调快速计算、大规模扫描和工程可用性。

High-Fidelity Lineage
  更强调高精度物理模块和外部专业工具接入。
```

这些理论族群可以互相挑战、互相借鉴、局部吸收测试，但不强制合并。

一句话定义：

```text
QuantaEngine Adversarial Self-Play 是一个并行多理论谱系优化系统：
每个宇宙生成理论作为独立个体保留自身哲学、假设、代码路径和版本谱系；
对抗只负责发现问题和提供进化压力，不负责把所有理论融合成一个最终答案。
```

---

## 1. 设计目标

### 1.1 科学目标

系统应支持：

```text
1. 从不同底层物理假设生成不同宇宙。
2. 比较不同宇宙生成理论的自洽性、生成能力、鲁棒性和解释力。
3. 让方案互相指出不可避免错误。
4. 让方案默认维护自身，不无条件接受对方建议。
5. 让独立验证器裁决硬错误。
6. 让每个理论独立迭代，不被强制合并。
7. 保留多个 Pareto-optimal 理论。
8. 支持标准宇宙复现，也支持非标准但自洽宇宙生成。
```

### 1.2 工程目标

系统应支持：

```text
1. TheorySpec 文件化。
2. Challenge/Defense/Judge/Patch 全部结构化。
3. 每次 duel 可复现。
4. 每次理论更新有 history.jsonl。
5. 每个理论有独立版本号。
6. 每个理论有独立配置、claim、假设和已知限制。
7. 可以运行 tournament。
8. 可以运行 population evolution。
9. 可以并行执行多个方案的 pipeline。
10. 可以生成 Markdown/JSON 报告。
```

### 1.3 关键非目标

明确不做：

```text
1. 不把所有方案融合成一个最终统一方案。
2. 不让 LLM 口头辩论直接决定物理正确性。
3. 不让批评自动变成补丁。
4. 不为了提高总分而牺牲理论独立性。
5. 不把 toy model 伪装成高精度物理。
6. 不用单一总分淘汰所有非主流理论。
```

---

## 2. 并行理论谱系原则

这是本方案相对普通 adversarial training 的最重要区别。

### 2.1 理论是长期并存的谱系

每个方案都是一个独立谱系：

```text
T-0001 Conservative-EFT
T-0002 Exploratory-Generative
T-0003 Minimal-Axiom
T-0004 Efficient-Scanner
T-0005 High-Fidelity-Hybrid
```

每个理论可以有自己的版本：

```text
T-0001 v0.1.0
T-0001 v0.1.1
T-0001 v0.2.0

T-0002 v0.1.0
T-0002 v0.1.1
T-0002 v0.2.0
```

但是：

```text
T-0001 和 T-0002 不会被强制合并成 T-final。
```

### 2.2 对抗只产生局部压力

当 B 成功指出 A 的错误时，只有 A 需要处理。

```text
B attacks A
Verifier confirms
Judge upholds challenge
PatchGate applies only to A or creates A'
B 不会被合并进 A
A 也不会被合并进 B
```

### 2.3 可以产生子理论，但父理论不消失

如果一个理论想吸收另一个理论的局部思想，不能覆盖原理论，只能创建新子理论：

```text
T-0001 Conservative-EFT
T-0002 Exploratory-Generative

可产生：
T-0006 Conservative-EFT-with-Exploratory-Scan

但：
T-0001 仍然存在
T-0002 仍然存在
T-0006 是独立新谱系或分支
```

### 2.4 保留 Pareto Front，而不是只保留第一名

一个理论可能在自洽性上最好，另一个在生成多样性上最好，另一个在计算速度上最好。

因此 selection 不能只按一个分数排序。

必须保留：

```text
- best validity theory
- best benchmark theory
- best generative theory
- best novelty theory
- best efficient theory
- best minimal-assumption theory
- best robust theory
```

### 2.5 防止理论坍缩

需要设置 anti-collapse 规则：

```text
1. 每个 generation 至少保留 N 个谱系。
2. 每个 theory family 至少保留 top K。
3. 不允许 tournament winner 替换整个 population。
4. 不允许 crossover 删除父理论。
5. 不允许 soft criticism 强制改变理论哲学。
6. 高 novelty 但 hard-valid 的理论进入 archive。
7. 保守理论和探索理论分开排名，同时进行 cross-duel。
```

---

## 3. 为什么不能做成普通 GAN

GAN 是生成器和判别器的 minimax 对抗：

```text
Generator 尝试生成更像真实数据的样本。
Discriminator 尝试判断真假。
最终 Generator 逼近数据分布。
```

你的项目不同：

```text
1. 不是只有一个真实数据分布。
2. 目标不是只逼近我们的宇宙。
3. 你想生成很多不同但自洽的宇宙。
4. 对抗者不是单一判别器，而是多个理论互相挑战。
5. 正确性不只来自统计相似，而来自物理自洽、可复现、有效理论边界和鲁棒性。
```

所以更准确的范式是：

```text
Parallel Adversarial Scientific Self-Play
```

也就是：

```text
多个科学理论并行存在；
通过互相挑战获得进化压力；
通过独立验证器裁决硬错误；
通过 Pareto 与 niche selection 保留多样理论。
```

---

## 4. 总体架构

### 4.1 系统分层

```text
Layer 1: Theory Layer
  定义每个宇宙生成理论的身份、哲学、假设、公理、模块、claim 和配置。

Layer 2: Execution Layer
  调用 QuantaEngine 原有 universe pipeline，生成 UniverseReport。

Layer 3: Adversarial Layer
  理论之间产生 ChallengeCard 和 DefenseCard。

Layer 4: Verification Layer
  独立运行测试、复现 challenge、检查物理硬约束。

Layer 5: Judge Layer
  根据证据、测试和防守结果判定 challenge 状态。

Layer 6: PatchGate Layer
  只对目标理论应用必要补丁，或者创建分叉理论。

Layer 7: Optimization Layer
  计算多目标指标、Pareto front、Elo、novelty、robustness。

Layer 8: Parallel Evolution Layer
  多理论族群并行迭代，不合并成单一赢家。
```

### 4.2 主流程

```text
Input:
  theories/T-0001/theory.yaml
  theories/T-0002/theory.yaml
  ...
  benchmark_suite.yaml

For each generation:
  1. 并行运行每个 TheorySpec 的 UniversePipeline。
  2. 为每对理论运行 Duel。
  3. 每个理论攻击其他理论。
  4. 每个理论防守自身。
  5. Verifier 验证 challenge。
  6. Judge 裁决 challenge。
  7. PatchGate 对目标理论局部修正或分叉。
  8. Scoring 计算多目标分。
  9. Selection 保留 Pareto front + niche elites。
  10. Archive 保存有效但非主流理论。
  11. 进入下一代。
```

---

## 5. 新增代码结构

在原项目中添加以下模块：

```text
src/quanta_engine/
├── adversarial/
│   ├── __init__.py
│   ├── roles.py
│   ├── agents.py
│   ├── challenge.py
│   ├── defense.py
│   ├── evidence.py
│   ├── protocol.py
│   ├── verifier_bridge.py
│   ├── judge.py
│   ├── patching.py
│   ├── debate_log.py
│   ├── duel.py
│   ├── tournament.py
│   └── scoring.py
│
├── theories/
│   ├── __init__.py
│   ├── theory_spec.py
│   ├── claims.py
│   ├── assumptions.py
│   ├── lineage.py
│   ├── registry.py
│   └── loader.py
│
├── optimization/
│   ├── __init__.py
│   ├── objectives.py
│   ├── pareto.py
│   ├── elo.py
│   ├── novelty.py
│   ├── population.py
│   ├── niches.py
│   └── selection.py
│
└── experiments/
    ├── duel.py
    ├── tournament.py
    ├── mutation.py
    ├── benchmark_suite.py
    └── parallel_evolution.py
```

项目根目录添加：

```text
theories/
├── T-0001_standard_eft/
│   ├── theory.yaml
│   ├── claims.yaml
│   ├── assumptions.md
│   ├── history.jsonl
│   └── configs/
│       └── standard_universe.yaml
│
├── T-0002_exploratory_generative/
│   ├── theory.yaml
│   ├── claims.yaml
│   ├── assumptions.md
│   ├── history.jsonl
│   └── configs/
│       └── exploratory_universe.yaml
│
├── T-0003_minimal_axiom/
│   ├── theory.yaml
│   ├── claims.yaml
│   ├── assumptions.md
│   ├── history.jsonl
│   └── configs/
│       └── minimal_axiom_universe.yaml
│
└── registry.yaml
```

报告目录：

```text
reports/
├── duels/
├── tournaments/
├── generations/
├── challenges/
├── defenses/
├── verifications/
├── judge_results/
├── patches/
├── lineages/
├── pareto_fronts/
└── archives/
```

测试目录：

```text
tests/
├── test_theory_spec.py
├── test_claim_schema.py
├── test_challenge_schema.py
├── test_defense_schema.py
├── test_verifier_bridge.py
├── test_judge.py
├── test_patch_gate.py
├── test_pareto.py
├── test_elo.py
├── test_niches.py
├── test_duel_protocol.py
├── test_tournament.py
├── test_parallel_evolution.py
└── test_adversarial_e2e.py
```

---

## 6. 核心数据模型

建议全部使用 Pydantic，确保 YAML/JSON 可验证。

### 6.1 Severity

```python
from enum import Enum

class Severity(str, Enum):
    INFO = "info"
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"
    FATAL = "fatal"
```

语义：

```text
INFO:
  建议或观察，不影响补丁。

MINOR:
  小问题，可能影响说明、边界或可读性。

MAJOR:
  影响某个模块或结论，需要修正、分叉或扣分。

CRITICAL:
  违反硬物理、数值一致性或 benchmark，必须修正。

FATAL:
  理论整体不可运行或核心假设自相矛盾，暂停进入 tournament。
```

### 6.2 ChallengeType

```python
class ChallengeType(str, Enum):
    DIMENSIONAL_INCONSISTENCY = "dimensional_inconsistency"
    CONSERVATION_VIOLATION = "conservation_violation"
    INTERNAL_CONTRADICTION = "internal_contradiction"
    NUMERICAL_INSTABILITY = "numerical_instability"
    FAILED_BENCHMARK = "failed_benchmark"
    REPRODUCIBLE_COUNTEREXAMPLE = "reproducible_counterexample"
    UNJUSTIFIED_ASSUMPTION = "unjustified_assumption"
    OVERFITTING_TO_STANDARD_UNIVERSE = "overfitting_to_standard_universe"
    UNDERCONSTRAINED_PARAMETER = "underconstrained_parameter"
    COMPUTATIONAL_INFEASIBILITY = "computational_infeasibility"
    LOW_GENERATIVE_POWER = "low_generative_power"
    LOW_FALSIFIABILITY = "low_falsifiability"
    MISLEADING_CLAIM = "misleading_claim"
    MISSING_BOUNDARY_CONDITION = "missing_boundary_condition"
    REGRESSION_RISK = "regression_risk"
```

### 6.3 EvidenceItem

```python
class EvidenceType(str, Enum):
    FORMULA = "formula"
    NUMERICAL_RESULT = "numerical_result"
    TEST_RESULT = "test_result"
    CONFIG_SNIPPET = "config_snippet"
    MODULE_OUTPUT = "module_output"
    LOG_EXCERPT = "log_excerpt"
    REFERENCE = "reference"
    ARGUMENT = "argument"


class EvidenceItem(BaseModel):
    evidence_type: EvidenceType
    summary: str
    content: str | dict
    source: str | None = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
```

### 6.4 Claim

```python
class Claim(BaseModel):
    claim_id: str
    statement: str
    module: str | None = None
    config_path: str | None = None
    test_refs: list[str] = []
    dependencies: list[str] = []
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    falsifiability: float = Field(default=0.5, ge=0.0, le=1.0)
    scope: str = "default"
    known_limits: list[str] = []
```

### 6.5 DefensePrior

```python
class DefensePrior(BaseModel):
    default_stance: str = "defend"

    accept_patch_only_if: list[str] = [
        "formal_validation_fails",
        "reproducible_counterexample_exists",
        "independent_verifier_confirms",
        "patch_improves_pareto_score_without_regression"
    ]

    reject_if: list[str] = [
        "criticism_is_style_preference",
        "no_reproduction_command",
        "no_test_case",
        "proposed_patch_reduces_explanatory_power",
        "proposed_patch_hides_problem_without_solving",
        "criticism_conflicts_with_theory_philosophy_but_has_no_hard_error"
    ]

    conservatism: float = Field(default=0.7, ge=0.0, le=1.0)
    novelty_preference: float = Field(default=0.3, ge=0.0, le=1.0)
    minimum_evidence_threshold: float = Field(default=0.6, ge=0.0, le=1.0)
```

### 6.6 TheoryPhilosophy

```python
class TheoryPhilosophy(BaseModel):
    summary: str
    conservatism: float = Field(ge=0.0, le=1.0)
    novelty: float = Field(ge=0.0, le=1.0)
    computational_efficiency: float = Field(ge=0.0, le=1.0)
    bottom_up_derivation: float = Field(ge=0.0, le=1.0)
    empirical_fidelity: float = Field(ge=0.0, le=1.0)
```

### 6.7 TheorySpec

```python
class TheorySpec(BaseModel):
    theory_id: str
    name: str
    family: str
    version: str
    parent_id: str | None = None

    philosophy: TheoryPhilosophy
    axioms: dict[str, Any]
    physics_stack: dict[str, str]
    config_paths: list[str]
    claims: list[Claim]
    known_limits: list[str] = []
    defense_prior: DefensePrior = DefensePrior()

    lineage_policy: dict[str, Any] = {
        "allow_patch": True,
        "allow_fork": True,
        "allow_merge": False,
        "preserve_parent": True,
    }

    created_at: str | None = None
    updated_at: str | None = None
```

关键字段：

```text
allow_merge: false
```

默认禁止强制合并。

### 6.8 ChallengeCard

```python
class ChallengeCard(BaseModel):
    challenge_id: str
    source_theory_id: str
    target_theory_id: str
    target_claim_id: str | None = None

    challenge_type: ChallengeType
    severity: Severity

    summary: str
    detailed_argument: str

    evidence: list[EvidenceItem] = []
    reproduction_command: str | None = None
    proposed_test_name: str | None = None
    proposed_test_description: str | None = None
    expected_failure_mode: str | None = None
    suggested_patch_summary: str | None = None

    created_by: str
    created_at: str | None = None
```

### 6.9 DefenseStance

```python
class DefenseStance(str, Enum):
    REJECT = "reject"
    ACCEPT = "accept"
    PARTIAL_ACCEPT = "partial_accept"
    REQUEST_TEST = "request_test"
    COUNTER_CHALLENGE = "counter_challenge"
    FORK_INSTEAD_OF_PATCH = "fork_instead_of_patch"
```

### 6.10 DefenseCard

```python
class DefenseCard(BaseModel):
    defense_id: str
    challenge_id: str
    target_theory_id: str

    stance: DefenseStance
    summary: str
    argument: str

    accepted_points: list[str] = []
    rejected_points: list[str] = []
    counter_evidence: list[EvidenceItem] = []
    requested_tests: list[str] = []
    proposed_minimal_patch: str | None = None
    proposed_fork_reason: str | None = None
```

### 6.11 VerificationResult

```python
class VerificationResult(BaseModel):
    verification_id: str
    challenge_id: str
    target_theory_id: str

    reproduced: bool
    tests_run: list[str] = []
    tests_passed: bool
    validation_errors: list[str] = []
    validation_warnings: list[str] = []

    measured_effect: dict[str, Any] = {}
    benchmark_delta: dict[str, float] = {}
    verifier_summary: str

    created_at: str | None = None
```

### 6.12 JudgeDecision

```python
class JudgeDecision(str, Enum):
    CHALLENGE_REJECTED = "challenge_rejected"
    CHALLENGE_UPHELD_NO_PATCH = "challenge_upheld_no_patch"
    PATCH_REQUIRED = "patch_required"
    PATCH_ACCEPTED = "patch_accepted"
    PATCH_REJECTED = "patch_rejected"
    NEEDS_MORE_TESTS = "needs_more_tests"
    THEORY_INVALIDATED = "theory_invalidated"
    FORK_RECOMMENDED = "fork_recommended"
```

### 6.13 JudgeResult

```python
class JudgeResult(BaseModel):
    judge_result_id: str
    challenge_id: str
    target_theory_id: str

    decision: JudgeDecision
    severity: Severity
    rationale: str

    required_actions: list[str] = []
    patch_required: bool = False
    fork_recommended: bool = False
    score_delta: dict[str, float] = {}
```

### 6.14 PatchProposal

```python
class PatchProposal(BaseModel):
    patch_id: str
    theory_id: str
    based_on_challenge_id: str

    summary: str
    patch_type: str  # config_patch, claim_patch, code_patch, documentation_patch, test_patch
    files_to_modify: list[str]
    diff_text: str | None = None
    expected_improvements: dict[str, float] = {}
    expected_risks: list[str] = []
    new_tests: list[str] = []

    preserve_lineage: bool = True
    creates_fork: bool = False
    child_theory_id: str | None = None
```

### 6.15 TheoryScoreVector

```python
class TheoryScoreVector(BaseModel):
    theory_id: str
    version: str

    validity: float = Field(ge=0.0, le=1.0)
    physical_consistency: float = Field(ge=0.0, le=1.0)
    benchmark_fit: float = Field(ge=0.0, le=1.0)
    generative_power: float = Field(ge=0.0, le=1.0)
    robustness: float = Field(ge=0.0, le=1.0)
    novelty: float = Field(ge=0.0, le=1.0)
    simplicity: float = Field(ge=0.0, le=1.0)
    computational_efficiency: float = Field(ge=0.0, le=1.0)
    unresolved_challenge_penalty: float = Field(ge=0.0, le=1.0)

    family: str
    generation: int
```

---

## 7. TheorySpec 示例

### 7.1 Conservative-EFT

文件：`theories/T-0001_standard_eft/theory.yaml`

```yaml
theory_id: T-0001
name: Conservative-EFT Universe Compiler
family: conservative_eft
version: 0.1.0
parent_id: null

philosophy:
  summary: "Use known physics and effective theory layers. Prioritize internal consistency, benchmark fidelity, and reproducibility."
  conservatism: 0.90
  novelty: 0.20
  computational_efficiency: 0.70
  bottom_up_derivation: 0.85
  empirical_fidelity: 0.90

axioms:
  spacetime_dimensions: 4
  locality: true
  lorentz_invariance: true
  action_principle: true
  quantum_fields: effective
  gravity: friedmann_gr

physics_stack:
  particle_model: effective_standard_model
  atomic_model: hydrogenic
  nuclear_model: toy_bbn
  cosmology_model: friedmann_background
  stellar_model: conservative_scaling
  structure_model: heuristic
  complexity_model: conservative_weighted_window

config_paths:
  - configs/standard_universe.yaml

claims:
  - claim_id: C-atom-001
    statement: "Stable hydrogen exists if alpha < 1, positive electron and proton masses, and positive binding energy."
    module: atomic.hydrogen
    test_refs:
      - tests/test_atomic.py::test_standard_hydrogen_binding_energy
    confidence: 0.85
    falsifiability: 0.95

  - claim_id: C-star-001
    statement: "Long-lived stars require stable hydrogen, stable deuteron, helium stability, and moderate gravity scale."
    module: stars.stellar_scaling
    test_refs:
      - tests/test_stars.py::test_standard_universe_has_long_lived_stars
    confidence: 0.70
    falsifiability: 0.80

known_limits:
  - "Does not solve full QCD."
  - "Does not implement full stellar evolution."
  - "Life score is a physical window score, not a probability of life."

defense_prior:
  default_stance: defend
  conservatism: 0.90
  novelty_preference: 0.20
  minimum_evidence_threshold: 0.70
  accept_patch_only_if:
    - formal_validation_fails
    - reproducible_counterexample_exists
    - independent_verifier_confirms
    - patch_improves_pareto_score_without_regression
  reject_if:
    - criticism_is_style_preference
    - no_reproduction_command
    - no_test_case
    - proposed_patch_reduces_explanatory_power
    - proposed_patch_hides_problem_without_solving

lineage_policy:
  allow_patch: true
  allow_fork: true
  allow_merge: false
  preserve_parent: true
```

### 7.2 Exploratory-Generative

文件：`theories/T-0002_exploratory_generative/theory.yaml`

```yaml
theory_id: T-0002
name: Exploratory Generative Universe Engine
family: exploratory_generative
version: 0.1.0
parent_id: null

philosophy:
  summary: "Prioritize valid alternative universes, broad parameter exploration, and generative diversity while preserving hard consistency checks."
  conservatism: 0.45
  novelty: 0.90
  computational_efficiency: 0.65
  bottom_up_derivation: 0.55
  empirical_fidelity: 0.50

axioms:
  spacetime_dimensions: 4
  locality: true
  lorentz_invariance: soft_required
  action_principle: true
  quantum_fields: effective_or_parametric
  gravity: parameterized_friedmann

physics_stack:
  particle_model: parameterized_effective_particles
  atomic_model: generalized_atomic_window
  nuclear_model: parameter_scan_nuclear_window
  cosmology_model: parameterized_background
  stellar_model: broad_scaling
  structure_model: heuristic_with_scan
  complexity_model: exploratory_weighted_window

config_paths:
  - configs/exploratory_universe.yaml

claims:
  - claim_id: C-diversity-001
    statement: "A universe theory should be rewarded for producing multiple self-consistent non-standard universes, not only reproducing our universe."
    module: optimization.novelty
    test_refs:
      - tests/test_novelty.py::test_valid_nonstandard_universe_gets_novelty_score
    confidence: 0.65
    falsifiability: 0.70

known_limits:
  - "Less conservative than T-0001."
  - "May require stronger verifier checks to avoid overclaiming complexity."

defense_prior:
  default_stance: defend
  conservatism: 0.45
  novelty_preference: 0.90
  minimum_evidence_threshold: 0.60
  accept_patch_only_if:
    - formal_validation_fails
    - reproducible_counterexample_exists
    - independent_verifier_confirms
    - patch_improves_pareto_score_without_regression
  reject_if:
    - criticism_is_only_that_the_model_is_not_standard_like
    - no_reproduction_command
    - no_test_case
    - proposed_patch_removes_valid_alternative_universes

lineage_policy:
  allow_patch: true
  allow_fork: true
  allow_merge: false
  preserve_parent: true
```

---

## 8. Agent 设计

### 8.1 基类

```python
class TheoryAgent(Protocol):
    theory: TheorySpec

    def generate_report(self) -> UniverseReport:
        ...

    def attack(
        self,
        target_theory: TheorySpec,
        target_report: UniverseReport,
    ) -> list[ChallengeCard]:
        ...

    def defend(
        self,
        challenges: list[ChallengeCard],
        own_report: UniverseReport,
    ) -> list[DefenseCard]:
        ...

    def propose_patch(
        self,
        judge_results: list[JudgeResult],
    ) -> list[PatchProposal]:
        ...
```

### 8.2 Rule-based Agents

第一版优先实现规则型 Agent，避免系统被 LLM 不稳定性拖垮。

```text
ConservativeEFTAgent:
  - 强调 benchmark fidelity
  - 攻击过度生成、无约束参数、未标注 toy model
  - 防守标准物理近似和保守阈值

ExploratoryGenerativeAgent:
  - 强调 generative diversity
  - 攻击过度拟合标准宇宙、参数范围过窄
  - 防守非标准但自洽宇宙

MinimalAxiomAgent:
  - 攻击参数过多、假设过多
  - 防守更少公理的解释力

EfficiencyAgent:
  - 攻击计算成本过高
  - 防守 toy approximation 的工程价值
```

### 8.3 LLM Agents

后续可以接 LLM，但必须约束输出。

```python
class LLMTheoryAgent:
    def attack(self, target_theory, target_report):
        raw = llm.generate(critic_prompt)
        cards = parse_yaml_or_json(raw)
        return [ChallengeCard.model_validate(c) for c in cards]

    def defend(self, challenges, own_report):
        raw = llm.generate(defender_prompt)
        cards = parse_yaml_or_json(raw)
        return [DefenseCard.model_validate(c) for c in cards]
```

要求：

```text
1. LLM 输出必须通过 schema。
2. 不能解析的 challenge 直接丢弃并记录 malformed。
3. LLM 不能直接改代码。
4. LLM 不能绕过 Verifier 和 Judge。
5. LLM 不能强制合并理论。
```

---

## 9. 对抗协议 Duel Protocol

### 9.1 单轮 Duel

```text
Input:
  Theory A
  Theory B

Step 1:
  Run UniversePipeline(A) → Report A
  Run UniversePipeline(B) → Report B

Step 2:
  B attacks A → ChallengeCards B→A
  A defends → DefenseCards A

Step 3:
  Verifier evaluates B→A challenges
  Judge decides B→A results
  PatchGate updates A if required

Step 4:
  A attacks B → ChallengeCards A→B
  B defends → DefenseCards B

Step 5:
  Verifier evaluates A→B challenges
  Judge decides A→B results
  PatchGate updates B if required

Step 6:
  Compute duel score vector
  Save DuelReport
```

### 9.2 伪代码

```python
def run_duel(
    theory_a: TheorySpec,
    theory_b: TheorySpec,
    rounds: int,
    allow_fork: bool = True,
    allow_merge: bool = False,
) -> DuelReport:
    assert allow_merge is False

    history = []
    current_a = theory_a
    current_b = theory_b

    for round_id in range(rounds):
        report_a = run_universe_pipeline_for_theory(current_a)
        report_b = run_universe_pipeline_for_theory(current_b)

        challenges_b_to_a = agent_for(current_b).attack(current_a, report_a)
        defenses_a = agent_for(current_a).defend(challenges_b_to_a, report_a)
        verifications_b_to_a = verifier.evaluate_many(current_a, challenges_b_to_a, defenses_a)
        judge_results_b_to_a = judge.decide_many(challenges_b_to_a, defenses_a, verifications_b_to_a)

        current_a, patch_events_a = patch_gate.process(
            target_theory=current_a,
            judge_results=judge_results_b_to_a,
            allow_fork=allow_fork,
            allow_merge=False,
        )

        challenges_a_to_b = agent_for(current_a).attack(current_b, report_b)
        defenses_b = agent_for(current_b).defend(challenges_a_to_b, report_b)
        verifications_a_to_b = verifier.evaluate_many(current_b, challenges_a_to_b, defenses_b)
        judge_results_a_to_b = judge.decide_many(challenges_a_to_b, defenses_b, verifications_a_to_b)

        current_b, patch_events_b = patch_gate.process(
            target_theory=current_b,
            judge_results=judge_results_a_to_b,
            allow_fork=allow_fork,
            allow_merge=False,
        )

        history.append(
            DuelRoundReport(
                round_id=round_id,
                theory_a=current_a.theory_id,
                theory_b=current_b.theory_id,
                challenges_b_to_a=challenges_b_to_a,
                challenges_a_to_b=challenges_a_to_b,
                judge_results=judge_results_b_to_a + judge_results_a_to_b,
                patch_events=patch_events_a + patch_events_b,
            )
        )

    return DuelReport(
        theory_a=current_a,
        theory_b=current_b,
        rounds=history,
        allow_merge=False,
    )
```

---

## 10. Verifier 设计

Verifier 是系统的硬裁判，不参与理论偏好。

### 10.1 Verifier 职责

```text
1. 运行目标理论对应配置。
2. 运行 UniversePipeline。
3. 运行指定测试。
4. 检查 challenge 中提出的 failure mode。
5. 生成 VerificationResult。
6. 不提出哲学判断。
7. 不决定补丁是否接受。
```

### 10.2 Verifier 检查项

```text
- config 是否可加载
- pipeline 是否可运行
- validation 是否通过
- benchmark 是否满足
- proposed_test 是否失败或通过
- challenge 是否复现
- patch 后是否修复
- patch 是否引入 regression
```

### 10.3 VerifierBridge

文件：`src/quanta_engine/adversarial/verifier_bridge.py`

接口：

```python
class VerifierBridge:
    def evaluate_challenge(
        self,
        target_theory: TheorySpec,
        challenge: ChallengeCard,
        defense: DefenseCard | None = None,
    ) -> VerificationResult:
        ...

    def run_regression_suite(
        self,
        theory: TheorySpec,
    ) -> RegressionReport:
        ...

    def compare_before_after(
        self,
        old_theory: TheorySpec,
        new_theory: TheorySpec,
    ) -> PatchVerificationReport:
        ...
```

---

## 11. Judge 设计

Judge 结合 Challenge、Defense、Verification 进行判定。

### 11.1 Judge 决策规则

```text
如果 challenge 没有具体对象：
  CHALLENGE_REJECTED

如果 challenge 没有证据但可测试：
  NEEDS_MORE_TESTS

如果 verifier 不能复现：
  CHALLENGE_REJECTED

如果 verifier 复现 hard error:
  PATCH_REQUIRED

如果 verifier 复现 soft issue:
  CHALLENGE_UPHELD_NO_PATCH 或 FORK_RECOMMENDED

如果 patch 修复问题但引入 regression:
  PATCH_REJECTED

如果 patch 修复 critical issue 且无 regression:
  PATCH_ACCEPTED

如果理论无法运行:
  THEORY_INVALIDATED
```

### 11.2 硬错误与软错误

硬错误：

```text
- CRITICAL/FATAL
- formal validation fails
- benchmark fails
- internal contradiction
- numerical instability
```

软错误：

```text
- low novelty
- low generative power
- high computational cost
- overly conservative
- under-explained assumption
```

软错误不能强制修改，只能：

```text
- 扣分
- 加 warning
- 建议 fork
- 建议增加 claim 边界
```

---

## 12. PatchGate 设计

PatchGate 是防止理论乱改和强制合并的关键。

### 12.1 PatchGate 输入

```text
target_theory
judge_results
patch_proposals
old_score_vector
new_score_vector
regression_report
```

### 12.2 PatchGate 输出

```text
- theory unchanged
- theory patched to new version
- child theory forked
- theory invalidated
- patch rejected
```

### 12.3 PatchGate 规则

```text
1. 不允许 merge。
2. CRITICAL hard error 必须 patch 或 invalidate。
3. MAJOR hard error 可以 patch 或 fork。
4. Soft issue 不强制 patch。
5. Patch 必须最小化。
6. Patch 必须通过 regression。
7. Patch 必须记录 history。
8. 如果 patch 会改变理论哲学，应 fork，而不是覆盖原理论。
9. 父理论默认保留。
```

### 12.4 何时 patch，何时 fork

Patch：

```text
适用于理论内部 bug：
- alpha >= 1 却标记 stable_hydrogen
- 单位换算错误
- benchmark 阈值写反
- missing validation check
```

Fork：

```text
适用于理论哲学变化：
- 保守理论想引入激进探索评分
- 标准宇宙拟合理论想变成多宇宙生成理论
- toy model 想替换成高精度模块
- 复杂性评分逻辑发生大改
```

不改：

```text
适用于对方只是偏好不同：
- “你的理论不够激进”
- “你的理论太保守”
- “你的模型不够漂亮”
```

---

## 13. 并行优化系统

### 13.1 Population

```python
class TheoryPopulation(BaseModel):
    generation: int
    theories: list[TheorySpec]
    archive: list[TheorySpec] = []
    pareto_front: list[str] = []
    family_elites: dict[str, list[str]] = {}
```

### 13.2 每一代的流程

```text
Generation g:
  1. Run all theories in parallel.
  2. Compute score vector for each theory.
  3. Pair theories for duels.
  4. Run duels in parallel.
  5. Apply patches/forks locally.
  6. Re-score changed theories.
  7. Update Elo/Glicko.
  8. Compute Pareto front.
  9. Apply niche preservation.
  10. Archive valid diverse theories.
  11. Select next generation without collapsing to one theory.
```

### 13.3 伪代码

```python
def evolve_population(
    population: TheoryPopulation,
    generations: int,
    min_families: int = 3,
    elites_per_family: int = 2,
    allow_merge: bool = False,
) -> EvolutionReport:
    assert allow_merge is False

    current = population

    for g in range(generations):
        reports = run_all_theories_parallel(current.theories)
        scores = score_all(current.theories, reports)

        pairings = make_duel_pairings(
            theories=current.theories,
            strategy="round_robin_or_swiss",
            preserve_family_diversity=True,
        )

        duel_reports = run_duels_parallel(pairings, allow_merge=False)

        updated_theories = collect_updated_theories(
            original=current.theories,
            duel_reports=duel_reports,
            preserve_parents=True,
        )

        rescored = score_all(updated_theories, run_all_theories_parallel(updated_theories))

        pareto = compute_pareto_front(rescored)
        family_elites = select_family_elites(rescored, elites_per_family)
        novelty_archive = update_novelty_archive(current.archive, updated_theories, rescored)

        next_theories = select_next_generation(
            theories=updated_theories,
            pareto_front=pareto,
            family_elites=family_elites,
            archive=novelty_archive,
            min_families=min_families,
            no_single_winner=True,
        )

        current = TheoryPopulation(
            generation=g + 1,
            theories=next_theories,
            archive=novelty_archive,
            pareto_front=[t.theory_id for t in pareto],
            family_elites=family_elites,
        )

    return EvolutionReport(final_population=current)
```

---

## 14. 多目标评分

### 14.1 分数向量

不要只用总分。

```text
validity:
  硬约束是否通过。

physical_consistency:
  守恒律、维度、数值稳定、内部一致性。

benchmark_fit:
  标准宇宙 benchmark 的复现能力。

generative_power:
  能否生成稳定原子、恒星、结构、复杂化学、非标准宇宙。

robustness:
  参数轻微扰动下结果是否稳定。

novelty:
  能否生成不同于标准宇宙但仍自洽的结果。

simplicity:
  假设数量、自由参数数量、补丁复杂度。

computational_efficiency:
  运行速度、内存成本、扫描能力。

unresolved_challenge_penalty:
  未解决 challenge 数量和严重度。
```

### 14.2 总分可以用于展示，但不能用于唯一选择

展示用：

```python
display_score = (
    0.20 * validity
    + 0.15 * physical_consistency
    + 0.15 * benchmark_fit
    + 0.15 * generative_power
    + 0.10 * robustness
    + 0.10 * novelty
    + 0.05 * simplicity
    + 0.05 * computational_efficiency
    - 0.05 * unresolved_challenge_penalty
)
```

但 selection 用：

```text
Pareto front + family elites + novelty archive
```

### 14.3 Pareto Dominance

```python
def pareto_dominates(a: TheoryScoreVector, b: TheoryScoreVector) -> bool:
    objectives = [
        "validity",
        "physical_consistency",
        "benchmark_fit",
        "generative_power",
        "robustness",
        "novelty",
        "simplicity",
        "computational_efficiency",
    ]

    no_worse = all(getattr(a, x) >= getattr(b, x) for x in objectives)
    strictly_better = any(getattr(a, x) > getattr(b, x) for x in objectives)

    penalty_no_worse = a.unresolved_challenge_penalty <= b.unresolved_challenge_penalty

    return no_worse and strictly_better and penalty_no_worse
```

### 14.4 Niche Preservation

防止所有理论都变成同一种。

```python
def select_family_elites(scores, elites_per_family=2):
    groups = group_by_family(scores)
    elites = {}
    for family, family_scores in groups.items():
        elites[family] = sorted(
            family_scores,
            key=lambda s: (
                s.validity,
                s.physical_consistency,
                s.generative_power,
                s.robustness,
            ),
            reverse=True,
        )[:elites_per_family]
    return elites
```

---

## 15. Novelty Search

### 15.1 为什么需要 Novelty

如果只优化 benchmark_fit，所有理论都会向标准宇宙坍缩。

但是创世模型需要：

```text
- 标准宇宙
- 类标准宇宙
- 弱引力长寿命恒星宇宙
- 强电磁短尺度化学宇宙
- 低扰动延迟结构形成宇宙
- 稳定原子但无复杂生命宇宙
- 有复杂化学但短文明窗口宇宙
```

### 15.2 Novelty 特征向量

```python
novelty_features = [
    alpha_scale,
    gravity_scale,
    strong_scale,
    weak_scale,
    cosmological_constant_scale,
    hydrogen_binding_energy_eV,
    bohr_radius_m,
    stellar_lifetime_years,
    universe_age_Gyr,
    life_window_score,
    civilization_potential_score,
]
```

### 15.3 Novelty 分数

```python
def novelty_score(theory_result, archive_results, k=5):
    distances = [
        normalized_distance(theory_result.features, other.features)
        for other in archive_results
    ]
    nearest = sorted(distances)[:k]
    return sum(nearest) / max(len(nearest), 1)
```

前提：

```text
hard validity 必须通过。
不自洽宇宙不能靠 novelty 得高分。
```

---

## 16. Benchmark Suite

### 16.1 Standard Universe Benchmark

标准宇宙必须大致通过：

```text
- Hydrogen binding energy ≈ 13.6 eV
- Bohr radius ≈ 5.29e-11 m
- Universe age in broad range 10–20 Gyr
- stable_hydrogen = true
- deuteron_stable = true
- helium4_stable = true
- hydrogen_fusion_possible = true
- structure_growth_possible = true
```

### 16.2 Failure Benchmarks

必须正确失败：

```text
alpha_scale very large:
  stable_hydrogen = false
  chemistry_score near zero

deuteron_binding < 0:
  deuteron_stable = false
  ordinary stellar nucleosynthesis suppressed

primordial_amplitude = 0:
  structure_growth_possible = false

gravity_scale very high:
  stellar_lifetime too short
  long_lived_stars_possible = false
```

### 16.3 Robustness Benchmarks

轻微扰动不应导致非连续灾难：

```text
alpha_scale = 0.95, 1.00, 1.05
gravity_scale = 0.8, 1.0, 1.2
omega_m slight perturbations
```

### 16.4 Alternative Universe Benchmarks

鼓励生成非标准但自洽宇宙：

```text
weak_gravity_universe:
  longer stellar lifetime

slightly_stronger_alpha_universe:
  smaller Bohr radius
  stronger chemistry energy scale

low_primordial_amplitude_universe:
  delayed or reduced structure formation

low_lambda_universe:
  extended structure growth window
```

---

## 17. CLI 设计

### 17.1 Theory 命令

```bash
quanta theory list
quanta theory show T-0001
quanta theory validate theories/T-0001_standard_eft/theory.yaml
quanta theory lineage T-0001
```

### 17.2 Duel 命令

```bash
quanta duel \
  theories/T-0001_standard_eft/theory.yaml \
  theories/T-0002_exploratory_generative/theory.yaml \
  --rounds 3 \
  --output reports/duels/T0001_vs_T0002.md
```

### 17.3 Challenge 命令

```bash
quanta challenge \
  --source theories/T-0002_exploratory_generative/theory.yaml \
  --target theories/T-0001_standard_eft/theory.yaml \
  --output reports/challenges/
```

### 17.4 Defense 命令

```bash
quanta defend \
  --theory theories/T-0001_standard_eft/theory.yaml \
  --challenge reports/challenges/CH-00042.yaml \
  --output reports/defenses/
```

### 17.5 Verify 命令

```bash
quanta verify-challenge reports/challenges/CH-00042.yaml
```

### 17.6 Tournament 命令

```bash
quanta tournament \
  theories/*/theory.yaml \
  --rounds 5 \
  --output reports/tournaments/generation_000.md
```

### 17.7 Parallel Evolution 命令

```bash
quanta evolve \
  theories/*/theory.yaml \
  --generations 10 \
  --population-size 12 \
  --min-families 4 \
  --elites-per-family 2 \
  --no-merge \
  --output reports/generations/
```

必须支持：

```text
--no-merge
```

且默认开启。

---

## 18. 报告格式

### 18.1 DuelReport

```markdown
# Duel Report: T-0001 vs T-0002

## Settings
- rounds: 3
- allow_merge: false
- preserve_parent: true

## Theory A
- id: T-0001
- family: conservative_eft
- version_before: 0.1.0
- version_after: 0.1.1

## Theory B
- id: T-0002
- family: exploratory_generative
- version_before: 0.1.0
- version_after: 0.1.0

## Round Summary
...

## Challenges B → A
...

## Defenses A
...

## Verifier Results
...

## Judge Results
...

## Patch Events
...

## Final Status
- A patched locally
- B unchanged
- no merge performed
```

### 18.2 EvolutionReport

```markdown
# Parallel Evolution Report

## Generation
5

## Anti-Collapse Rules
- allow_merge: false
- min_families: 4
- elites_per_family: 2
- preserve_parents: true

## Population Summary
| Theory | Family | Version | Validity | Generative | Novelty | Benchmark | Status |
|---|---|---:|---:|---:|---:|---:|---|

## Pareto Front
...

## Family Elites
...

## Archived Valid Alternatives
...

## New Forks
...

## Invalidated Theories
...

## Next Generation
...
```

---

## 19. 端到端测试方案

### E2E-1：两个方案并行存在，不合并

输入：

```text
T-0001 Conservative-EFT
T-0002 Exploratory-Generative
```

运行：

```bash
quanta duel T-0001 T-0002 --rounds 1 --no-merge
```

预期：

```text
- T-0001 仍存在
- T-0002 仍存在
- allow_merge = false
- DuelReport 明确写 no merge performed
- 如果产生新理论，只能是 T-0003 child/fork
```

测试断言：

```python
assert report.allow_merge is False
assert "T-0001" in registry
assert "T-0002" in registry
assert not report.merged_theory_id
```

### E2E-2：批评成立，目标理论局部 patch

场景：

```text
T-0001 某配置 alpha_scale = 200 仍声称 stable_hydrogen = true。
T-0002 提出 challenge。
Verifier 复现。
Judge 要求 patch。
PatchGate 只修改 T-0001。
```

预期：

```text
T-0001 v0.1.0 → T-0001 v0.1.1
T-0002 不变
没有合并
history.jsonl 记录 challenge_id
```

### E2E-3：批评只是偏好，不 patch

场景：

```text
T-0002 批评 T-0001 太保守。
没有具体 claim。
没有测试。
```

预期：

```text
Challenge rejected or soft scoring only.
T-0001 不改。
```

### E2E-4：理论哲学改变时 fork，而不是覆盖

场景：

```text
T-0001 保守理论想引入 T-0002 的激进 novelty scoring。
```

预期：

```text
不直接 patch T-0001。
创建 T-0003 Conservative-EFT-with-Novelty-Branch。
T-0001 保留。
T-0002 保留。
```

### E2E-5：Tournament 保留多个 family

输入：

```text
5 个 theory families
```

运行：

```bash
quanta evolve --generations 3 --min-families 4
```

预期：

```text
最终 population 至少包含 4 个 family。
最高总分理论不能独占 population。
```

---

## 20. 分阶段实现路线

### Phase 1：Schema 与 TheorySpec

目标：

```text
实现 TheorySpec、Claim、ChallengeCard、DefenseCard、JudgeResult、PatchProposal。
```

文件：

```text
src/quanta_engine/theories/theory_spec.py
src/quanta_engine/adversarial/challenge.py
src/quanta_engine/adversarial/defense.py
src/quanta_engine/adversarial/evidence.py
```

验收：

```bash
pytest tests/test_theory_spec.py
pytest tests/test_challenge_schema.py
pytest tests/test_defense_schema.py
```

### Phase 2：Theory Registry 与 Loader

目标：

```text
支持加载 theories/*/theory.yaml。
支持 registry。
支持 theory lineage。
```

文件：

```text
src/quanta_engine/theories/loader.py
src/quanta_engine/theories/registry.py
src/quanta_engine/theories/lineage.py
```

验收：

```bash
quanta theory list
quanta theory show T-0001
quanta theory validate theories/T-0001_standard_eft/theory.yaml
```

### Phase 3：Rule-based Agents

目标：

```text
实现 ConservativeEFTAgent 和 ExploratoryGenerativeAgent。
```

文件：

```text
src/quanta_engine/adversarial/agents.py
src/quanta_engine/adversarial/roles.py
```

验收：

```bash
pytest tests/test_duel_protocol.py
```

### Phase 4：VerifierBridge 与 Judge

目标：

```text
challenge 可以被 verifier 复现。
judge 可以做结构化判定。
```

文件：

```text
src/quanta_engine/adversarial/verifier_bridge.py
src/quanta_engine/adversarial/judge.py
```

验收：

```bash
pytest tests/test_verifier_bridge.py
pytest tests/test_judge.py
```

### Phase 5：PatchGate 与 Lineage

目标：

```text
支持 patch、fork、不合并。
```

文件：

```text
src/quanta_engine/adversarial/patching.py
src/quanta_engine/theories/lineage.py
```

验收：

```bash
pytest tests/test_patch_gate.py
```

### Phase 6：Duel Protocol

目标：

```text
完整运行 T-0001 vs T-0002。
```

文件：

```text
src/quanta_engine/adversarial/duel.py
src/quanta_engine/experiments/duel.py
```

验收：

```bash
quanta duel theories/T-0001_standard_eft/theory.yaml theories/T-0002_exploratory_generative/theory.yaml --rounds 1 --no-merge
```

### Phase 7：Scoring、Pareto、Niche

目标：

```text
多目标评分与不坍缩选择。
```

文件：

```text
src/quanta_engine/adversarial/scoring.py
src/quanta_engine/optimization/objectives.py
src/quanta_engine/optimization/pareto.py
src/quanta_engine/optimization/niches.py
src/quanta_engine/optimization/novelty.py
```

验收：

```bash
pytest tests/test_pareto.py
pytest tests/test_niches.py
```

### Phase 8：Tournament

目标：

```text
多个理论两两对抗。
```

文件：

```text
src/quanta_engine/adversarial/tournament.py
src/quanta_engine/experiments/tournament.py
```

验收：

```bash
quanta tournament theories/*/theory.yaml --rounds 3 --output reports/tournaments/test.md
```

### Phase 9：Parallel Evolution

目标：

```text
多个谱系并行演化，不合并。
```

文件：

```text
src/quanta_engine/experiments/parallel_evolution.py
src/quanta_engine/optimization/population.py
src/quanta_engine/optimization/selection.py
```

验收：

```bash
quanta evolve theories/*/theory.yaml --generations 3 --min-families 3 --no-merge
pytest tests/test_parallel_evolution.py
```

### Phase 10：LLM Agent 接入

目标：

```text
LLM 只负责生成结构化 challenge/defense，不负责直接裁决和改代码。
```

文件：

```text
src/quanta_engine/adversarial/llm_agent.py
src/quanta_engine/adversarial/prompts.py
```

验收：

```text
- malformed LLM output 被拒绝
- schema valid output 进入 verifier
- LLM 不能绕过 no-merge policy
```

---

## 21. AI Coding Agent 总控 Prompt

可以直接给 AI Coding Agent：

```text
You are implementing the adversarial scientific self-play system for QuantaEngine.

Read ADVERSARIAL_SELF_PLAY_IMPLEMENTATION.md.

Hard requirements:
1. Multiple theories must evolve in parallel.
2. Never merge theories into one final theory.
3. Patch only the target theory when a challenge is upheld.
4. If a change would alter a theory's philosophy, create a fork instead of overwriting the parent.
5. Preserve parent theories by default.
6. Use Pydantic schemas for TheorySpec, ChallengeCard, DefenseCard, VerificationResult, JudgeResult, PatchProposal.
7. Use deterministic VerifierBridge for hard physics and benchmark checks.
8. LLM-generated criticism must be schema-validated before use.
9. Selection must use Pareto front + family elites + novelty archive, not single-score winner-takes-all.
10. Add tests for no-merge behavior.

Start with Phase 1 only:
- implement schemas
- add tests
- add example theory.yaml files
- do not implement duel yet

Return:
- changed files
- tests run
- result summary
- next recommended phase
```

---

## 22. Critic Prompt

```text
You are an adversarial scientific critic for a universe-generation theory.

Your job is to attack the target theory, but every criticism must be structured as a ChallengeCard.

Rules:
1. Identify a specific target claim, module, assumption, or output.
2. Explain the alleged inconsistency.
3. Provide evidence.
4. Provide a reproduction command or testable condition whenever possible.
5. Assign severity.
6. Do not make vague stylistic criticism.
7. Do not propose merging theories.
8. You may suggest a local patch or fork, but the target theory must preserve its own lineage.

Return valid YAML list of ChallengeCards.
```

---

## 23. Defender Prompt

```text
You are defending your own universe-generation theory.

Your default stance is to defend the theory.
Do not accept criticism unless it is supported by:
- formal inconsistency
- reproducible failure
- failed validation
- benchmark failure
- contradiction with your own claims

Rules:
1. Do not agree automatically.
2. Reject vague or preference-only criticism.
3. Accept only minimal necessary changes.
4. If a change would alter your theory's philosophy, request a fork instead of patching the parent.
5. Never merge your theory with another theory.
6. Preserve your lineage and assumptions unless hard evidence requires local correction.

Return valid YAML list of DefenseCards.
```

---

## 24. Judge Prompt

```text
You are an independent arbiter.

You do not care which theory wins.
You evaluate:
- ChallengeCard
- DefenseCard
- VerificationResult
- regression risk
- no-merge lineage policy

Rules:
1. If challenge lacks evidence and reproduction, reject or request more tests.
2. If verifier reproduces a hard error, require patch.
3. If issue is soft preference, do not require patch.
4. If proposed change alters theory philosophy, recommend fork.
5. Never merge theories into one.
6. Parent theories must be preserved unless explicitly invalidated by fatal errors.

Return valid JudgeResult objects.
```

---

## 25. PatchGate Prompt

```text
You are PatchGate for a scientific theory lineage.

Input:
- target TheorySpec
- JudgeResult
- PatchProposal
- RegressionReport
- current score vector
- proposed score vector

Rules:
1. Never merge theories.
2. Patch only target theory.
3. Preserve parent theory by default.
4. If patch is small bug fix and passes regression, create new version.
5. If patch changes philosophy, create child fork.
6. If patch introduces regression, reject.
7. If challenge is soft preference, do not patch parent.
8. Record every accepted patch or fork in history.jsonl.

Return PatchGateDecision.
```

---

## 26. 成功标准

这个系统成功不是因为最后得出一个唯一最佳宇宙生成方案，而是因为：

```text
1. 多个理论能够长期并行存在。
2. 理论之间可以互相指出可复现问题。
3. 每个理论可以防守自身，不无条件接受批评。
4. 硬错误能被修正。
5. 软分歧不会导致强制合并。
6. 每个理论有独立版本谱系。
7. Tournament 保留多个 family。
8. Pareto front 展示多个不同方向的优秀方案。
9. Novelty archive 保存有效另类宇宙。
10. 所有决策有日志、测试和报告。
```

---

## 27. 最终项目定位

```text
QuantaEngine 不只是一个宇宙模拟器，而是一个并行多理论创世实验平台。

它允许多个从基本物理出发生成宇宙的方案同时存在、互相挑战、互相防守、独立修正和长期进化。

最终结果不是一个被合并的单一理论，而是一组经过对抗验证的理论谱系：
每个谱系代表一种不同的创世哲学、物理近似、优化目标和宇宙生成能力。
```
