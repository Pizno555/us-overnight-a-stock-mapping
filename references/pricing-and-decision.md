# A股上一交易日定价、预期差与今日决策

## 目的

这一阶段把“海外Theme + A股真实映射”转换成真正有盘前价值的判断：

> A股已经交易了多少？哪里还有预期差？谁基本面最好？谁今天风险收益最好？

## A-share Prior Pricing：Expectation Gap的必经步骤

对每个Top Theme先研究上一A股交易日的定价，再研究个股。

### Theme-level Pricing

至少回答：

- 对应A股板块/行业上一交易日涨跌与相对大盘强弱；
- 该Theme最近5/10/20日是否已明显提前交易；
- 是领涨、抗跌、补跌、拥挤释放还是结构破坏；
- 海外最新信息相对A股收盘新增了什么；
- 海外与A股方向不一致时，更可能是时间差、估值/拥挤、资金结构、基本面差异还是海外短线技术因素。

### Candidate-level Pricing

比较Theme内主要候选：

- 谁最抗跌/最强；
- 谁跌得最多但基本面未破坏；
- 谁已经提前大涨或严重偏离；
- 谁的相对强弱与基本面纯度一致/背离；
- 哪些位置提供赔率，哪些位置只提供胜率，哪些中间状态不值得交易。

数据不足时写Unknown，不用“没涨”直接推导高预期差。

## Expectation Gap

基于以下乘积式思考，而不是线性打分：

```text
已验证的海外Driver
× 海外价格/扩散确认
× A股上一交易日与近期定价
× A股公司真实受益与兑现
× 新信息尚未Price-in的程度
```

输出High / Medium / Low / Unknown，并说明为什么。

- High：Driver重要且证据较强，A股此前定价明显不足，且没有决定性反证；
- Medium：已有部分反映或存在分歧；
- Low：信息已广为人知/价格已充分反映，或盈利传导有限；
- Unknown：缺少可靠价格、预期或证据。

## 三种排序不得混淆

### 1. Theme Ranking

在Discovery阶段已固定，回答“昨夜市场什么最重要”。后续不得因为某只A股Evidence更高而重写Theme Rank。

### 2. Fundamental Ranking

Theme内部回答“Driver持续时谁的产业/管线价值最直接”。参考L、E/P、Evidence、盈利/管线弹性、同行优势和反证。

### 3. Trading Ranking

允许跨Theme排序，回答“今天谁的风险收益最好”。参考Theme Rank、Expectation Gap、T_static、近期涨幅、位置、宏观和板块联动。

如果较低Theme Rank的个股在Trading Ranking更靠前，必须说明原因，例如A股未Price-in、位置更优或最高Theme已过度拥挤。不能用一个100分总分替代三套排序。

## T_static

只使用集合竞价结束前已存在的数据：上一交易日MA5/10/20/60、RSI9、BIAS20、成交、近期涨幅、板块强弱和海外风险环境。

- T1：静态位置较优；
- T2：位置尚可，需要竞价/开盘确认；
- T3：等待；
- T4：过热/加速/偏离大，高风险；
- T5：结构破坏或风险收益明显不合适。

指标按[data-and-metrics-contract.md](data-and-metrics-contract.md)和脚本计算。T_static不证明业务真实性。

## Auction Conditions

Auction只决定**今天是否执行**，不决定Core资格。

9:25前只写条件预案；9:25后有真实数据才更新，并标时间戳。

生成条件前比较current_price与MA5/10/20/60、previous high/low：

- 当前已经低于某均线：只能写“重新收复并站稳”作为升级/维持条件；
- 当前高于某均线：才可写“跌破且无法收回”作为降级条件；
- 数据Unknown：不用该指标编阈值。

真实9:25竞价**不得**成为Core的必要资格门槛。

## Core / Watch / Exclude

### Core

0–5只，允许为空，不凑数。

Core需要同时满足：

- Theme/Driver已经形成可信解释；`Unresolved - researched`或`Unknown - insufficiently checked`不得进Core；
- L1/L2；
- 商业产业E1/E2优先，少数高置信E3；Biotech P1/P2优先，P3视数据；
- Evidence High，或实际满足非常强多源链；Evidence Low/Unknown不得进Core。非常强多源链至少同时具备：产业Driver有适配的官方/行业证据，海外Theme到A股具体产品/管线的传导成立，A股业务/客户/订单/收入或临床阶段有公司/交易所/监管/客户/供应商侧依据，且没有未解决的决定性反证；
- 同行、反证、推翻条件完成；
- T_static不是T4/T5。

