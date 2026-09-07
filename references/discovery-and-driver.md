# Discovery、Cluster Decomposition 与 Market Driver

## 目的

这一阶段只解决两件事：

1. 昨夜真正被资金交易的是什么；
2. 什么Driver最能解释这种价格与产业扩散。

Discovery追求High Recall。不要因为某条线索暂时没有Core级证据、没有单一公司公告或不在固定关注清单中就停止研究。

## Broad Overnight Scan

同时运行两类扫描：

### Market Radar：从价格出发

先看资金行为，再看新闻解释。优先获取可用范围内的：

- 大幅上涨/下跌与盘前盘后异常；
- 高Dollar Volume、Relative Volume、Abnormal Return；
- 行业ETF与同行扩散；
- 同行、上下游、产业代理在相近时间的同步行为。

不能只看涨幅榜，也不要求为了形式完整必须拿到某个固定Top20榜单。数据拿不到时披露缺口，并判断它是否会实质影响“是否可能漏掉重要Theme”。

### Event Radar：从事件出发

主动找可能改变产业、公司经营或市场预期的新增信息：

1. 公司一级信源、财报、电话会、SEC或法定披露；
2. 政府、监管、交易所、正式政策；
3. 产业协会、价格、供需、缺货、扩产、交期、Capex、订单、认证、技术路线；
4. 权威媒体用于发现和交叉验证，并追原始来源；
5. 市场讨论只作线索。

可设置`priority seeds`提高常见高价值节点的召回，例如：AI/云厂商/半导体/存储/光通信龙头及FDA、BIS、DOE、SEMI等关键监管或产业入口。它们只是搜索起点，不是市场Universe，也不形成固定31家公司、13方向之类的硬分母；扫描中出现的新行业必须同等处理。

### Independent Material Event Ledger

Event Radar维护一个独立事件账本，防止Theme机制变强后反而漏掉重大公司/监管事件。事件进入账本看**材料性**，不要求先有价格集群。优先检查：

- 隔夜窗口内已排期的高影响财报、电话会、监管决定和重大产品/资本开支节点；
- 对市场/产业有系统影响力的龙头公司出现的新披露、并购、指引、订单、路线变化；
- FDA/BIS/DOE/SEC等监管政府机构，以及SEMI等与当夜异动行业匹配的组织；
- 宽市场或权威媒体扫描中新出现、但不在预设seeds里的高材料性事件。

高材料性事件定义：若属实，足以显著改变公司盈利/现金流、行业供需/价格、监管准入、技术路线或关键客户/Capex预期。

每条高材料性事件至少记录：

```text
Event
Timestamp / A股上一交易日是否已知
Materiality
Primary Evidence
Role: Theme Driver | Cross-theme Driver Candidate | Event-only | Macro Context
Linked Themes
Causal Status: confirmed | supporting | possible | none
Observed Price Response
A-share Relevance
```

事件账本与Theme Ranking分开：

- 有独立价格/同行扩散且Driver成立 → 可以成为某个Theme的`Theme Driver`；
- 同一事件合理影响多个Theme、但无法证明是共同主因 → 记`Cross-theme Driver Candidate`，逐Theme标`supporting/possible`，不得写成confirmed common catalyst；
- 材料性高但没有形成Top Theme → 记`Event-only`；
- 主要改变宏观风险环境 → 记`Macro Context`；
- 只是普通新闻、轻微评级或弱社媒线索 → 不为填表保留。

**同一事件已在Theme正文被引用，不构成从Material Event Ledger删除它的理由。** 账本负责事件完整性，Theme负责市场资金行为；两者允许交叉索引。

## Search Sufficiency

目标不是证明“互联网全部扫完”，而是达到足以支持研究结论的搜索充分性。

完整盘前研究至少应具备：

1. 一次宽市场异常扫描；
2. 一次独立重大事件扫描，同时覆盖已排期高影响事件和扫描中新出现的高材料性事件；
3. 对每个进入Top Themes的集群做同行/上下游/ETF扩散验证；
4. 对每个Top Theme追至少一种适配的一级/官方或高质量产业来源；
5. 检查Material Event Ledger中的高材料性事件是否都完成Role / Linked Themes / Causal Status登记；无论是否已被Theme引用，都不能因“避免重复”而漏掉；
6. 明确会影响结论的关键数据缺口。

用`search_scope`说明：

