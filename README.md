# US Overnight → A股映射雷达

版本：v1.1.2  
用途：研究支持与条件化盘前预案，不代替投资决策，不自动下单。

## 这个 Skill 做什么

本 Skill 用于把**最新美国或全球隔夜市场真正交易的主线**映射到下一 A 股交易日。

它不是简单做“海外新闻摘要”，也不是“找最容易取得一级证据的海外事件”。真正目标是：

```text
昨夜市场到底在交易什么
→ 为什么
→ 对应A股哪些真实产业环节
→ 哪些公司最直接、最能兑现
→ A股上一交易日已经Price-in多少
→ 今天先看谁，什么条件下才执行
```

核心原则：

> **先判断市场正在交易什么，再判断A股谁真正受益，再判断A股有没有预期差，最后才判断今天能不能交易。**

---

## 双雷达：同时看“发生了什么”和“资金在交易什么”

本 Skill 同时运行两套互补雷达。

### Event Radar：从事件出发

主动寻找可能改变产业、公司经营或市场预期的新增信息，例如：

- 公司财报、指引、电话会、订单、产品路线和资本开支；
- 监管、政策、审批、禁限措施；
- 行业价格、供需、库存、交期、缺货、扩产；
- 客户需求、认证、量产、技术路线变化；
- 重大临床、监管和商业化节点。

即使相关股票暂时没有明显上涨，也不能因为“价格没反应”直接忽略。

Event Radar还维护一个**独立 Material Event Ledger**：高材料性事件无论是否已经被某个Theme引用，都保留独立登记。每条事件标记`Role`、`Linked Themes`和`Causal Status`，用于区分真正Theme Driver、跨主题Driver候选、纯事件和宏观背景；事件账本不会因为一级证据更好拿就抢占Theme Rank，也不会把“可能影响多个Theme”写成已经证明的共同催化。

### Market Radar：从价格出发

先看资金行为，再寻找解释。重点发现：

- 个股、板块、ETF 的异常涨跌；
- Dollar Volume、Relative Volume、Abnormal Return 等异常；
- 同行、上下游、产业代理的同步行为；
- 盘前、盘后与常规交易时段的显著扩散。

即使暂时没有找到明确新闻，也不能因为“没有当天公告”就停止研究。

### 两套雷达如何配合

| 情形 | 含义 | 处理 |
|---|---|---|
| 事件强 + 价格确认 | 事件与市场行为互相支持 | 优先形成高置信 Driver |
| 事件强 + 价格弱/反向 | Event–Price Divergence | 研究是否已 Price-in、是否有反证或传导转移 |
| 价格强 + 事件不明 | Strong Cluster / Unresolved Trigger | 继续查供需、价格、订单、Capex、扩散和替代解释 |
| 两边都弱 | 缺少足够研究价值 | 降低优先级 |

重要：

> **Strong Cluster ≠ Stop Signal。**  
> 强价格集群但缺少单一公告，应该触发深挖，而不是直接写 `Unresolved` 后停止。

---

## 什么时候使用

只有请求同时满足以下条件时，才应由本 Skill 主导：

1. 存在明确的最新海外/隔夜锚点，例如美国或全球市场事件、财报、监管变化、产业信号、个股/板块/ETF 异常行为，或用户明确要求扫描昨夜/隔夜；
2. 目标是把这些海外变化映射到 A 股产业环节、公司、预期差或盘前候选。

典型请求：

```text
使用 $us-overnight-a-stock-mapping 扫描昨夜海外事件与异动，找出真正被资金交易的主线，并映射到A股盘前候选。
```

```text
昨夜英伟达财报上调AI网络需求，A股光模块、PCB、散热里谁是真受益？
```

```text
美股光通信昨夜出现集群异动，但公开消息不明确，继续查因并给出A股方向。
```

```text
昨夜存储、设备、光互连都有异动，拆分真正的Market Themes，再判断A股上一交易日有没有预期差。
```

---

## 不适用范围

本 Skill 不负责：

