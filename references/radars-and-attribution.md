# 双雷达、信息源与催化归因

## 五层目标

1. Discovery：昨夜发生了什么，防漏。
2. Attribution：市场为何异动、事件多重要，防错因。
3. Mapping：海外事件对应A股哪段产业链，防错方向。
4. Validation：哪些公司真正受益、能否兑现，防蹭概念。
5. Trading：逻辑成立后，今天的位置是否适合，防交易错误。

## Event Radar

主动扫描可能改变产业、公司经营或市场预期的事件；即使主体股未上涨也必须保留。

信息源按下列优先级使用：

1. 公司一级信源：IR、新闻稿、财报、电话会、产品公告、SEC重大披露、正式演讲、Investor Day、会议演示。
2. 监管和政府：FDA、NIH、ClinicalTrials.gov、美国商务部/BIS、CHIPS、白宫、DOE、DoD、Fed、Treasury、BLS、BEA。
3. SEC或法定披露：8-K、10-Q、10-K、6-K、并购、合同、Capex、诉讼、重组、管理层变化。
4. 产业与技术节点：行业协会、标准组织、大会、白皮书、价格、缺货、扩产、交期、认证、新产品路线。
5. 财报与电话会：Revenue、EPS、毛利率、Guidance、Capex、Backlog、ASP、库存、利用率、需求、量产和供应链变化；电话会常比EPS更有映射价值。
6. Reuters、Bloomberg、WSJ、CNBC、FT、AP等权威媒体：发现、解释和交叉验证，继续追溯原始发布者。
7. X、Reddit、Stocktwits、论坛、KOL：只作线索。

关键产业节点公司 Watchlist 至少包括：

- AI/半导体：NVIDIA、AMD、Broadcom、Marvell、Intel、TSMC、Micron、SanDisk、Applied Materials、Lam Research、KLA、ASML。
- 云厂商：Microsoft、Meta、Alphabet/Google、Amazon、Oracle。
- 光通信：Lumentum、Coherent、Applied Optoelectronics、Fabrinet、Corning。
- 创新药/Biotech固定项：Merck、Moderna、BioNTech、Eli Lilly、Novo Nordisk、Amgen、Regeneron、Gilead、Vertex。

上述固定Watchlist共31家。`dynamic_watchlist` 单列当期重点Biotech、财报日历、重大会议和已知政策窗口主体；扫描中发现的新主体进入 `event_specific_additions`。三者去重后形成 `active_watchlist`，完整运行时按 [radar-scan-coverage-contract.md](radar-scan-coverage-contract.md) 记录各自分母、`checked/total`、一级信源检查数量和失败项。没有分母时不得标记 `covered`。

重点 Radar Registry 至少覆盖 AI硬件、光通信、半导体、存储、PCB/CCL、先进封装、机器人、创新药、生物科技、新能源、有色、电力设备和商业航天。每个方向必须配置并检查至少一个非价格型 `Discovery Anchor`；公司一级信源、政府/监管源、行业协会、正式大会或事件日历均可。ETF和行情源只能辅助，不能单独支持Event Radar的 `covered`。具体锚点与分母见覆盖契约，不通过机械扩充股票数量解决。

宏观信息单列 `macro_risk_pool`。只保留显著影响A股风险偏好、成长估值或映射交易环境的变化：美债收益率、Fed预期、CPI/PCE/非农、美元指数、纳指或全球风险资产、重大流动性或地缘风险。无显著变化时明确写“无显著宏观扰动”。

## Market Radar

不先看新闻，直接寻找资金突然交易的对象。

- 个股：涨跌幅Top、盘前/盘后、跳空、瞬时拉升或跳水、成交量/额、Relative Volume、波动率。
- 板块：行业ETF、半导体、生物科技、AI、软件、光通信、核电、铜、稀土、能源、军工、机器人、医疗器械等。
- 集群：同行、上下游及ETF是否同步，异动时间是否一致。

不能只按涨幅排序，至少同时看涨跌幅、Dollar Volume、Relative Volume、Market Cap、Abnormal Return、Sector Diffusion 和事件确认。所有指标严格使用 [data-and-metrics-contract.md](data-and-metrics-contract.md) 的口径；缺失时写 `Unknown`，不得临时发明阈值。

Market Universe、Top榜数量、ETF分母和排除项遵守 [radar-scan-coverage-contract.md](radar-scan-coverage-contract.md)。只拿到精选报价、新闻头条或少数标的时，Market Radar必须标记 `partial`。

标准发现表：

| 排名 | 代码 | 公司 | 涨跌 | 成交异常 | 核心催化 | 产业扩散 | 初始A股方向 |
|---|---|---|---:|---|---|---|---|

此表只发现异常，不直接给交易结论。

## 双雷达交叉

- `A∩B`：重大事件且市场响应，作为高置信催化优先归因、区分公司/产业事件并评级。
- `A-B`：重大事件但价格反应弱，进入 Event–Price Divergence；不得默认“市场没看懂”或“已Price-in”。
- `B-A`：市场异动但没有可信事件，标记 `UNRESOLVED SIGNAL`，继续反向查因；可以形成监控方向，未归因前不得进核心池。
- 双空：忽略。

## Event–Price Divergence

严格分四段：

1. Observed Facts：事件、发布时间、来源、候选级别、主体/同行/ETF价格、量额、事件前走势。
2. Hypotheses：提前Price-in、主体盈利影响小、其他负面抵消、弹性在供应链、市场理解不足等；`Hypothesis ≠ Conclusion`，无需强选一个。
3. Evidence：逐项寻找支持与反对证据。判断Price-in时检查此前走势、市场一致预期、分析师预测、同类事件和期权/成交异动。
4. Confidence：High / Medium / Low / Unknown。无法确认时写“原因未确定”并停止定性。

重点机会形态是：S/A事件 + 主体反应有限 + 产业影响明确 + A股某上游有更高业绩弹性；必须完成产业链与A股验证后才能升级。

## 催化归因

每个重要异动至少完成：

1. 时间检查：比较消息发布时间与价格异动时间；时间不贴合时继续找原因。
2. 同行业检查：同行、上下游和ETF是否同步，用于区分公司事件与产业事件。
3. 一级信源检查：媒体说法追到公司、SEC、FDA、政府、正式电话会、客户或供应商；否则不得自动升为S/A。
4. 替代解释检查：并购、临床结果、评级变化、空头回补等是否更能解释异动。

Catalyst Confidence 使用 High / Medium / Low / Unknown，依据一级信源、时间匹配、同步扩散、多源交叉与替代解释。Unknown 不进入核心映射。

## 催化等级与事件性质

- S：产业级硬催化，如正式批准、III期成功、超大订单、龙头严重超预期、路线确定性变化、Capex大幅上调、重大短缺或实质政策变化。
- A：高价值产业信号，如明确产品路线、需求大增、量产、大客户验证、行业价格显著上涨或多家公司上调预期。
- B：一般催化，如行业会议、中小订单、一般管理层表态、单家券商观点、未完全验证变化。
- C：弱催化/噪声，如单独评级、社媒传闻、无来源截图、无原因小盘暴涨、单一KOL；原则上不进核心映射。

区分：

- Company-specific：收购、自身药物数据、诉讼、管理层变化，通常映射价值较弱。
- Industry-wide：技术路线、需求、价格、短缺、政策、龙头Capex变化，通常映射价值较高。

禁止从“某股上涨”直接跳到宽泛主题。必须先拆出具体产品、技术、靶点、平台、适应症和上下游传导。
