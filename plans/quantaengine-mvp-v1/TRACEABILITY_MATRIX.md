# 需求追踪矩阵

本矩阵把原始方案阶段映射到当前实现、自动测试和交付证据。路径均相对于仓库根目录。

| 阶段/任务 | 实现 | 测试 | 证据 |
|---|---|---|---|
| 0 / A | `pyproject.toml`, `src/quanta_engine/cli.py`, `README.md` | `tests/test_cli.py` | `quanta --version` |
| 1 / B-C | `core/schema.py`, `core/units.py`, `configs/` | `test_config_schema.py`, `test_units.py` | 配置继承和换算测试 |
| 2 / D | `validation/` | `test_validation.py` | validation JSON/Markdown |
| 3 / E | `fields/particles.py`, `fields/spectrum.py` | `test_particles.py` | 标准报告粒子表 |
| 4 / F | `atomic/hydrogen.py`, `atomic/chemistry_window.py` | `test_atomic.py` | 13.5983 eV, 5.2947e-11 m |
| 5 / G | `nuclear/stability.py`, `nuclear/bbn.py` | `test_nuclear.py` | 氘和氦-4 稳定标志 |
| 6 / H | `cosmology/friedmann.py`, `thermal_history.py` | `test_cosmology.py` | 13.8029 Gyr, 200 点历史 |
| 7 / I | `stars/fusion.py`, `lifetime.py`, `stellar_scaling.py` | `test_stars.py` | 标准与强引力寿命 |
| 8 / J | `structure/halos.py`, `galaxies.py`, `planets.py` | `test_structure.py` | 无扰动场景关闭结构 |
| 9 / K | `complexity/` | `test_complexity.py` | 六类 `[0,1]` 分数 |
| 10 / L-M | `pipeline.py`, `core/result.py`, `cli.py` | `test_e2e_universe.py`, `test_cli.py` | `reports/standard.*` |
| 11 / N | `experiments/scan.py`, `compare.py`, `sensitivity.py` | `test_scan.py` | `reports/scan_*` |
| O | `.github/workflows/tests.yml`, `docs/`, `examples/` | 全量测试与 Actions | CI 成功、示例成功 |

## 横向要求

| 要求 | 实现证据 | 防回归证据 |
|---|---|---|
| 输入 schema | Pydantic `extra=forbid` | 缺字段、未知字段和继承循环测试 |
| 输出 schema | dataclass reports + `UniverseReport` | JSON 解析和字段断言 |
| 单位检查 | `core/units.py`, `core/dimensions.py` | 已知常数往返测试 |
| 边界检查 | validation + 各层 warnings | 负质量、负密度、超临界 alpha 测试 |
| 非致命失败 | pipeline 始终组装报告 | 三类失败宇宙 E2E |
| 不过度声称 | 报告尾注和物理假设文档 | 文档审计 |
| 参数可解释性 | compare/scan 输出 delta 和曲线 | alpha/gravity 扫描测试 |

机器可读阈值以 [PLAN_MANIFEST.yaml](PLAN_MANIFEST.yaml) 为准，最近证据以 [records/acceptance-evidence.json](records/acceptance-evidence.json) 为准。