- 没有海外隔夜锚点的 A 股全市场复盘、持仓复盘或次日综合预案；
- 单一 A 股公司的客户、订单、技术、产能或传闻专项核验；
- 完整公司研究、盈利预测、估值和长期投资分析；
- 没有明确隔夜触发的长期产业链瓶颈扫描；
- 普通美股新闻摘要、纯行情查询、翻译；
- 无条件荐股、自动交易或自动下单；
- 后台定时抓取、数据库维护或自动监控。

复合任务中，本 Skill 只负责“海外隔夜 → A股映射”这一段，不需要额外生成正式 handoff 协议。

---

## 数据与时间要求

- 主时区统一为 `Asia/Shanghai`，同时记录对应美国东部时间和 UTC 偏移；
- 默认隔夜窗口从上一个 A 股交易日 15:00（北京时间）开始，到报告明确的数据截止时间结束；
- Market Radar 以最近一个已完成的美国常规交易时段为主体，同时纳入窗口内重要盘前/盘后异动；
- 美国休市、周末或长假必须明确说明，不能伪造常规时段行情，也不能把多日事件混写成“昨夜”；
- 报告截止后的信息不能回写成此前已经知道的事实；
- 9:25 前不得使用尚未形成的 A 股竞价或盘中数据；9:25 后只有取得真实数据并标注时间戳时才能更新 Auction 判断；
- 来源冲突未解决时输出 `Unknown`，不能选择最符合叙事的数据。

来源优先级：

```text
公司 / 监管 / 交易所 / 政府 / 正式电话会或法定文件
→ 市场数据 / 行业组织 / 专业价格与产业数据
→ 权威媒体事实报道
→ 聚合行情 / 二级研究
→ 市场讨论与社交媒体线索
```

市场讨论只作线索，不作事实证据。

详细口径见 [data-and-metrics-contract.md](references/data-and-metrics-contract.md)。

---

## 搜索充分性，而不是形式化“全覆盖”

本 Skill 不再要求为了形式完整，机械完成固定 31 家公司、13 个行业方向或所有 Top20 榜单后才允许输出结论。

目标是：

> **达到足以支持主要 Market Themes 和 Drivers 的搜索充分性。**

完整盘前研究至少应具备：

1. 一次宽市场异常扫描；
2. 一次独立重大事件/产业变化扫描，兼顾已排期高影响事件和扫描中新出现的高材料性事件；
3. 对每个 Top Theme 做同行、上下游、ETF/行业扩散验证；
4. 对每个 Top Theme 追至少一种适配的一级/官方或高质量产业来源；
5. 检查高材料性 Event Radar 事件是否完成独立账本登记与Event↔Theme关联；即使已在Theme正文引用也不能因“避免重复”而消失；
6. 明确会影响结论的关键数据缺口。

使用：

- `sufficient`：关键检查完成，缺失项不太可能改变主要 Theme 判断；
- `partial`：缺失可能导致漏掉 Theme 或改变 Driver 置信度；
- `unavailable`：关键市场或事件数据不可取得。

`partial` 不等于报告无效，但必须降低相应结论置信度，并说明可能漏掉什么。

---

## 完整研究流程

```text
① Broad Overnight Scan
事件 + 市场价格/成交异常 + 行业/ETF扩散
↓
② Cluster Decomposition
把宽泛大类拆成经济机制不同的子集群
↓
③ Market Theme / Driver
为每个重要集群形成具体Driver Hypothesis
↓
④ Driver Validation
Supporting Evidence + Counter Evidence + Alternative Explanations
↓
④b Event–Theme Join
高材料性Event记录Role/Linked Themes/Causal Status；Theme反查其Event/Trend/Repricing依据
↓
⑤ Theme Ranking
先排昨夜市场主线的重要性
↓
⑥ A-share Economic Chain Expansion
先拆经济机制不同的主要节点，再逐节点寻找Candidate
↓
⑥b Economic Chain Coverage Gate + Omission Challenge
先给节点状态，再从物理/技术必需依赖与经济价值流/Capex两条独立路径反推遗漏节点，补齐后才允许收敛
↓
⑦ Preliminary Validation → Shortlist → 10步Deep Validation
↓
⑧ L + E/P + Evidence + 同行PK + 反证/推翻条件
↓
⑨ A-share Prior Pricing
研究上一A股交易日板块与个股如何定价该Theme
↓
⑩ Expectation Gap
海外Driver × 海外价格 × A股既有定价 × 当前新增信息
↓
⑪ Fundamental Ranking / Trading Ranking
产业价值与今日风险收益分开
↓
⑫ Core / Watch / Exclude
↓
⑬ T_static → Auction Conditions
最后决定今天是否执行
```

