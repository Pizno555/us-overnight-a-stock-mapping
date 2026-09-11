---
name: us-overnight-a-stock-mapping
description: 当用户要把最新美国或全球隔夜市场的事件、财报、监管、产业变化或异常价格集群映射到下一A股交易日时，先识别昨夜真正被资金交易的Market Themes和Drivers，再展开A股产业链、验证公司真实性、研究A股上一交易日定价与预期差，最终给出Core/Watch/Exclude和条件式执行预案。无明确海外隔夜锚点的A股复盘、单一消息核验、完整估值或长期产业扫描不由本Skill主导。
metadata:
  version: "1.1.3"
  short-description: "隔夜市场主线 → A股预期差与盘前决策"
---

# US Overnight → A股映射雷达

## 任务目标

始终围绕这一条主线工作：

```text
昨夜市场到底在交易什么
→ 为什么
→ 哪些A股产业环节真正受益
→ 谁的业务/管线最真实、兑现最好
→ A股上一交易日已经Price-in多少
→ 今天先看谁、什么条件下才执行
```

不要把任务退化成“谁最容易找到一级证据就优先研究谁”，也不要为了完成扫描、填满模板或获得更高证据等级而覆盖掉真正的市场主线。

## 启动边界

仅在同时满足以下条件时主导：

1. 有明确的最新海外/隔夜锚点：事件、财报、监管变化、产业信号、个股/板块/ETF异常行为，或用户明确要求扫描昨夜/隔夜；
2. 用户要求映射A股产业链、公司、预期差或盘前候选。

没有海外锚点的A股全市场复盘、持仓预案、单一消息真假、完整基本面/估值或长期瓶颈扫描，交给相邻Skill。本Skill在复合任务中只完成海外→A股映射部分，不需要额外生成正式handoff协议。

开始前写明：报告生成时间、`Asia/Shanghai`数据截止、最近完成的美国常规交易日、价格数据来源、`search_scope`、`discovery_gate`与关键数据缺口。9:25前不得使用尚未形成的A股竞价或盘中数据。`discovery_gate=passed`只表示两条独立Discovery Pass已执行且没有已知未决High Materiality线索，不代表“互联网已全部扫完”。

## 强制研究链

```text
① Blind Event Sweep
在任何Theme / Driver / A股候选形成前，独立扫描隔夜重大公司、行业、监管/政府与政策Delta，形成Event Leads
↓
② Market Radar
独立从价格、成交、ETF、同行/上下游异常发现Market Leads，不用Event Sweep结果替代价格扫描
↓
③ Merge + Cluster Decomposition
合并两套Leads，再把宽泛大类拆成经济机制不同的子集群
↓
④ Market Theme / Driver
为每个重要集群形成具体Driver Hypothesis
↓
⑤ Driver Validation + Event–Theme Join
Supporting Evidence + Counter Evidence + Alternative Explanations；高材料性Event登记Role/Linked Themes/Causal Status
↓
⑤b Discovery Gate
只有Blind Event Sweep和Market Radar都实际执行，且不存在已知未决、足以改变Theme Rank或A股映射的High Materiality线索，才可passed
↓
⑥ Theme Ranking
先排昨夜市场主线的重要性，不以A股个股Evidence反向改写
↓
⑦ A-share Economic Chain Expansion
先列出经济机制不同的主要受益/受损节点，再为每个重要节点找Candidate；不能找到2–5只显眼股票就提前停止
↓
⑦b Economic Chain Coverage Gate + Omission Challenge
先给节点状态，再从“物理/技术必需依赖”和“经济价值流/Capex”两条独立路径反推是否漏节点；补齐后才进入初筛
↓
⑧ Preliminary Validation → Shortlist → 10步Deep Validation
↓
⑨ L + E/P + Evidence + 同行PK + 反证/推翻条件
↓
⑩ A-share Prior Pricing
研究上一A股交易日板块与个股如何定价该Theme
↓
⑪ Expectation Gap
海外Driver × 海外价格 × A股既有定价 × 当前新增信息
↓
⑫ Fundamental Ranking / Trading Ranking
产业价值与今日风险收益分开
↓
⑬ Core / Watch / Exclude
↓
⑭ T_static → Auction Conditions
最后决定今天是否执行
```

宏观只作为风险背景，不能替代产业Driver。

## 关键概念

### Market Theme优先于个股

Theme是“昨夜资金共同交易的具体产业机制”，例如“DRAM/NAND景气重新定价”，而不是宽泛的“半导体上涨”。

