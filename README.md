# US Overnight → A股映射雷达

版本：v1.0.0  
发行目标：OpenAI / Codex  
用途：研究支持与条件化盘前预案，不代替投资决策，不自动下单。

## 这个 Skill 做什么

本 Skill 从最新美国或全球隔夜事件、财报、监管变化、产业信号以及美股异常价格行为出发，先发现并归因海外催化，再映射到A股真实产业环节和公司，最终形成证据化的 `Core / Watch / Exclude` 候选分层。

它同时运行两套互补雷达：

- `Event Radar`：主动发现重大事件，即使相关股票没有明显上涨也保留。
- `Market Radar`：从全市场价格、成交和板块扩散中发现资金正在交易但新闻雷达可能尚未捕捉的对象。

雷达结果分为 `A∩B`、`A-B`、`B-A` 和双空。未找到可信原因的异动保留为 `UNRESOLVED SIGNAL`，在完成归因前不得进入 `core_pool`。

## 什么时候使用

只有请求同时满足以下条件时才应由本 Skill 主导：

1. 存在明确的最新海外隔夜锚点，例如美国或全球市场事件、财报、监管变化、产业信号、个股/板块/ETF异动，或者用户明确要求扫描昨夜/隔夜。
2. 目标是把该锚点映射到A股产业环节、公司、预期差或盘前候选池。

典型请求：

```text
使用 $us-overnight-a-stock-mapping 扫描昨夜海外事件与异动，完成催化归因、A股映射和盘前候选分层。
```

```text
昨夜英伟达财报上调AI网络需求，A股光模块、PCB和散热方向中谁是真受益？
```

```text
美股光通信昨夜出现集群异动但公开消息不明确，查因并给出A股监控方向。
```

## 不适用范围

本 Skill 不负责：

- 没有海外隔夜锚点的A股全市场复盘、持仓复盘或次日综合预案；这类任务属于 `a-stock-trading-review`。
- 单一A股公司的客户、订单、技术、产能或传闻专项核验；这类任务属于 `a-stock-evidence-research`。
- 完整公司研究、盈利预测、估值和长期投资分析；这类任务属于 `a-stock-investment-analysis`。
- 没有明确隔夜事件的长期产业链瓶颈扫描；这类任务属于 `serenity-skill`。
- 普通美股新闻摘要或翻译、纯行情查询、无条件荐股、自动交易和自动下单。
- 后台定时扫描、持续监控、数据库维护或自动抓取。Skill本身不内置行情数据库、付费数据源、爬虫或交易接口。

复合请求只先完成海外催化映射，再通过 `handoff_packet` 把已确认事实、候选、证据缺口和后续任务交给相邻 Skill；不会用本 Skill 越权替代完整复盘、专项核验或估值。

## 数据与时间要求

- 报告主时区为 `Asia/Shanghai`，同时记录美国东部时间对应的UTC偏移。
- 默认隔夜窗口从上一个A股交易日15:00（北京时间）开始，到报告明确的数据截止时间结束。
- 美国休市、周末或长假必须单独说明，不能伪造常规时段行情，也不能把多日事件混写为“昨夜”。
- 任务依赖当日信息，执行环境需要具备联网检索及适用的行情数据能力。
- 来源优先级为：公司/监管/交易所/政府/法定文件 → 市场数据与行业组织 → 权威媒体 → 聚合行情或二级研究 → 市场讨论线索。
- 市场讨论只提供线索，不能作为事实证据。来源冲突未解决时输出 `Unknown`。
- 9:25前不得使用尚未形成的A股竞价或盘中数据；9:25后使用真实竞价数据时必须标注时间戳。

详细口径见 [data-and-metrics-contract.md](references/data-and-metrics-contract.md)。

## 可审计扫描覆盖

完整运行必须输出 `coverage_log`。没有明确的 `universe`、`total` 和 `checked` 时，覆盖状态最高只能是 `partial`。

### Event Radar

公司扫描分母拆为：

- 固定31家公司；
- `dynamic_watchlist`：运行前已知的重点Biotech、财报日历、重大会议和政策窗口主体；
- `event_specific_additions`：扫描过程中发现的新主体。

三者按公司或法定主体去重后形成 `active_watchlist`，分别记录分母、实际检查数、一级信源检查数和失败项。

Event Radar还覆盖13个Radar Registry方向：AI硬件、光通信、半导体、存储、PCB/CCL、先进封装、机器人、创新药、生物科技、新能源、有色、电力设备和商业航天。每个方向必须检查至少一个可审计的非价格型 `Discovery Anchor`，例如公司一级信源、政府/监管源、行业协会、正式大会或事件日历。ETF、行情源和涨跌榜只能辅助，不能作为某方向唯一的Event Anchor。

只有公司Watchlist、13个行业方向及关键事件来源层均达到覆盖条件时，Event Radar才能标记 `covered`。

### Market Radar

数据源支持时，默认市场宇宙为NYSE、Nasdaq和NYSE American上市的普通股及ADR，并排除OTC、权证、权利、units、优先股、封闭式基金和ETF；ETF单独扫描。

完整Market Radar至少检查：

- 涨幅Top 20；
- 跌幅Top 20；
- Dollar Volume Top 20；
- Relative Volume Top 20；
- 盘前/盘后显著异动；
- `SPY、QQQ、IWM、SOXX、SMH、XBI、IBB` 及当夜相关行业ETF；
- 公司行动、极低流动性和数据异常隔离项。

如果数据供应方无法覆盖默认宇宙，必须写出实际支持的Universe并降级，不能沿用“全量扫描”表述。

完整规则及13行业默认锚点见 [radar-scan-coverage-contract.md](references/radar-scan-coverage-contract.md)。

## 分析流程