宏观只作为风险背景，不能替代产业 Driver。

### 两个新的防漏门

- **Event–Theme Join**：事件和Theme是多对多关系。重大事件已经出现在Theme分析里，不代表可以从事件层消失；但“能解释多个Theme”也不代表已证明共同催化，必须标因果强弱。
- **Omission Challenge**：Economic Chain Coverage不能只检查模型自己列出的节点。宣布覆盖完成前，要从“物理/技术必需依赖”和“经济价值/Capex流”两条路径独立重建一次产业链；复杂技术系统还要至少用一份架构/BOM/标准/工艺类可靠资料校验，发现遗漏节点就补搜Candidate。

---

## Cluster Decomposition：不能把不同机制压成一个大类

发现宽泛集群后，必须判断是否包含经济机制不同的子集群。

错误：

```text
半导体上涨
```

更合理的拆法可能是：

```text
存储价格 / 供需重新定价
光互连需求 / 网络升级
前道设备 Capex / 出货
```

拆分依据包括：

- 产品；
- 客户；
- 需求来源；
- 供给约束；
- 技术路线；
- 受益环节；
- 价格发生时间；
- ETF / 同行扩散。

只有共同 Driver 足以解释主要成员时才允许合并；不能因为都属于“AI”或“半导体”就压成一个 Theme。

---

## Market Theme 与 Market Driver

### Theme 是第一等研究对象

Theme 回答：

> **昨夜资金共同交易的具体产业机制是什么？**

例如“DRAM/NAND 景气重新定价”是 Theme；“半导体上涨”通常太宽泛。

`Theme Ranking` 在 A 股个股验证之前完成。

后续 A 股 Evidence 只能决定某只公司是否是真受益、是否能进入 Core，不能把一个次要事件因为一级证据更容易获取，就反向改写成昨夜第一主线。

### Catalyst 与 Market Driver 分开

`Catalyst` 是离散新增事件，例如财报、订单、批准、政策、正式涨价。

`Market Driver` 是市场正在交易的主要原因，可以是：

| Driver Type | 含义 |
|---|---|
| `Discrete Catalyst` | 由明确新增硬事件驱动 |
| `Industry Trend/Repricing` | 供需、价格、订单、Capex、库存、需求等共同推动重新定价 |
| `Continuation` | 既有硬信息继续扩散或延迟定价 |
| `Mixed` | 多个因素共同作用 |
| `Unresolved` | 完成必要研究后仍无法形成可信主导解释 |

没有单一当日公告，不等于没有可信 Driver。

非离散事件 Theme 的 `Catalyst Grade` 可以写 `N/A`，不得为了填表强行套 S/A/B/C。

### Driver 研究退出条件

对于 Strong Cluster，真正的完成条件不是“查过四类东西”，而是至少形成：

```text
Driver Hypothesis
+ Supporting Evidence
+ Counter Evidence
+ Alternative Explanations
+ Why this cluster moves together
```

只有三种合法结束状态：

- `Credible Driver`：具体 Driver 足以解释主要成员和扩散结构；
- `Unresolved - researched`：必要检查完成，但多个解释仍势均力敌；
- `Unknown - insufficiently checked`：必要检查尚未完成。

“行业景气不错”“AI需求强”“市场情绪好”等泛化表述，不算研究完成。

详细规则见 [discovery-and-driver.md](references/discovery-and-driver.md)。