- Theme Ranking在A股个股验证之前完成。
- 后续Evidence只能影响某只A股是否是真受益、是否能进入Core，不能把一个次要单事件因为证据更好而改写成昨夜第一主线。
- 最终Trading Ranking可以因A股预期差和位置让次级Theme中的个股获得更高交易优先级，但必须保留Theme Rank并说明为什么交易排序不同于市场主线排序。

### Event Radar独立保留重大事件，并与Theme交叉索引

Event Radar不是Theme Ranking的附庸。重大公司/监管/产业事件即使没有形成独立价格集群，也不能因为“已在Theme正文引用”或“没进Top Theme”而消失。

- 对已验证且足以改变公司经营、行业供需、监管路径或关键技术路线的高材料性事件，保留到独立`Material Events`账本。
- 每条Material Event标记`Role`：`Theme Driver`、`Cross-theme Driver Candidate`、`Event-only`或`Macro Context`，并列出`Linked Themes`与因果状态（confirmed / supporting / possible / none）。
- Event与Theme允许多对多：同一重大事件可以在账本中独立出现，同时在一个或多个Theme的Driver分析中被引用；这是交叉索引，不是无效重复。
- `Cross-theme Driver Candidate`只表示存在合理传导假设，不等于已证明共同催化；若缺乏价格时序、产业扩散或硬数据支持，不得写成confirmed common catalyst。
- 这些事件不因一级证据更容易取得就自动升级为Market Theme；Market Theme仍必须由价格/成交/产业扩散和Driver解释支持。
- 事件若只有公司自身影响且没有合理A股传导，可以保留事实，但A股映射写“弱/无直接映射”。
- 正常情况下只保留最重要的3–5条；但High Materiality且与Top Theme存在Linked Themes的事件不得因“名额已满”而删除，必要时可超过5条。避免恢复成新闻摘要。

### Two-Pass Discovery：先发现，再归因

重大事件Recall依靠两条在Theme形成前分开的发现路径，而不是Theme形成后的自我证明：

- **Blind Event Sweep**先做，目标是发现足以改变公司经营、行业供需/价格、监管准入、跨境贸易、技术路线或关键Capex的新增事件；搜索不能以当前Theme、A股候选或已知价格主线为起点。
- 政府/监管/政策Delta必须先执行至少一次**blank-slate discovery**：查询不得包含预设机构名、当前Theme或A股候选；只有开放搜索已经产生线索后，才允许按具体机构、公司或域名做定向追查。具名主体不能替代开放发现扫描，也不是完成分母。
- **Market Radar**再独立从价格/成交/ETF/同行扩散发现异常集群；即使Event Sweep没有找到共同新闻，也不能停止。
- 两套Leads合并以后才允许形成Theme / Driver。

`search_scope`只描述数据可得性；`discovery_gate`只约束流程边界：两条Discovery Pass均已实际执行，且没有已知未决、足以改变Theme Rank或A股映射的High Materiality线索时才可`passed`。`blocked`时只能输出已确认事实、Provisional Themes与阻塞项，不得输出Final Theme Ranking、Final Trading Ranking或Core。`passed`不等于保证零遗漏。

### Catalyst与Market Driver分开

`Catalyst`是离散新增事件，如财报、订单、批准、政策、正式涨价；使用S/A/B/C。

`Market Driver`是市场正在交易的主要原因，可以是：

- Discrete Catalyst：由新增硬事件驱动；
- Industry Trend / Repricing：供需、价格、订单、Capex、库存、需求等多项事实共同推动重新定价；
- Continuation：已有硬信息继续扩散或延迟定价；
- Mixed：多个因素共同作用；
- Unresolved：完成必要研究后仍无法形成可信主导解释。

没有单一当日公告，不等于没有可信Driver。非离散事件Theme的`催化等级`可写`N/A`，不得强行套S/A/B/C。

### Strong Cluster不是停止信号

多个经济关系紧密的同行/上下游/ETF同步异常时，必须继续查：公司新增事件、行业供需/价格/订单/Capex、扩散结构、至少两种替代解释。

真正的退出条件不是“查过四类东西”，而是：

- 已形成一个足够具体、能解释主要成员与扩散结构的Driver Hypothesis；
- 已列出支持证据、反证和替代解释；
- 或者在完成上述研究后仍无法形成主导解释，才写`Unresolved - researched`。

未完成必要研究写`Unknown - insufficiently checked`。两者都不得进入Core，但仍需展开真实A股产业链Candidate。

### Candidate展开必须达到经济链充分性

Candidate生成的退出条件不是“已经找到几只熟悉的股票”，也不是“我自己列出的节点都打了状态”，而是**重要经济节点经过遗漏反查后已经被处理**。对每个Top Theme：

