---
name: us-overnight-a-stock-mapping
description: 当主问题同时包含最新美国或全球隔夜事件、财报、监管、产业信号或美股异常行为，以及A股产业或公司映射需求时，执行双雷达、催化归因、真实性验证和盘前Core/Watch/Exclude筛选。不用于无海外锚点的A股复盘或持仓预案（a-stock-trading-review）、单一A股消息核验（a-stock-evidence-research）、完整基本面或估值（a-stock-investment-analysis）、长期瓶颈扫描（serenity-skill）、普通新闻摘要、纯行情或自动交易。
metadata:
  version: "1.0.0"
  short-description: "隔夜催化归因与A股盘前映射"
---

# US Overnight → A股映射雷达

## 路由与启动

只主导“海外隔夜事件/异动 → 归因 → A股映射 → 条件候选池”。先执行 [routing-and-handoffs.md](references/routing-and-handoffs.md)；无明确海外锚点时不触发。复合请求仅做海外映射，其余交接。

开始前标明报告时间、时区、数据截止、隔夜窗口及A股交易日；节假日/跨周末须说明。9:25前禁用尚未形成的今日竞价或盘中数据；9:25后使用真实竞价须标时间戳。必须检索最新资料，技术问题优先一级/官方来源，结论附近给出可追溯出处。扫描前读取 [data-and-metrics-contract.md](references/data-and-metrics-contract.md)；实时数据缺失须披露并降级为 `partial`/`Unknown`，不得以估算冒充观察值，也不自动交易。

## 强制执行链

按以下顺序执行，不得跳过归因直接找A股：

```text
Event Radar + Market Radar
→ A∩B / A-B / B-A / 双空分类
→ 催化归因与可信度
→ 公司事件 / 产业事件
→ S/A/B/C催化评级
→ 产品、技术、靶点或平台拆解
→ A股 Candidate
→ Preliminary Validation
→ Shortlist
→ 10步 Deep Validation
→ L级 + E级或P级 + Evidence
→ 同行比较 + 反证 + 推翻条件
→ 预期差 + T_static + Auction Conditions
→ 产业/管线价值排序 + 交易排序
→ core_pool / watch_pool / exclude
```

宏观仅进入 `macro_risk_pool`，修正风险偏好，不替代产业催化。

## 必读参考

完整雷达读取：

1. [routing-and-handoffs.md](references/routing-and-handoffs.md)：触发、边界与交接。
2. [data-and-metrics-contract.md](references/data-and-metrics-contract.md)：窗口、降级与指标口径。
3. [radar-scan-coverage-contract.md](references/radar-scan-coverage-contract.md)：Universe、分母、Top榜与覆盖判定。
4. [radars-and-attribution.md](references/radars-and-attribution.md)：双雷达、交叉分类、背离与归因。
5. [a-share-validation.md](references/a-share-validation.md)：映射、初筛、10步深验与L/E/P/Evidence。
6. [trading-and-pools.md](references/trading-and-pools.md)：非补偿门槛、预期差、T_static、竞价与三类池。
7. [output-spec.md](references/output-spec.md)：0–17共18个模块、摘要及产业链模板。

窄模块仍须读取上游参考；交易排序前必须完成归因和A股验证。

确定性指标优先使用 [compute_indicators.py](scripts/compute_indicators.py)；输入不合格时输出 `Unknown`，不得心算或替换口径。

## 最低研究纪律

- Event Radar与Market Radar必须同时运行，并报告Universe、分母、实际扫描量；Watchlist与13方向Discovery Anchor未达覆盖契约时最高为 `partial`。
- 雷达追求High Recall，验证追求High Precision；媒体用于发现/交叉验证，市场讨论仅作线索。
- 异动至少检查时间对应、同行/ETF扩散、一级信源和替代解释；`UNRESOLVED SIGNAL` 归因前不得进 `core_pool`。
- 按参考执行背离、Candidate→Preliminary Validation→Shortlist、10步深验及L/E/P/Evidence分离；假设和间接证据不得冒充事实。
- 每个核心方向都要主动找反证并给出可操作的推翻条件。
- 产业/管线价值排序与当日交易排序必须分开。
- 不使用单一总分；输出多维决策向量，未知维度写 `Unknown`。
- `core_pool` 0–5只，采用非补偿门槛，允许为空、禁止凑数；技术指标只定执行位置，不证明业务逻辑。
- 核心结果必须按 [output-spec.md](references/output-spec.md) 的三表契约分别展示海外催化、A股真实映射和盘前候选分层；不得把催化、L/E/P/Evidence、预期差和T_static压成单个编码列。

## 完成标准

完整结果按 [output-spec.md](references/output-spec.md) 覆盖18个模块；证据不足时保留 `Unknown`、空池或未归因状态，不为完整感编造确定性。

源设计、版本解释、`input_files`、`output contract` 与 `rollback boundary` 见 [source-traceability.md](references/source-traceability.md)。

回归与回放见 `evals/`；静态fixture、交互回放和provider runner证据必须分开计量，升级后重跑。