---

## 等级、指标与状态速查字典

评级是不同维度的事实标签，不是可以相加的分数。

> 催化强，不代表 A 股映射真实；  
> 映射真实，不代表业务已经兑现；  
> 业务成熟，也不代表当前交易位置适合。

关键缺陷不能被其他维度补偿。

### 一眼看懂各维度

| 维度 | 从强/直接/成熟/适宜到弱/间接/早期/高风险 |
|---|---|
| 催化等级 | `S → A → B → C` |
| A股映射 | `L1 → L2 → L3 → L4` |
| 商业化成熟度 | `E1 → E2 → E3 → E4 → E5` |
| Biotech管线成熟度 | `P1 → P2 → P3 → P4 → P5` |
| Evidence / Confidence | `High → Medium → Low → Unknown` |
| 静态交易位置 | `T1 → T2 → T3 → T4 → T5` |

注意：`E/P` 数字越小表示越成熟，`T` 数字越小表示盘前静态风险收益越合适。

### 催化等级 S/A/B/C

只用于**离散 Catalyst 本身的重要性**。

| 等级 | 含义 | 常见例子 |
|---|---|---|
| `S` | 产业级硬催化，可能明显改变路线、需求、供给或盈利预期 | 正式批准、III期关键成功、超大订单、龙头严重超预期、Capex大幅上调、重大短缺或政策变化 |
| `A` | 高价值产业信号，传导路径较明确 | 明确产品路线、需求大增、量产、大客户验证、价格显著上涨、多家公司上调预期 |
| `B` | 一般催化，价值或验证程度有限 | 行业会议、中小订单、一般管理层表态、单家研究观点 |
| `C` | 弱催化或噪声 | 单独评级、社媒传闻、无来源截图、无原因小盘暴涨、单一KOL观点 |

对于 `Industry Trend/Repricing`、`Continuation` 等没有单一离散事件的 Theme，可以写 `N/A`。

### Driver Confidence

回答：

> **当前 Driver 是否真的能解释海外市场异动？**

| 等级 | 含义 |
|---|---|
| `High` | 多源证据、时间关系和扩散结构高度一致，替代解释较弱 |
| `Medium` | 主要证据相互支持，但时间、扩散或替代解释仍有缺口 |
| `Low` | 证据链较弱，存在明显替代解释 |
| `Unknown` | 无法可靠判断 |

Driver Confidence 与 A 股公司的 `Evidence` 是两个不同概念。

### A股映射等级 L1–L4

| 等级 | 含义 |
|---|---|
| `L1` | 直接生产对应产品，或拥有真正可比的靶点、平台或管线 |
| `L2` | 核心上游/下游，Driver 持续会明确改变其需求或盈利 |
| `L3` | 间接受益、弹性有限或传导链较长 |
| `L4` | 只有技术名词、规划、研发项目或市场联想 |

`L4` 不得进入 Core。

### 商业化成熟度 E1–E5

`E` 只描述已有产品、材料、设备、器件、服务等商业化产业的业务兑现阶段，不用于创新药临床阶段。

| 等级 | 含义 |
|---|---|
| `E1` | 已有显著收入、利润或订单 |
| `E2` | 订单、产能或收入快速增长 |
| `E3` | 已有客户验证、小批量或量产节点临近 |
| `E4` | 有真实业务基础，但尚无明确订单或规模兑现 |
| `E5` | 纯概念或未证实 |

### Biotech 管线成熟度 P1–P5

`P` 只描述创新药 / Biotech 管线成熟度，不代表临床成功概率、股价机会或证据强弱。

| 等级 | 含义 |
|---|---|
| `P1` | 已获监管批准或已经商业化 |
| `P2` | 注册阶段、III期关键成功，或 NDA/BLA 已提交/受理/进入关键审评 |
| `P3` | III期进行中、II期较强 PoC，或进入明确关键性临床阶段 |
| `P4` | IND获批、I期/I–II期，或只有初步人体安全性/有效性数据 |
| `P5` | 动物/临床前阶段、尚未人体临床、仅平台或早期布局 |

