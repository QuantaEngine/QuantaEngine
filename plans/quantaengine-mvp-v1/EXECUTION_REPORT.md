# QuantaEngine MVP v1 方案执行说明

## 1. 执行目标

本轮执行把原始方案中的概念设计转化为一个可安装、可配置、可验证、可重复运行的多尺度有效宇宙生成器。输入为基础常数、有效粒子参数、宇宙学参数和尺度因子；输出为验证、粒子、原子、核、宇宙学、恒星、结构、复杂性，以及 Markdown/JSON 总报告。

主管线为：

```text
YAML config
-> Pydantic schema and inheritance
-> physical consistency validation
-> effective particle spectrum
-> hydrogen and chemistry window
-> light nuclei window
-> FLRW background
-> stellar window
-> structure and planet window
-> complexity indicators
-> UniverseReport
```

## 2. 执行范围

已完成原方案阶段 0 到 11，以及第一轮任务 A 到 O。完整 QFT 推导、BBN 网络、恒星演化、N-body、化学网络、生命模拟和文明 agent 属于 V2 到 V6，不以占位实现伪装为完成。

## 3. 关键工程决策

### 3.1 保留旧原型并新增主管线

仓库原有 `quantaengine` 包是标量场格点原型。为避免破坏已发布 API，新实现使用 `quanta_engine` 包和 `quanta` CLI，旧包继续接受回归测试。

### 3.2 配置继承而不是复制完整宇宙

标准宇宙提供完整字段，变体通过 `inherit` 和深合并只覆盖变化参数。加载器检测循环、未知字段和缺失字段，保证新方案失败得足够早且错误明确。

### 3.3 用有效理论分层而不是跨尺度暴力模拟

每一层只消费配置或上一层报告。非致命物理失败返回结构化 warnings 和 false 窗口，主管线继续生成完整报告；schema 错误才阻止配置加载。

### 3.4 解释原初振幅阈值

配置中的 `primordial_amplitude` 是功率振幅。结构窗口使用其平方根作为扰动幅度，再与原方案的 `1e-7` 到 `1e-3` 阈值比较，因此标准值 `2.1e-9` 能产生约 `4.58e-5` 的有效扰动。

### 3.5 分数是可行性指标

化学分数由氢能标和长度标组成，生命窗口由化学门控，文明窗口再由生命窗口门控。所有分数限制在 `[0, 1]`，不解释为生命或文明出现概率。

## 4. 分阶段完成结果

| 阶段 | 完成内容 | 主要输出 |
|---|---|---|
| 0 | 包、CLI、安装元数据、README、CI | `quanta --version` |
| 1 | Pydantic schema、继承、深合并、单位 | `UniverseConfig` |
| 2 | 错误、告警、评分、量纲和密度预算 | `ValidationReport` |
| 3 | 七种有效粒子和导出方法 | `ParticleSpectrum` |
| 4 | 约化质量 Bohr 模型和化学窗口 | `AtomicReport` |
| 5 | 氘、氦-4、氢和重元素种子判断 | `NuclearReport` |
| 6 | FLRW 积分、年龄和 200 点膨胀历史 | `CosmologyReport` |
| 7 | 聚变、寿命和重元素窗口 | `StellarReport` |
| 8 | 结构、星系、行星和稳定轨道窗口 | `StructureReport` |
| 9 | 六类复杂性指标和定性结论 | `ComplexityReport` |
| 10 | 主管线、Markdown/JSON、CLI | `UniverseReport` |
| 11 | 参数扫描、比较、CSV/PNG/Markdown | 扫描产物 |

详细文件级映射见 [TRACEABILITY_MATRIX.md](TRACEABILITY_MATRIX.md)。

## 5. 物理与数值验收

标准宇宙的参考结果：

| 指标 | 结果 | 验收范围 |
|---|---:|---:|
| 氢结合能 | 13.5983 eV | 13.0 到 14.0 eV |
| Bohr 半径 | 5.2947e-11 m | 5.0e-11 到 5.6e-11 m |
| 宇宙年龄 | 13.8029 Gyr | 10 到 20 Gyr |
| 恒星寿命 | 1.0e10 年 | 大于 1.0e9 年 |
| 生命窗口 | 约 0.9997 | 大于 0.5 |

失败型宇宙证明主管线不会只会生成成功案例：

- `no_stable_atoms_universe`：`alpha > 1`，稳定氢为 false，生命和文明窗口为 0，仍生成完整 invalid 报告。
- `strong_gravity_universe`：引力尺度为 100，恒星寿命降至 `1.0e6` 年，长寿恒星窗口关闭。
- `no_perturbations_universe`：原初功率为 0，结构、星系和行星窗口关闭。

## 6. 验证层级

1. 单元测试验证换算、公式、阈值和错误分支。
2. 集成测试验证相邻层之间的数据契约。
3. E2E 测试验证配置到报告和磁盘产物。
4. CLI 测试验证用户入口。
5. 扫描测试验证参数变化产生可解释差异。
6. Ruff、格式检查、Mypy 和 `pip check` 验证工程质量。
7. GitHub Actions 在 Python 3.11、3.12、3.13 上重复 pytest、标准宇宙生成和 manifest 场景验收。

## 7. 交付物

- 源码：`src/quanta_engine/`
- 配置：`configs/`
- 测试：`tests/`
- 示例：`examples/`
- 可复现报告：`reports/`
- 物理边界：[../../docs/physics_assumptions.md](../../docs/physics_assumptions.md)
- 完成矩阵：[../../docs/MVP_COMPLETION.md](../../docs/MVP_COMPLETION.md)
- 自动验收：[execution/run_acceptance.py](execution/run_acceptance.py)

## 8. 已知限制

- 粒子谱来自配置，不由作用量自动推导。
- 核稳定性只覆盖轻核符号级判据。
- 恒星、结构和复杂性使用显式 toy heuristics。
- 未进行参数不确定性传播或观测拟合。
- 扫描是独立样本，不是贝叶斯后验或全局敏感性分析。

这些限制是本方案边界，不是隐藏缺陷。迭代时应优先替换单层模型并保持报告契约稳定。
