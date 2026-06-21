# QuantaEngine 方案库

本目录用于保存可迭代、可执行、可追踪的宇宙生成方案。每个方案包都应同时包含方案入口、机器可读清单、执行说明、代码映射、验收程序和历史证据，避免只留下无法复现的设计文档。

## 当前方案

| 方案 | 状态 | 入口 | 适用范围 |
|---|---|---|---|
| QuantaEngine MVP v1 | 已实现并验收 | [quantaengine-mvp-v1/README.md](quantaengine-mvp-v1/README.md) | 从有效物理参数生成粒子、原子、核、宇宙学、恒星、结构与复杂性报告 |
| 2026-06-21 代码库修复 | 已验证 | [codebase-remediation-2026-06-21/README.md](codebase-remediation-2026-06-21/README.md) | 评估 finding 修复、回归、覆盖率、wheel 与双远端发布证据 |

原始完整方案保存在 [2026-06-20-QuantaEngine_PROJECT_PLAN.md](2026-06-20-QuantaEngine_PROJECT_PLAN.md)，作为需求来源和历史基线，不随实现细节重写。

## 新方案约定

新增或分叉方案时，复制现有方案包的目录结构并更换唯一 `plan_id`：

```text
plans/<plan-id>/
├── README.md                 # 导航和状态
├── PLAN_MANIFEST.yaml        # 机器可读范围、命令、阈值、产物
├── EXECUTION_REPORT.md       # 方案执行说明与决策记录
├── TRACEABILITY_MATRIX.md    # 需求到代码、测试、证据的映射
├── ITERATION_GUIDE.md        # 修改和回归流程
├── DOCUMENT_MAP.md           # 关联文档索引
├── execution/
│   └── run_acceptance.py     # 可重复运行的端到端验收代码
├── templates/
│   └── universe_variant.yaml # 新宇宙场景模板
└── records/
    └── acceptance-evidence.json
```

方案只有在清单、实现、测试和证据同时更新后，才应标记为完成。