**语义锁死：商业产业只用 E；Biotech 只用 P；技术/价格位置只用 `T_static`。**

### Evidence

Evidence 回答：

> **A股映射、业务关系或管线关系得到多强的证据支持？**

| 等级 | 含义 |
|---|---|
| `High` | 公司、监管、客户/订单、临床注册或权威技术证据充分 |
| `Medium` | 多个独立来源形成相互印证 |
| `Low` | 单一间接线索或证据链不完整 |
| `Unknown` | 无法验证 |

业务本身真实，不等于“本次海外 Driver → 该 A 股公司”的 Evidence 自动为 High。

---

## A股产业链映射与 Candidate 漏斗

每个重要 Theme 先拆真实经济链，再找股票：

```text
Market Theme / Driver
→ 核心产品 / 技术 / 靶点 / 平台
→ 需求 / 价格 / 供给变化
→ 直接受益环节
→ 核心上游 / 下游
→ 设备 / 材料 / 设计 / 制造 / 模组 / 分销等适用环节
→ A股 Candidate
```

不设置固定 Candidate 数量：

- 真正相关公司少就少；
- 相关产业环节多则充分展开；
- 不允许只挑一只“代表股”代替完整经济链；
- 不允许为了凑数量加入弱映射。

Candidate阶段还有一个明确退出条件：**主要经济节点已经处理完，而不是“已经找到几只熟悉的股票”。** 对每个重要节点至少做一次A股搜索，并标记为`covered / no-valid-A-share / not-applicable / needs-check`。只有继续搜索只会增加同质或L3/L4弱映射时，才进入Preliminary Validation。

价格型 Driver 必须做双向传导。例如 DRAM/NAND 涨价，对模组/分销公司同时检查：

- 售价上涨；
- 库存收益；
- 采购成本；
- 营运资金；
- 终端需求压力。

### Candidate 漏斗

| 阶段 | 含义 |
|---|---|
| `Candidate` | 根据 Theme 和产业链拆解得到的高召回初始候选，不代表真实受益 |
| `Preliminary Validation` | 快速检查产品/管线、产业位置、基础证据和明显反证 |
| `Shortlist` | 通过初筛，值得执行完整 10 步验证的集合，不等于 Core |
| `Deep Validation` | 对 Shortlist 执行完整证据验证、同行比较、反证和推翻条件 |

---

## A股 10 步 Deep Validation

严格按照以下顺序：

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

原则：

> **先硬证据、再交叉验证、最后看观点。市场讨论只作线索。**

每个进入 Core 或高优先 Watch 的候选，都必须给出可操作的推翻条件。

详细规则见 [a-share-validation.md](references/a-share-validation.md)。

---

## A-share Prior Pricing：预期差的必经步骤

海外 Theme 映射到 A 股后，不能直接判断“利好 / 低估 / 有预期差”。

必须先研究 A 股上一交易日以及近期如何定价该 Theme。

### Theme-level Pricing

至少回答：

- 对应 A 股板块上一交易日涨跌与相对大盘强弱；
- 最近 5/10/20 日是否已经明显提前交易；
- 当前是领涨、抗跌、补跌、拥挤释放还是结构破坏；
- 海外最新信息相对 A 股收盘新增了什么；
- 海外与 A 股方向不一致时，更可能是时间差、估值/拥挤、资金结构、基本面差异还是海外短线技术因素。

### Candidate-level Pricing

比较 Theme 内主要候选：

- 谁最强 / 最抗跌；
- 谁跌得多但基本面没有破坏；
- 谁已经提前大涨或偏离过大；
- 谁的相对强弱与基本面纯度一致或背离；
- 哪些位置提供赔率，哪些位置只提供胜率，哪些处在中间状态不值得交易。

数据不足写 `Unknown`，不能用“没涨”直接推导 High 预期差。

---

## Expectation Gap

预期差回答：

> **已经验证的产业信息，与 A 股现有价格之间还剩多少未被交易？**