对于没有离散Catalyst、但属于Industry Trend/Repricing或Continuation的Theme，只要`Driver Confidence=High`、产业证据链扎实、扩散结构吻合且A股映射/兑现满足上述门槛，可以进入Core；不得因为`Catalyst Grade=N/A`机械排除。

### Watch

逻辑明确但证据/兑现/位置尚不足；早期E3/E4、P3/P4；强Theme但A股Price-in较多；或未归因集群。

Core为空但存在重要Theme时，列Watch前3–5个最高优先级观察对象和排序依据，不新增第四Pool。

### Exclude

映射错误、蹭概念、业务被证伪、路线相反、公司独立事件无合理A股传导、决定性反证成立。

## 非补偿原则

禁止单一线性总分。输出多维向量：

```text
Theme Rank
Driver Type / Confidence
Catalyst Grade（适用时）
L
E或P
Evidence
Expectation Gap
T_static
Pool
```

关键缺陷不能由其他维度补偿。正文若已经判断“证据不足Core/严格应降Watch”，最终Pool必须一致。

## 完整输出：6模块

### 1. 昨夜最重要Market Themes + Material Events

主表至少包含：Theme Rank、市场集群、Driver、Driver Type、Catalyst Grade（适用时）、Driver Confidence、为什么重要、A股潜在方向。

主表后增加一个很短的`Material Events`表（没有则写“无额外高材料性事件”），通常3–5条。它不只收“Theme之外”的事件：已经作为一个或多个Theme的Driver/Supporting因素被引用的高材料性事件，也应在这里保留一行做交叉索引。High Materiality且`Linked Themes`非空的事件不得仅因表格名额限制被删，必要时可以超过5条。

字段至少包括：Event、Materiality、Role（Theme Driver / Cross-theme Driver Candidate / Event-only / Macro Context）、Linked Themes、Causal Status（confirmed / supporting / possible / none）、一级/官方证据、价格反应、A股相关性。

`Cross-theme Driver Candidate`不能自动写成共同催化剂；只有逐Theme的时序、扩散与产业证据支持时才可标confirmed。该表只负责事件完整性与层级表达，不能与Theme Rank混成一个排行榜。

宏观风险背景放在表前1–3句话，只写会影响映射交易的显著变化。

### 2. Driver证据与反证

对Top Themes写Supporting Evidence、Counter Evidence、Alternative Explanations，以及为什么这个Driver能/不能解释集群。Unresolved/Unknown在这里明确。

### 3. A股产业链与真实映射

按Theme分组展示Candidate漏斗和Shortlist。每个Top Theme先给一行`Economic Chain Coverage`，说明主要经济节点哪些已覆盖、哪些无合格A股、哪些仍待核验，并标记`Omission Challenge: passed / needs-check`；只有节点集合经过物理/技术依赖与经济价值流两条独立反查后才可写passed。然后再展示公司表。表格至少包含：公司/代码、Theme Rank、L、E/P、Evidence、为什么相关、关键缺口/反证。

### 4. A股上一交易日定价与Expectation Gap

先写Theme-level Pricing，再写主要候选相对强弱；给Expectation Gap及理由。国内补充催化在这里或模块3显式标注。

### 5. Fundamental Ranking 与 Trading Ranking

先按Theme给产业/管线价值排序，再给跨Theme的今日交易排序。若两者顺序不同，解释原因。

### 6. 今日决策

一张表汇总：公司/代码、Theme Rank、Driver、L、E/P、Evidence、Expectation Gap、T_static、Core/Watch/Exclude、维持条件、降级/排除条件。

随后简短列：

- Core 0–5；
- Watch前3–5；
- 最大风险与Theme/个股推翻条件；
- Auction Conditions（9:25前为条件式）。

## 终检

提交前确认：

- 是否先回答了“昨夜真正交易什么”；
- Material Event Ledger中的高材料性事件是否完成Role/Linked Themes/Causal Status登记；已在Theme正文出现的事件是否仍有事件层交叉索引，且possible关系没有被写成confirmed因果；
- 是否把宽泛集群拆成不同产业机制；
- 无单一公告时是否仍允许形成可信Industry Trend/Repricing Driver；
- Theme Rank是否在A股Evidence出现后仍保持为市场层结论；
- Candidate是否按经济节点展开；Coverage Gate前是否执行了Omission Challenge，确认不是“模型漏列节点但自称全部covered”的假闭环；是否存在“找到几只龙头就停”的过早收缩；
- E/P/T_static是否严格分工；
- 是否真正研究A股上一交易日板块与个股定价后才给Expectation Gap；
- 是否完全没有单一总分；
- Core资格与Auction执行是否分层；
- 当前价与均线条件是否状态一致；
- 国内信息是否清楚标注来源边界；
- Core可以为空，但真正的Top Themes和高优先Watch不能消失。
