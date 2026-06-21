# 迭代指南

## 优化同一方案

1. 从 `PLAN_MANIFEST.yaml` 选择 finding 或质量门禁，不直接修改原始评估报告。
2. 先增加可失败的定向回归，再修改最小所属模块。
3. 运行 `execution/run_remediation.py`，确认结构化证据全部为 `passed`。
4. 更新追踪矩阵、执行报告和独立复审报告，记录行为变化与剩余风险。
5. 提交后同步 `origin/main` 与 `quantaengine/main`，核对两个远端哈希和 CI。

## 测试新方案

1. 复制本方案包到新的唯一 `plan_id`，将状态设为 `experimental`。
2. 保留基线命令和现有回归，不覆盖本方案的 evidence。
3. 把新算法放在独立模块或 feature branch，通过同一输入、run seed 和指标比较。
4. 若改变评分、搜索几何或 lineage 语义，必须记录迁移策略和历史兼容方式。
5. 只有新方案同时通过科学契约、确定性、并发和安装 smoke 后才可替换当前方案。

## 历史与复现

- 每个 evolve run 保存 `run_id`、`run_seed`、软件版本、代码提交和输入指纹。
- lineage `generation` 是文件级单调序号，`run_generation` 是单次运行内序号。
- 对比串并行结果时固定 `run_seed`，并比较 report 与 registry 的结构化内容。
- 不删除旧 evidence；需要长期保留时按提交或日期复制到新的 record 文件。