采用乘积式思考，而不是线性打分：

```text
已验证的海外Driver
× 海外价格 / 扩散确认
× A股上一交易日与近期定价
× A股公司真实受益与兑现
× 新信息尚未Price-in的程度
```

| 等级 | 阅读方式 |
|---|---|
| `High` | Driver重要且证据较强，A股此前定价明显不足，且没有决定性反证 |
| `Medium` | 市场已有部分反映，但兑现路径、持续性或覆盖范围仍存在分歧 |
| `Low` | 信息已广为人知、价格已充分反映，或盈利/管线传导有限 |
| `Unknown` | 缺少可靠价格、市场预期或证据 |

“没涨”不能自动判为 High，“已经上涨”也不能单独证明完全 Price-in。

---

## 三种排序：不能混成一个总分

### 1. Theme Ranking

回答：

> **昨夜市场什么最重要？**

在 Discovery 阶段固定。后续某只 A 股的 Evidence 更高，不能反向改写 Theme Rank。

### 2. Fundamental Ranking

在每个 Theme 内回答：

> **Driver 持续时，谁的产业/管线价值最直接？**

参考：

- L；
- E/P；
- Evidence；
- 盈利或管线弹性；
- 同行优势；
- 反证和推翻条件。

### 3. Trading Ranking

允许跨 Theme 排序，回答：

> **今天谁的风险收益最好？**

参考：

- Theme Rank；
- Expectation Gap；
- T_static；
- 近期涨幅与位置；
- 宏观风险；
- 板块联动。

如果较低 Theme Rank 的股票在 Trading Ranking 更靠前，必须说明原因，例如 A 股尚未 Price-in、位置更优，或最高 Theme 已过度拥挤。

**禁止使用单一 100 分总分替代三套排序。**

---

## T_static：盘前静态交易位置

`T_static` 只使用集合竞价结束前已经存在的数据，回答：

> **逻辑已经成立以后，当前静态位置是否值得等待执行确认？**

| 等级 | 含义 |
|---|---|
| `T1` | 静态位置较优，风险收益较理想 |
| `T2` | 位置尚可，需要竞价/开盘确认 |
| `T3` | 等待，位置或确认度不足 |
| `T4` | 过热、加速、偏离大或波动高；不能推出“今天适合买” |
| `T5` | 结构破坏或风险收益明显不合适 |
| `Unknown` | 缺少合格行情或指标输入 |

技术指标原则上使用至少 60 个有效交易日、口径一致的历史序列，由 [compute_indicators.py](scripts/compute_indicators.py) 确定性计算。

### 技术指标

| 指标 | 定义 | 用途 |
|---|---|---|
| `MA5/10/20/60` | 最近 N 个有效交易日收盘价算术平均 | 趋势和相对位置 |
| `RSI9` | Wilder 方法的 9 期 RSI | 辅助判断短期强弱与过热 |
| `BIAS20` | `(最新收盘价 ÷ MA20 - 1) × 100%` | 衡量相对 MA20 的偏离 |

技术指标只用于执行位置，不能证明产业逻辑、客户、订单或管线真实性。

---

## Core / Watch / Exclude

### Core

`0–5` 只，允许为空，不凑数。

常见非补偿式门槛：

- Theme / Driver 已形成可信解释；
- `Unresolved - researched` / `Unknown - insufficiently checked` 不得进入 Core；
- L1/L2；
- 商业产业 E1/E2 优先，少数高置信 E3；Biotech P1/P2 优先，P3 视数据；
- Evidence High，或实际满足非常强的多源证据链；
- Evidence Low/Unknown 不得作为高确定性 Core；
- 同行、反证、推翻条件已完成；
- T_static 不是 T4/T5。

对于没有离散 Catalyst、但属于 `Industry Trend/Repricing` 或 `Continuation` 的 Theme，只要 Driver Confidence 高、产业证据链扎实、扩散结构吻合，并且 A 股映射/兑现满足上述门槛，也可以进入 Core；不能因为 `Catalyst Grade=N/A` 机械排除。

