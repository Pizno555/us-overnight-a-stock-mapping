---
name: us-overnight-a-stock-mapping
description: 当用户的主问题明确从最新美国或全球隔夜事件、财报、监管变化、行业信号或美股异常价格行为出发，并要求映射A股产业环节或公司时，执行事件雷达与市场雷达、催化归因、A股真实性验证和盘前Core/Watch/Exclude筛选。不要用于A股全市场复盘、持仓复盘或次日综合预案（转a-stock-trading-review），单一A股公司的消息/客户/订单真假核验（转a-stock-evidence-research），完整基本面/盈利预测/估值（转a-stock-investment-analysis），无明确隔夜锚点的产业链瓶颈扫描（转serenity-skill），普通美股新闻摘要、纯行情查询或自动交易。
metadata:
  version: "1.0.0"
  source-spec: "US Overnight → A股映射雷达 Skill v1.0（含源文档末尾所列v1.3修正规则）"
  short-description: "隔夜催化归因与A股盘前映射"
---

# US Overnight → A股映射雷达

把美国隔夜市场视为A股盘前的产业催化实验室。先发现、再归因；先硬证据、再映射；先验证业绩或管线、再谈交易。

仅提供研究预案，不代替决策，不自动下单。

## 路由边界

只主导“最新海外隔夜事件/异动 → 归因 → A股映射 → 条件候选池”。先执行 [routing-and-handoffs.md](references/routing-and-handoffs.md)；没有明确隔夜海外锚点时，不因出现A股、盘前、股票池或产业链等词触发。复合请求只完成海外映射模块，其余交给对应近邻 Skill。

## 启动规则

开始前明确：

- 报告生成时间、时区和数据截止时间。
- 对应的“隔夜”交易窗口和A股交易日；节假日或跨周末时显式说明。
- 当前是否早于A股 9:25。9:25前严禁使用尚未形成的今日竞价或盘中数据；9:25后若使用真实竞价数据，标注时间戳。
- 若关键实时数据无法取得，列为数据缺口并降低结论置信度，不用估算值冒充观察值。

任务依赖当日数据，必须检索最新资料。技术问题使用一级/官方资料；A股与海外事件按来源层级引用，结论附近给出链接或可追溯出处。扫描前读取 [data-and-metrics-contract.md](references/data-and-metrics-contract.md)，并在报告中披露实际覆盖率与降级项。

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

宏观只进入 `macro_risk_pool`，修正风险偏好，不替代产业催化。

## 必读参考

执行完整盘前雷达时，依次读取并遵守：

1. [routing-and-handoffs.md](references/routing-and-handoffs.md)：主触发条件、近邻Skill边界和复合请求交接。
2. [data-and-metrics-contract.md](references/data-and-metrics-contract.md)：隔夜窗口、数据降级和指标口径。
3. [radar-scan-coverage-contract.md](references/radar-scan-coverage-contract.md)：扫描Universe、Watchlist分母、Top榜数量和覆盖状态判定。
4. [radars-and-attribution.md](references/radars-and-attribution.md)：双雷达、来源矩阵、交叉分类、背离和归因。
5. [a-share-validation.md](references/a-share-validation.md)：产业映射、Candidate初筛、10步深验、L/E/P/Evidence分级。
6. [trading-and-pools.md](references/trading-and-pools.md)：非补偿式门槛、预期差、T_static、竞价预案与三类池。
7. [output-spec.md](references/output-spec.md)：编号0–17的18个模块、摘要模板及产业链模板。

若用户只问其中一个窄模块，读取该模块参考以及它依赖的上游参考；例如只问交易排序，也必须先完成归因和A股验证，不能只读交易规则。

确定性指标优先使用 [compute_indicators.py](scripts/compute_indicators.py)；无法提供合格输入时输出 `Unknown`，不得由模型心算或用未说明口径替代。

## 最低研究纪律

- Event Radar 与 Market Radar 必须同时运行；不能只扫新闻，也不能只扫涨幅榜。
- 没有明确Universe、分母和实际扫描数量时，coverage状态最高只能是 `partial`。
- Event Radar的Watchlist与13方向Discovery Anchor须达到覆盖契约才可写 `covered`。
- 雷达阶段追求 High Recall，验证阶段追求 High Precision。
- 媒体用于发现和交叉验证，市场讨论只作线索，不作事实证据。
- 任何异动至少检查时间对应、同行/ETF扩散、一级信源和替代解释。
- `UNRESOLVED SIGNAL` 可以监控，但归因完成前不得进入 `core_pool`。
- 背离、Candidate→Shortlist、10步深验及E/P/Evidence分离按对应参考执行；假设和间接证据不得冒充结论。
- 每个核心方向都要主动找反证并给出可操作的推翻条件。
- 产业/管线价值排序与当日交易排序必须分开。
- 不使用单一总分；输出多维决策向量。无法可靠判断的维度使用 `Unknown`。
- `core_pool` 为0–5只，允许为空，禁止凑数。
- 核心结果必须按 [output-spec.md](references/output-spec.md) 的三表契约分别展示海外催化、A股真实映射和盘前候选分层；不得把催化、L/E/P/Evidence、预期差和T_static压成单个编码列。

## 完成标准

完整结果须覆盖事件、异动、归因、产业逻辑、A股真伪映射、兑现或管线价值、预期差、静态位置、竞价预案及 Core / Watch / Exclude。

如数据或证据不足以完成某项，保留 `Unknown`、空池或未归因状态；不要为完整感编造确定性。

源设计、版本解释、`input_files`、`output contract` 与 `rollback boundary` 见 [source-traceability.md](references/source-traceability.md)。

回归与回放见 `evals/`；静态fixture、交互回放和provider runner证据必须分开计量，升级后重跑。
