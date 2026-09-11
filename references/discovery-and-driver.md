# Discovery、Cluster Decomposition 与 Market Driver

## 目的

这一阶段只解决两件事：

1. 昨夜真正被资金交易的是什么；
2. 什么Driver最能解释这种价格与产业扩散。

Discovery追求High Recall。不要因为某条线索暂时没有Core级证据、没有单一公司公告或不在固定关注清单中就停止研究。

## Two-Pass Discovery

重大事件Recall由两条在Theme形成前分开的发现路径负责。不要先形成Theme，再要求同一个搜索过程证明自己没有遗漏。

### Pass A：Blind Event Sweep

必须先执行；此时不得使用当前Theme、A股候选或Market Radar已形成的价格叙事来限定搜索范围。目标是发现隔夜窗口内足以显著改变公司盈利/现金流、行业供需/价格、监管准入、跨境贸易、技术路线或关键客户/Capex预期的新增事件。

至少覆盖三类发现入口：

1. 已排期和突发的重大公司/行业事件：财报、电话会、订单、并购、产品/路线、Capex、供需/价格/库存变化；
2. 政府/监管/政策Delta：新增规则、禁限、准入、审批、清单、贸易与产业政策变化；
3. 权威媒体/行业组织的跨行业高材料性扫描，并追到一级/官方来源验证。

政府/监管/政策Delta的发现必须先执行至少一次**blank-slate discovery**：查询只围绕时间窗口和事件类型开放搜索，不得包含任何预设机构名、当前Theme或A股候选。只有开放搜索已经产生具体线索后，才允许用该线索对应的机构、公司或域名做定向追查与一级来源验证。具名主体不得作为Blind Sweep的预选清单、固定起点、市场Universe或完成分母；扫描中出现的新机构、新行业和新主体同等处理。

Blind Event Sweep先产生`Event Leads`。High Materiality事件验证后进入Independent Material Event Ledger；没有价格簇也不能因此删除。未完成上述blank-slate监管发现动作时，不得宣告Pass A完成。

### Pass B：Market Radar

Event Sweep完成后，再独立从市场行为出发：

- 大幅上涨/下跌与盘前盘后异常；
- 高Dollar Volume、Relative Volume、Abnormal Return；
- 行业ETF、同行、上下游和产业代理的同步扩散；
- 当前Event Leads无法解释的异常价格/成交集群。

Market Radar产生`Market Leads`。不能因为Pass A已经找到几个强事件，就用它们替代价格扫描；也不能因为没有共同新闻就把Strong Cluster直接写成Unresolved后停止。

### Merge：两套Leads之后才形成Theme

只有Pass A和Pass B都完成后，才合并Event Leads与Market Leads，做Cluster Decomposition、Driver Hypothesis和Event–Theme Join：

- Event强 + 价格确认：优先验证是否为Theme Driver；
- Event强 + 价格弱/反向：保留Event，研究Event–Price Divergence；
- 价格强 + Event不明：继续查Industry Trend/Repricing、Continuation和替代解释；
- 两边都弱：降低优先级。

### Independent Material Event Ledger

Event Radar维护独立事件账本。每条高材料性事件至少记录：

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

事件账本与Theme Ranking分开：有独立价格/同行扩散且Driver成立可成为`Theme Driver`；合理影响多个Theme但共同因果未证实则记`Cross-theme Driver Candidate`并标`supporting/possible`；材料性高但没有形成Top Theme记`Event-only`；主要改变宏观风险环境记`Macro Context`。同一事件已在Theme正文引用，不构成从Material Event Ledger删除它的理由。

## Search Sufficiency 与 Discovery Gate

`search_scope`只描述数据可得性：

- `sufficient`：关键数据检查已完成，缺失项不太可能改变主要Theme判断；
- `partial`：重要数据缺失，可能漏Theme或改变Driver置信度；
- `unavailable`：关键市场或事件数据不可取得。

`partial`不等于报告无效；它要求降低相应结论置信度并披露可能漏掉什么。

`discovery_gate`只约束研究顺序，不承担“证明互联网没有遗漏”的任务：

- `passed`：Blind Event Sweep与Market Radar均已实际执行，且当前没有**已知未决**、足以改变Theme Rank或A股映射的High Materiality线索；
- `blocked`：任一Pass未执行，或仍有上述未决High Materiality线索。

`blocked`时只允许输出已确认事实、`Provisional Themes`、未决高材料性线索和阻塞原因；不得输出Final Theme Ranking、Final Trading Ranking或Core。`passed`不等于“零遗漏”，也不要求固定31家公司、13方向、监管4/4或任何机械分母。禁止声称“全量”“全部重大事件”除非数据来源确实支持。

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

最终报告通常保留3–5条`Material Events`，字段包括Event、Materiality、Role、Linked Themes、Causal Status、Primary Evidence、Observed Price Response与A-share Relevance。High Materiality且Linked Themes非空的事件不得仅因名额限制被删。事件已在Theme正文被引用仍可在此占一行；正文只需引用，不重复整段论证。

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

重大事件但主体价格反应弱时，分别输出Observed Facts、Hypotheses、Supporting/Counter Evidence与Confidence。不得直接写“市场没看懂”或“已经Price-in”。如果弹性可能在供应链，只有完成真实产业链验证后才可提高A股优先级。

## 国内信息边界

国内公告、集采、技术论文等可以帮助解释A股自身定价，标记为“国内补充催化”；海外与国内共同形成逻辑时标记“混合驱动”。它们不能倒推为海外Theme的一级证据。