### Watch

逻辑存在，但证据、兑现节点、预期差或交易位置暂时不足。

Core 为空但存在重要 Theme 时，Watch 仍必须明确前 `3–5` 个最高优先级观察对象及排序依据，不新增第四个正式 Pool。

### Exclude

包括：

- 映射错误；
- 蹭概念；
- 业务被证伪；
- 路线相反；
- 公司独立事件没有合理 A 股传导；
- 决定性反证成立。

---

## Auction Conditions

Auction 只决定：

> **今天是否执行。**

它不决定某只股票是否具备 Core 研究资格。

正确层级：

```text
Core / Watch / Exclude
↓
T_static
↓
Auction Conditions
↓
今日执行 / 不执行
```

9:25 前只写条件式预案；9:25 后有真实竞价数据才更新，并标注时间戳。

生成均线条件前，必须检查当前价格状态：

- 当前已经低于某均线：只能写“重新收复并站稳”作为升级/维持条件；
- 当前高于某均线：才可以写“跌破且无法收回”作为降级条件；
- 数据 Unknown：不用该指标编阈值。

真实 9:25 竞价**不得**成为 Core 的必要资格门槛。

详细规则见 [pricing-and-decision.md](references/pricing-and-decision.md)。

---

## 完整输出结构

完整盘前报告只要求 6 个模块。

### 1. 昨夜最重要 Market Themes + Material Events

先给Top Themes主表，至少包含：

- Theme Rank；
- 市场集群；
- Driver；
- Driver Type；
- Catalyst Grade（适用时）；
- Driver Confidence；
- 为什么重要；
- A 股潜在方向。

宏观风险背景放在表前 1–3 句话，只写会影响映射交易的显著变化。

主表后通常保留3–5条`Material Events`。高材料性事件即使已经作为Theme Driver或Supporting因素在正文引用，也仍可在这里保留一行做交叉索引；同时收纳没有形成Top Theme的重大事件。High Materiality且Linked Themes非空的事件不得仅因名额限制被删，必要时可超过5条。字段包括Role、Linked Themes和Causal Status，明确区分“confirmed / supporting / possible / none”。这不是重复新闻榜，而是防止跨主题重大事件被Theme正文吞掉，也防止把可能关系写成确定因果。

### 2. Driver 证据与反证

对 Top Themes 写：

- Supporting Evidence；
- Counter Evidence；
- Alternative Explanations；
- 为什么该 Driver 能或不能解释这个集群；
- Unresolved / Unknown 状态（如适用）。

### 3. A股产业链与真实映射

按 Theme 分组展示 Candidate 漏斗和 Shortlist。每个Top Theme先用一行`Economic Chain Coverage`说明主要经济节点的覆盖状态，防止Candidate过早收缩。

至少包含：

- 公司 / 代码；
- Theme Rank；
- L；
- E/P；
- Evidence；
- 为什么相关；
- 关键缺口 / 反证。

### 4. A股上一交易日定价与 Expectation Gap

先写 Theme-level Pricing，再写主要 Candidate 的相对强弱、提前定价程度、拥挤/补跌/抗跌状态，并给出 Expectation Gap 及理由。

国内信息必须显式标注为“国内补充催化”或“混合驱动”，不能静默提升海外 Theme 等级。

### 5. Fundamental Ranking 与 Trading Ranking

先按 Theme 给产业/管线价值排序，再给跨 Theme 的今日交易排序。

如果两者顺序不同，明确解释原因。

### 6. 今日决策

汇总：

- 公司 / 代码；
- Theme Rank；
- Driver；
- L；
- E/P；
- Evidence；
- Expectation Gap；
- T_static；
- Core / Watch / Exclude；
- 维持条件；
- 降级 / 排除条件。

随后简短列：

- Core `0–5`；
- Watch 前 `3–5`；
- 最大风险与 Theme / 个股推翻条件；
- Auction Conditions（9:25 前为条件式）。

研究过程可以复杂，但最终输出不需要为了审计感重复填 18 个模块。

