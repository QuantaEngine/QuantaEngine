# QuantaEngine MVP v1 方案包

`plan_id: quantaengine-mvp-v1`

本方案包是 2026-06-20 原始项目方案的可执行归档，覆盖原方案阶段 0 到 11、第一轮任务 A 到 O，以及五类端到端宇宙场景。V2 到 V6 高级路线不属于本方案的完成范围。

## 导航

- [原始方案](../2026-06-20-QuantaEngine_PROJECT_PLAN.md)：需求和科学目标的权威来源。
- [PLAN_MANIFEST.yaml](PLAN_MANIFEST.yaml)：工具命令、物理阈值、场景和产物的机器可读定义。
- [EXECUTION_REPORT.md](EXECUTION_REPORT.md)：详细执行过程、关键选择、结果与限制。
- [TRACEABILITY_MATRIX.md](TRACEABILITY_MATRIX.md)：每个阶段对应的实现、测试和证据。
- [ITERATION_GUIDE.md](ITERATION_GUIDE.md)：优化同一方案或测试新方案的标准流程。
- [DOCUMENT_MAP.md](DOCUMENT_MAP.md)：仓库说明文档与本方案的关系。
- [execution/run_acceptance.py](execution/run_acceptance.py)：一键执行工具门禁、生成宇宙并检查阈值。
- [templates/universe_variant.yaml](templates/universe_variant.yaml)：新宇宙变体模板。
- [records/acceptance-evidence.json](records/acceptance-evidence.json)：最近一次完整验收的结构化证据。

## 一键复验

在仓库根目录运行：

```bash
python -m pip install -e ".[dev]"
python plans/quantaengine-mvp-v1/execution/run_acceptance.py
```

验收器会执行 pytest、Ruff、Mypy、依赖检查，生成标准宇宙和失败型宇宙，重建报告与扫描图，并将结果写入 `records/acceptance-evidence.json`。

## 当前状态

- 实现状态：完成
- 本地验收：完成
- GitHub Actions：完成
- 物理精度：MVP toy + analytic，不是精密预测工具
