# 方案执行说明

## 目标与边界

本次执行以 `6050e48` 的评估为冻结基线，修复 `QE-2026-001` 至
`QE-2026-008`。范围覆盖 arena 正确性、复现性、兼容性、路径解析、优化几何、
长期历史、测试、CI、wheel 和双远端发布；不改变物理模型的科学精度边界。

## 执行阶段

### 1. 结果可信度

- 将每场 duel 放入隔离 registry 并行计算，再按 pair/round/challenge 固定顺序提交。
- Registry 和 fork 分配使用可重入锁与原子事务，父 lineage 始终保留。
- 用 Blake2 摘要从 run seed、theory、version 和操作名派生随机种子与 challenge ID。
- novelty 改用行为特征，按索引排除自身，并在 evolution 中保存跨代特征 archive。
- 聚合 JudgeResult/PatchEvent；未解决挑战进入 penalty，invalidation 清零有效性。

### 2. 安装与可移植性

- `quanta_engine.version` 成为 `0.3.0` 单一版本源。
- 增加 `quantaengine` deprecated compatibility namespace，转发旧子模块。
- theory 记录来源路径并解析 workspace/config；registry.yaml 成为实际加载清单。
- GenesisArena CLI 增加全局 `--workspace`、`--version` 和各运行命令的 `--seed`。

### 3. 优化与长期记录

- `Axis.log` 在正反归一化中采用 log10 空间，重力每个数量级等距。
- Evolution report 和 lineage history 保存 run identity、seed、版本、commit、theory/config 指纹。
- history 的 `generation` 按文件持续递增，另存 `run_generation`，避免多次运行语义重置。

### 4. 工程门禁

- 新增针对 8 个 finding 的回归文件 `tests/test_remediation.py`。
- CI 在 Python 3.11-3.13 执行 Ruff、format、Mypy、wheel build 和安装 smoke。
- pytest/hypothesis 移至 dev extra，README、CHANGELOG 和可执行计划命令同步更新。

## 验证结果

最终命令结果由 `execution/run_remediation.py` 写入
`records/remediation-evidence.json`。独立复审结论保存在
`docs/reviews/2026-06-21-codebase-remediation.md`；远端提交和 CI 证据在发布后补入。

## 剩余边界

- 本次证明软件契约和工程结果可复现，不等于物理模型经过外部论文级校准。
- 默认理论仍存放在 workspace；wheel smoke 通过显式 `--workspace` 指向版本化输入。
- `quantaengine` 兼容 namespace 在 0.x 保留，新代码应迁移到 `quantaengine_lattice`。