---

## 文件结构

```text
us-overnight-a-stock-mapping/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── discovery-and-driver.md
│   ├── a-share-validation.md
│   ├── pricing-and-decision.md
│   └── data-and-metrics-contract.md
├── scripts/
│   └── compute_indicators.py
└── evals/
    ├── cases.jsonl
    ├── trigger_cases.json
    ├── validate_skill.py
    └── fixtures/
        ├── golden-case-theme-driver-regression.md
        ├── unresolved-signal-input.md
        └── indicator-test.csv
```

### 四个 Reference 分别负责什么

| 文件 | 作用 |
|---|---|
| `discovery-and-driver.md` | 双雷达、市场集群、子集群拆分、Theme/Driver、搜索充分性、归因退出条件 |
| `a-share-validation.md` | A股产业链展开、Candidate→Shortlist、10步验证、L/E/P/Evidence、同行与反证 |
| `pricing-and-decision.md` | A股上一交易日定价、Expectation Gap、三种排序、三池、T_static、Auction、6模块输出 |
| `data-and-metrics-contract.md` | 时间窗口、数据源、缺口降级、价格/成交、MA/RSI/BIAS 等确定性口径 |

---

## 修改后如何验收

修改 Skill 后至少运行：

```bash
python evals/validate_skill.py
```

该脚本检查：

- Skill 引用文件是否存在；
- 已删除旧合同是否仍有悬空引用；
- Golden / 边界 fixtures 能否通过静态断言；
- 是否重新出现单一总分；
- 是否出现 E/P/T_static 混用；
- 是否再次把 Core 资格和 Auction 层级混淆；
- 指标脚本能否在 fixture 上运行。

`evals/cases.jsonl` 保留行为级回归，用于 Codex / 客户端进行真实 model-run。

Golden Case 的目的不是把某个日期或历史答案硬编码进 Skill，而是用一个真实历史截面验证通用能力，例如：

```text
强价格集群是否被发现
→ 是否正确拆子Theme
→ 是否继续查Driver
→ 是否按重要经济节点充分展开A股Candidate，而不是找到几只龙头就停
→ Event Radar高材料性非Theme事件是否仍能保留
→ 是否保持Theme优先级
→ 是否检查A股上一交易日定价
→ 是否形成Expectation Gap
→ 是否守住Core门槛
```

---

## 当前验证边界

- `evals/trigger_cases.json`：保存路由正例、反例和近邻任务；
- `evals/cases.jsonl`：保存关键行为断言和真实 model-run 用例；
- `evals/fixtures/`：保存指标、边界和 Golden Case 输入。Golden Case 使用历史市场截面验证通用能力，日期记录在 fixture 正文/元数据中，不作为通用规则。

这些材料用于回归与防漂移，不代表已经证明实盘收益，也不代表取得长期漏报率、错映射率或独立 provider-runner 统计。

---

## 最重要的设计纪律

1. **Discovery 高召回，Validation 高精度。**
2. **Strong Unresolved 不是停止信号，而是深挖触发器。**
3. **Theme 是第一等研究对象，先排主线，再在主线内部选股。**
4. **没有单一当天公告，不等于没有可信 Market Driver。**
5. **A股上一交易日定价是 Expectation Gap 的必经步骤。**
6. **Theme Ranking、Fundamental Ranking、Trading Ranking 不能混为一个总分。**
7. **商业产业用 E，Biotech 用 P，交易位置用 T_static。**
8. **Core/Watch/Exclude 是研究分层，Auction 是执行层。**
9. **可以 Core 为空，但不能漏掉真正的 Market Themes 和高优先 Watch。**
10. **所有重要方向都要主动寻找反证和推翻条件。**
11. **Candidate生成以经济节点覆盖为退出条件，不以股票数量或熟悉度为退出条件。**
12. **Event Radar独立于Theme Ranking保留高材料性事件，但不让新闻榜反客为主。**

---

## 许可

Copyright (c) 2026 simplelove. All rights reserved.