- `sufficient`：上述关键检查已完成，缺失项不太可能改变主要Theme判断；
- `partial`：缺失可能导致漏掉Theme或改变Driver置信度的重要数据；
- `unavailable`：关键市场或事件数据不可取得。

`partial`不等于报告无效；它要求降低相应结论置信度和披露可能漏掉什么。禁止声称“全量”“全部重大事件”除非数据来源确实支持。

## Cluster Decomposition

发现宽泛集群后必须检查是否包含经济机制不同的子集群。

错误示例：

```text
半导体上涨
```

正确思路可能是：

```text
存储价格/供需重新定价
光互连需求/网络升级
前道设备Capex/出货
```

拆分依据包括：产品、客户、需求来源、供给约束、技术路线、受益环节、价格发生时间和ETF/同行扩散。只有共同Driver足以解释主要成员时才合并；不能因为都属于“AI”或“半导体”就压成一个Theme。

## Market Theme记录

每个重要Theme至少写：

```text
Theme:
Theme Rank:
Observed Market Cluster:
Driver Type: Discrete Catalyst | Industry Trend/Repricing | Continuation | Mixed | Unresolved
Driver Hypothesis:
Catalyst Grade: S/A/B/C/N/A
Driver Confidence: High/Medium/Low/Unknown
Supporting Evidence:
Counter Evidence:
Alternative Explanations:
Why this cluster moves together:
A-share transmission candidates:
```

Theme Rank先回答“昨夜什么最重要”，综合考虑市场扩散、事件/产业重要性、新鲜度、与A股可传导性和替代解释，不做线性总分。

## Event–Theme Join 与 Material Events

Driver Validation后做一次双向Join：

1. **Event → Theme**：每条High Materiality事件是否影响一个或多个Theme？关系是confirmed、supporting、possible还是none？
2. **Theme → Driver**：每个Top Theme的主要解释来自离散Event、Industry Trend/Repricing、Continuation还是Mixed？不能为了给Theme找新闻而强配事件。

最终报告最多保留3–5条`Material Events`：

```text
Event:
Materiality: High | Medium
Role: Theme Driver | Cross-theme Driver Candidate | Event-only | Macro Context
Linked Themes:
Causal Status:
Primary Evidence:
Observed Price Response:
A-share Relevance: direct | indirect | weak/none | needs-check
```

选择优先级看材料性、跨Theme影响范围和对A股研究价值，不按“一级证据最容易获得”排序。优先保留：①High Materiality且Linked Themes非空的Theme Driver/Cross-theme Driver Candidate；②High Materiality且对A股有直接/间接意义的Event-only；③必要Macro Context。通常3–5条，但第一类不得仅因名额限制被删。事件已在Theme正文被引用仍可在此占一行；正文只需引用，不重复整段论证。

这张表只防漏和表达层级，不参与Theme Rank竞争；不能把报告重新变成“重大新闻榜”，也不能把`possible`关系写成已确认因果。

## Driver研究退出条件

### 有离散事件

检查：发布时间与价格时序、同行/ETF扩散、一级信源、替代解释。事件本身用S/A/B/C评级，`Driver Confidence`单独表示它是否真正解释价格。

### 没有单一离散事件

不能自动写Unresolved。先检查：

1. 公司级新增事件；
2. 行业供需、价格、订单、库存、Capex或需求变化；
3. 同行、上下游、ETF/行业指数扩散；
4. 至少两种替代解释，如宏观Beta、空头回补、拥挤交易、技术反弹、个别公司行为；
5. 是否存在已有硬信息的Continuation/Repricing。

满足以下任一情况才允许结束：

- **Credible Driver**：形成具体Driver，能解释主要成员及扩散结构，并有多源支持，反证/替代解释不足以推翻；
- **Unresolved - researched**：上述检查完成，但多个解释仍势均力敌，无法形成主导Driver；
- **Unknown - insufficiently checked**：必要检查尚未完成。

“行业景气不错”“AI需求强”“市场情绪好”等泛化表述不能作为研究完成条件。

## Event–Price Divergence

重大事件但主体价格反应弱时，分别输出：

1. Observed Facts；
2. Hypotheses；
3. Supporting/Counter Evidence；
4. Confidence。

不得直接写“市场没看懂”或“已经Price-in”。如果弹性可能在供应链，只有完成真实产业链验证后才可提高A股优先级。

## 国内信息边界

国内公告、集采、技术论文等可以帮助解释A股自身定价，标记为“国内补充催化”；海外与国内共同形成逻辑时标记“混合驱动”。它们不能倒推为海外Theme的一级证据。