1. 先按Driver列出会产生不同收入/成本/订单/资本开支传导的主要节点；
2. 每个重要节点至少完成一次A股候选搜索，并落为`covered`、`no-valid-A-share`、`not-applicable`或`needs-check`；
3. 在宣布覆盖完成前必须执行一次`Omission Challenge`，用两条彼此独立的路径重新推导产业链：
   - **物理/技术必需依赖**：Driver要真正发生，哪些核心器件、接口/控制器、材料、设备、制造/测试环节是不可缺的？复杂技术系统不能只凭模型记忆，至少查一份产品架构/BOM/标准/技术路线类可靠资料；拿不到则标`needs-check`。
   - **经济价值流/Capex**：谁因量、价、份额、库存、毛利或资本开支变化真正获得/损失经济价值？
4. 将两次反推与初始节点表比较；发现新的重要节点就补搜Candidate并重新给状态。不能因为“初始节点全部covered”就自动通过。
5. 只有遗漏反查不再产生新的重要经济节点，且继续搜索只会增加同质L3/L4弱映射时，才允许结束Candidate Generation。

禁止用“一只代表股”替代整个环节，也禁止因为已有2–5只强候选就停止。淘汰应该发生在Preliminary Validation，而不是发生在Candidate生成之前。

## 必读参考

按任务需要读取以下4个参考：

1. [discovery-and-driver.md](references/discovery-and-driver.md)：Two-Pass Discovery、集群拆分、Driver、搜索充分性与归因退出条件。
2. [a-share-validation.md](references/a-share-validation.md)：A股产业链展开、Candidate/Shortlist、10步验证、L/E/P/Evidence。
3. [pricing-and-decision.md](references/pricing-and-decision.md)：A股上一交易日定价、预期差、两套排序、三池、T_static与Auction。
4. [data-and-metrics-contract.md](references/data-and-metrics-contract.md)：时间、行情、数据降级、MA/RSI/BIAS等确定性口径。

确定性指标优先使用 [compute_indicators.py](scripts/compute_indicators.py)。输入不足写`Unknown`。

## 不可破坏的纪律

- Discovery高召回，Validation高精度。
- Event Radar必须独立保留高材料性事件；已被Theme引用也不等于可以从事件账本消失，跨Theme关联必须标注因果强弱。
- Discovery必须先执行Blind Event Sweep，再独立执行Market Radar；政府/监管Delta若未先完成一次不含预设机构名、当前Theme或A股候选的blank-slate discovery，不视为Blind Event Sweep完成。两套Leads合并前不得先形成最终Theme。任一Pass未执行，或仍有足以改变Theme Rank/A股映射的未决High Materiality线索时，`discovery_gate=blocked`，不得输出Final Theme Ranking、Final Trading Ranking或Core。
- Candidate生成必须完成重要经济节点覆盖与Omission Challenge后才允许收敛；“给自己列出的节点全部打勾”不等于覆盖完整，淘汰放在Preliminary Validation。
- 先排Theme，再在Theme内部选股；禁止把所有跨主题股票放入单一线性总分。
- 商业化公司使用E1–E5；Biotech使用P1–P5；技术位置只使用T_static，三者不得混用。
- 每个重要方向主动找反证和推翻条件。
- A股上一交易日定价是Expectation Gap的必经步骤，不能只凭“海外上涨+A股没涨”判High。
- Core/Watch/Exclude是研究分层；T_static和Auction是执行层。没有真实9:25竞价不能成为Core资格门槛。
- Evidence Low/Unknown、L4、未归因Driver、决定性反证未解决者不得进入Core。
- 可以Core为空，但不能漏掉真正的市场主线；Core为空时Watch仍按今日观察优先级给出前3–5个对象。
- 技术指标不证明产业、客户、订单或管线真实性。
- 国内信息只能标注为“国内补充催化”或“混合驱动”，不能静默提升海外Theme等级。

## 输出

完整结果按 [pricing-and-decision.md](references/pricing-and-decision.md) 的6模块输出；模块1保留一个很短的`Material Events`事件表，对高材料性事件做Role/Linked Themes交叉索引。研究过程可以复杂，用户看到的报告必须先回答主线、Driver、A股映射、预期差和今日决策，不为格式完整感重复同一结论。

回归与Golden Cases位于`evals/`。修改Skill后至少执行静态验收、边界回归和2026-09-07 Golden Case；Golden Case验证能力，不把“存储/光通信/设备”硬编码成日常答案。
