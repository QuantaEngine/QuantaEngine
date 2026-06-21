# 修复追踪矩阵

| Finding | 实现位置 | 回归证据 | 验收目标 |
|---|---|---|---|
| `QE-2026-001` | `arena/registry.py`, `patchgate.py`, `tournament.py` | concurrent forks；parallel/serial tournament | ID 唯一、提交不丢失、串并行一致 |
| `QE-2026-002` | `arena/tournament.py`, `bridge.py` | behavior novelty test | 按索引排除自身、跨代 archive、novelty 非零 |
| `QE-2026-003` | `core/reproducibility.py`, agents/scoring/PatchGate | hash-salt subprocess test | seed 和 ID 不依赖 Python salted hash |
| `QE-2026-004` | `arena/scoring.py`, `tournament.py` | adversarial outcome test | 未解决挑战降分，invalidation 清零有效性 |
| `QE-2026-005` | `quanta_engine/version.py`, `quantaengine/` | compatibility/version test；wheel smoke | 旧 import 可用，所有版本入口一致 |
| `QE-2026-006` | `arena/theory.py`, `bridge.py`, `cli.py`, registry manifest | arbitrary-cwd、CLI workspace、manifest tests | theory/config 不依赖 cwd，manifest 生效 |
| `QE-2026-007` | `core/parameters.py` | equal-decade log-axis test | 每个数量级在归一化空间等距 |
| `QE-2026-008` | CI、pyproject、plan manifests、README | Ruff、Mypy、build、wheel smoke、双远端校验 | 本地和 CI 门禁完整，发布状态一致 |

完整命令及其时间、返回码和输出摘要保存在
`records/remediation-evidence.json`。原始问题叙述和基线复现保存在
`docs/reviews/2026-06-21-codebase-assessment.md`，不随修复重写。
