# QuantaEngine 代码库修复复审报告

## 1. 复审元数据

| 字段 | 值 |
|---|---|
| 原评估 | `QE-REVIEW-2026-06-21` |
| 原基线 | `6050e48e095fc87770c7b1e02fc1883f675fe5b3` |
| 实现提交 | `a6db7d93793262ef41a97fa032165199c56ebd39` |
| 覆盖门禁提交 | `ebf7b36a3799e5ec748c75df26101313831de2e1` |
| 复审日期 | 2026-06-21 |
| 结论 | 8 项 finding 全部 `verified`；无剩余开放工程问题 |

原始问题、复现输出和建议保留在
[2026-06-21-codebase-assessment.md](2026-06-21-codebase-assessment.md)，本报告只记录修复与复验证据。

## 2. 结论摘要

arena 已从共享并发写入改为隔离评估加确定性提交，稳定 seed 和 ID 不再依赖
Python salted hash；novelty 使用行为特征并排除自身，裁决结果实际进入 Pareto 与
selection。旧 API、版本、workspace 路径、registry manifest、对数搜索和长期历史
均已修复。质量门禁覆盖 Python 3.11-3.13、Ruff、Mypy、coverage、wheel 和安装 smoke。

## 3. Finding 复审

| Finding | 状态 | 修复摘要 | 关键证据 |
|---|---|---|---|
| `QE-2026-001` | verified | duel 使用隔离 registry；主 registry 固定顺序回放；fork 分配原子化 | 100 个并发 fork ID 唯一；串并行 report 与 registry 相同 |
| `QE-2026-002` | verified | novelty 按索引排除自身，改用 behavior features，并维护跨代 archive | novelty 非零；有效理论进入 archive |
| `QE-2026-003` | verified | Blake2 派生 seed/challenge ID；历史保存 seed、commit 和输入指纹 | 两个 `PYTHONHASHSEED` 子进程输出一致 |
| `QE-2026-004` | verified | 聚合 JudgeResult/PatchEvent；未解决挑战降分，invalidation 清零 | penalty 改变 display 与 Pareto dominance |
| `QE-2026-005` | verified | 单一 `0.3.0` 版本源；增加 deprecated `quantaengine` namespace | 四个版本入口一致；旧子模块 import 与 wheel smoke 通过 |
| `QE-2026-006` | verified | theory 来源路径、workspace CLI 与 manifest 校验生效 | 临时 cwd 下 list/show/score/duel/tournament/evolve smoke 通过 |
| `QE-2026-007` | verified | log axis 正反归一化使用 log10 空间 | `0.01,0.1,1,10,100` 映射为等距坐标 |
| `QE-2026-008` | verified | CI 增加 lint、format、全量 typing、coverage、build 和 wheel smoke | 两个远端各 6 个 Python 3.11-3.13 job 全部成功 |

逐项代码和测试路径见
[修复追踪矩阵](../../plans/codebase-remediation-2026-06-21/TRACEABILITY_MATRIX.md)。

## 4. 本地验证

结构化证据：
[remediation-evidence.json](../../plans/codebase-remediation-2026-06-21/records/remediation-evidence.json)。

| 门禁 | 结果 |
|---|---|
| 定向回归 | 16 passed |
| 全量 pytest | 96 passed |
| cosmogenesis 总覆盖率 | 95.41%，门槛 90% |
| PatchGate 覆盖率 | 100%，门槛 85% |
| GenesisArena CLI 覆盖率 | 94.32%，门槛 85% |
| Ruff lint / format | passed |
| Mypy `src` | 93 个源文件无问题 |
| `pip check` | 无损坏依赖 |
| sdist / wheel build | `quanta_engine-0.3.0` 构建成功 |
| 隔离 wheel smoke | 四包版本、旧 API、workspace CLI 全部通过 |

复审入口：

```bash
python plans/codebase-remediation-2026-06-21/execution/run_remediation.py
```

## 5. 远端与 CI

| 仓库 | 验证提交 | Actions |
|---|---|---|
| `mjincoin/QuantaEngine` | `ebf7b36` | [tests run 27893878011](https://github.com/mjincoin/QuantaEngine/actions/runs/27893878011) |
| `QuantaEngine/QuantaEngine` | `ebf7b36` | [tests run 27893878659](https://github.com/QuantaEngine/QuantaEngine/actions/runs/27893878659) |

两条 run 均为 `success`，每条包含 Python 3.11、3.12、3.13 的 pytest 与 quality，
共 12 个成功 job。两个远端 `main` 在复审时均指向 `ebf7b36`。

## 6. 剩余边界

- 工程 finding 已关闭，但物理模型仍是 MVP toy + analytic，不代表外部论文级数值校准。
- wheel 中不内置可变 theory workspace；从任意 cwd 运行时显式传入 `--workspace`。
- `quantaengine` 兼容 namespace 在 0.x 保留，新代码应迁移到 `quantaengine_lattice`。
- Windows 的 dotted-module pytest-cov 定位会提前导入 NumPy；正式 coverage 门禁使用等价的
  文件系统源路径 `--cov=src/cosmogenesis`，避免改变测试导入生命周期。

## 7. 后续优化方向

1. 为物理阈值增加外部基准数据与不确定性分析，不与本轮工程修复混合。
2. 为 registry reducer 增加显式冲突策略对象，支持未来更多 patch 类型。
3. 在 0.x 结束前统计旧 namespace 使用情况并制定 1.0 移除计划。
4. 新方案沿用同一 run manifest、覆盖率门禁和双远端发布证据。