执行顺序如下：

```text
双雷达发现
→ 交叉分类与催化归因
→ 公司事件/产业事件判断
→ S/A/B/C催化评级
→ 产品、技术、靶点或平台拆解
→ A股 Candidate初筛
→ Shortlist
→ 10步Deep Validation
→ L级 + E级或P级 + Evidence
→ 同行比较、反证和推翻条件
→ 预期差 + T_static + Auction Conditions
→ 产业/管线价值排序 + 当日交易排序
→ Core / Watch / Exclude
```

强事件但价格反应弱时使用 `Event–Price Divergence`：分别输出 Observed Facts、Hypotheses、Evidence 和 Confidence。无法确认原因时写“原因未确定”，不能强行解释为“已经Price-in”或“市场没看懂”。

## A股映射与验证

产业映射使用：

- `L1`：直接生产对应产品，或拥有真正可比的靶点、平台或管线。
- `L2`：明确受益的核心上游。
- `L3`：间接受益或传导链较长。
- `L4`：仅技术名词、研发规划或市场联想。

全部Candidate先做快速初筛，只对Shortlist执行完整10步验证：

1. 公司官方披露
2. 交易所和监管资料
3. 订单与客户验证
4. 技术与资质验证
5. 产业景气数据
6. 财务和经营交叉验证
7. 同行横向对比
8. 反证与风险检查
9. 研究和媒体
10. 市场讨论

商业化产业使用 `E1–E5` 描述业务兑现阶段；创新药/Biotech使用 `P1–P5` 描述管线成熟度。Evidence独立标记为 `High / Medium / Low / Unknown`。P级不是成功概率，Evidence也不能被产品或管线成熟度替代。

详细规则见 [a-share-validation.md](references/a-share-validation.md)。

## 交易定位与候选池

Skill分别输出产业/管线价值排序和当日交易排序，不使用单一综合分。每个候选采用多维向量：

```text
催化S/A/B/C
映射L1-L4
成熟度E1-E5或P1-P5
Evidence
预期差
T_static T1-T5
Auction Conditions
```

`T_static` 只使用盘前已经存在的数据。MA5/10/20/60、Wilder RSI9和BIAS20可由 [compute_indicators.py](scripts/compute_indicators.py) 按统一复权口径计算；技术指标只用于执行位置，不能证明产业逻辑、客户、订单或管线真实性。

- `core_pool`：0–5只，允许为空；L4、E5、Evidence Low/Unknown和T4/T5等关键缺陷不能被其他维度补偿。
- `watch_pool`：逻辑存在但证据、节点、归因、预期差或股价位置尚不满足核心门槛，必须说明暂不进入核心池的决定性原因。
- `exclude`：映射错误、产品不匹配、业务被证伪、路线相反、核心证据失效或公司独立事件没有合理A股映射。

竞价部分只提供条件式预案，不预测尚未发生的竞价；具体规则见 [trading-and-pools.md](references/trading-and-pools.md)。

## 输出内容

完整盘前报告包含编号0–17的18个模块：

0. 宏观与流动性背景
1. 隔夜最重要结论
2. 美股异动与催化摘要
3. 隔夜重大事件榜
4. Unresolved Signals
5. Event–Price Divergence
6. 产业链映射
7. A股Candidate初筛
8. Shortlist深度验证
9. A股真实映射
10. 真映射 vs 蹭概念
11. 产业/管线价值排序
12. 交易排序
13. Auction Conditions
14. Core Pool
15. Watch Pool
16. Exclude
17. 风险与推翻条件

报告同时包含生成时间、数据截止、时区、美国交易日、价格来源、复权方式、公司行动检查、`coverage_log` 和 `known_data_gaps`。窄请求可以只输出相关模块，但不能跳过它所依赖的归因和验证步骤。

完整模板见 [output-spec.md](references/output-spec.md)。

## 当前验证状态与证据边界

截至2026-08-20，公开发行版v1.0.0已有：

- 路由测试22例：should-trigger 8/8、should-not-trigger 8/8、near-neighbor 6/6；该结果来自现有测试集，不代表长期真实误触发率。
- 静态输出对照6例：现有断言中Skill输出通过率100%、基线0%；这是recorded fixture断言评测，不是独立模型或实盘收益证明。
- 5个真实历史事件的交互式模型回放来自公开发行前的本地开发版本；本次只收紧输出与覆盖口径，没有把旧回放冒充重跑。
- 指标脚本已通过65日样例、Python编译和帮助接口检查。
- OpenAI目标包验证和临时目录安装模拟通过；Review Studio当前为 `review`、阻塞项0。

当前仍缺少：独立provider-runner日志、精确模型/token记录、人工盲审裁决、完整全市场扫描分母，以及长期漏报率、错映射率和交易价值记录。因此本 Skill不能声称已经证明实盘有效，也不能把静态测试写成真实投资表现。

详见 [validation-summary.md](reports/validation-summary.md) 和 [runtime-replay-summary.md](reports/runtime-replay-summary.md)。

## 文件结构

```text
SKILL.md                    运行入口与核心约束
agents/openai.yaml         OpenAI/Codex界面元数据
references/                路由、数据、雷达、验证、交易和输出规范
scripts/compute_indicators.py
evals/                     路由、静态输出和历史回放材料
reports/                   验证、信任、分发及Review Studio报告
manifest.json              版本、所有者、发行目标和回滚边界
```

原始设计以字节一致的 `file-backed fixture` 保存在 [source-design-v1.0.md](references/source-design-v1.0.md)。文件标题为v1.0，正文末尾包含v1.3修正规则；版本关系与条款映射见 [source-traceability.md](references/source-traceability.md)。

## 许可

Copyright (c) 2026 simplelove. All rights reserved.
