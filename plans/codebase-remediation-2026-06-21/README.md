# QuantaEngine 代码库修复方案包

`plan_id: codebase-remediation-2026-06-21`

本方案包将 `docs/reviews/2026-06-21-codebase-assessment.md` 的 8 个 finding
转化为可执行、可验证、可继续迭代的工程任务。原评估报告保持为只读基线，修复事实、
测试证据和剩余风险记录在本目录以及独立复审报告中。

## 导航

- [PLAN_MANIFEST.yaml](PLAN_MANIFEST.yaml)：机器可读范围、finding 映射和门禁命令。
- [EXECUTION_REPORT.md](EXECUTION_REPORT.md)：逐阶段执行说明、设计决策和结果。
- [TRACEABILITY_MATRIX.md](TRACEABILITY_MATRIX.md)：finding 到代码、测试和证据的映射。
- [ITERATION_GUIDE.md](ITERATION_GUIDE.md)：后续优化同一方案或分叉试验的流程。
- [execution/run_remediation.py](execution/run_remediation.py)：一键复审执行器。
- [execution/check_coverage.py](execution/check_coverage.py)：关键模块覆盖率门禁。
- [records/remediation-evidence.json](records/remediation-evidence.json)：最近一次结构化证据。

## 执行

```bash
python plans/codebase-remediation-2026-06-21/execution/run_remediation.py
```

执行器运行定向回归、全量测试、Ruff、Mypy、依赖检查、wheel 构建和隔离安装 smoke test，
并原子更新证据 JSON。只有全部检查通过后，finding 才能标记为 `verified`。
