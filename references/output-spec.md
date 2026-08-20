# 每日输出结构与映射模板

完整盘前报告按编号0–17的18个模块输出；没有内容时明确写“无”，不要删除用于防漏和防错的模块。

报告开头先给审计字段：`report_generated_at`、`cutoff_at`、`timezone`、`us_session_date`、`price_source`、`adjustment_basis`、`coverage_log`、`known_data_gaps`。覆盖不足时先披露降级，再输出正文。

`coverage_log` 不得只写状态词，至少展开：

```text
Event Radar：company_watchlist fixed/dynamic/event-specific分母与checked/total、sector_registry_coverage checked/13及逐方向锚点状态、七层来源checked/total、失败项
Market Radar：Universe、eligible/scanned、五类Mover榜返回数量、movers_scanned、ETF checked/total、排除项
overall_status：不得高于较弱雷达
confidence_impact：覆盖缺口影响哪些结论
```

具体判定以 [radar-scan-coverage-contract.md](radar-scan-coverage-contract.md) 为准。

## 核心三表展示契约

完整报告必须用三张相互承接、无需读者人工解码的表展示核心结果：

1. **表1｜美股异动与催化摘要**：对应模块2，按“催化级别优先，其次产业扩散强度”排序。
2. **表2｜A股真实映射**：对应模块9，按“映射直接性与证据强度优先，其次当前阶段”排序。
3. **表3｜盘前候选分层**：在模块14之前汇总Core、Watch、Exclude，按“分层Core→Watch→Exclude；层内按交易优先级”排序。模块14–16继续给出逐只理由和条件。

三表共同规则：

- 每行重复写清该公司的`核心催化`，不得写“同上”、留空或要求读者跨行补全。
- A股公司必须同时写公司名称和证券代码。
- `催化级别`、`L级`、`E级或P级`、`Evidence`、`预期差`、`T_static`、`分层`必须分列；禁止压成类似`S/L1/P4/High/T2`的单列编码。
- 表3还必须逐行写明`维持条件`和`降级/排除条件`；不适用或无法判断时写`Unknown`并说明原因。
- 每张表标题或表前必须写明排序口径。

表2固定列：

| 优先级 | A股公司 | 代码 | 核心催化 | 为什么相关 | 当前阶段 | 为什么不能升级 |
|---:|---|---|---|---|---|---|

`当前阶段`须展开L级、E级或P级及Evidence；“为什么不能升级”写出关键证据缺口、反证或成熟度限制，已经达到最高可支持结论时写“当前证据下无需升级”。

表3固定列：

| A股公司 | 代码 | 核心催化 | 催化级别 | L级 | E级/P级 | Evidence | 预期差 | T_static | 分层 | 维持条件 | 降级/排除条件 |
|---|---|---|---|---|---|---|---|---|---|---|---|

## 0. 宏观与流动性背景

```text
宏观风险等级：Low / Medium / High
主要变化：
- ...
对今日映射交易的影响：...
```

无显著扰动时写“无显著宏观扰动”。

## 1. 隔夜最重要结论

只保留3–8条真正重要事件；格式为“等级｜事件”，一句话说明发生了什么、为什么重要。

## 2. 美股异动与催化摘要

排序：催化级别优先，其次产业扩散强度。

| 排名 | 标的 | 涨跌 | 成交异常 | 核心催化 | 催化级别 | 产业扩散 | A股方向 |
|---|---|---:|---|---|---|---|---|

## 3. 隔夜重大事件榜

允许主体股票没有上涨的事件出现。

| 排名 | 事件 | 一级来源 | 催化等级 | 美股反应 | A股潜在影响 |
|---|---|---|---|---|---|

## 4. Unresolved Signals

列出异动标的、涨跌、成交异常、产业扩散、时间一致性、查因进度和需监控的A股方向。明确“可监控，未归因前不进入core_pool”。

## 5. Event–Price Divergence

只按 Observed Facts / Hypotheses / Evidence / Confidence 输出。无法判断写“原因未确定”。

## 6. 产业链映射

```text
海外事件 → 核心技术/产品/靶点 → 直接受益 → 一级上游 → 二级上游 → A股
```

## 7. A股 Candidate 初筛

表格前必须披露完整漏斗：

```text
初始Candidate总数：
通过Preliminary Validation：
进入Shortlist：
淘汰数量：
主要淘汰原因：
下表范围：全部Shortlist / 代表性样本
```

若下表只展示代表性候选，必须明确写“不是完整候选池”；不得用已展示行数替代初始Candidate、通过初筛和Shortlist的真实数量。

| 公司 | 代码 | 核心催化 | 产品/管线是否匹配 | 产业位置 | 基础证据 | 明显反证 | 是否进Shortlist |
|---|---|---|---|---|---|---|---|

## 8. Shortlist 深度验证

只对Shortlist展示完整10步验证的关键证据、交叉验证、反证和缺口。

## 9. A股真实映射

按“映射直接性与证据强度优先，其次当前阶段”排序，使用核心三表契约的表2。`为什么相关`中，商业化产业写环节、产品及传导关系；Biotech写靶点/平台/管线、适应症与可比性。`当前阶段`分别写L+E+Evidence或L+P+Evidence，不得混用E/P。

不得输出单一综合分。

## 10. 真映射 vs 蹭概念

真映射：商业化产业列产品、客户/验证、订单/收入、已确认事实和受益原因；Biotech列靶点/平台、管线、临床、监管、权利归属和受益原因。

疑似蹭概念：列缺失证据和为何仅是主题联想。

## 11. 产业/管线价值排序

回答催化持续时谁的基本面或管线价值最直接受益。

## 12. 交易排序

回答基于当前已知信息谁的当日风险收益更优；结合T_static、位置、涨幅、MA、RSI9、BIAS20、成交、预期差和宏观环境。

## 13. Auction Conditions

对核心候选列明竞价出现哪些状态时维持、降级或取消；盘前不伪造今日数据。

## 14. Core Pool

先按核心三表契约输出表3，汇总Core、Watch、Exclude。随后列Core Pool，0–5只；每只展开逻辑、证据、E/P、预期差、T_static、竞价条件、风险和推翻条件，不得只给压缩向量。

## 15. Watch Pool

列明是位置不合适、早期证据不足、关键客户/订单/量产/临床待确认，或未归因；必须解释为何暂不进核心。

## 16. Exclude

列出映射错误、被证伪或无实际价值者及决定性原因。

## 17. 风险与推翻条件

每个主要方向列最大风险、反向证据和逻辑失效条件。

## 盘前最终摘要

```text
【隔夜 → A股映射雷达】

数据截止：
A股交易日：

⓪ 宏观与流动性背景：
风险等级：
主要变化：
对今日交易环境影响：

① 最强催化：
催化等级：S / A / B / C

② 海外确认：
主体股：
同行：
行业ETF：
扩散强度：

③ 真正交易逻辑：
不是XXX，而是XXX。

④ Event–Price Divergence：有 / 无
Observed Facts：
Hypotheses：
Evidence：
Confidence：

⑤ Unresolved Signals：有 / 无
产业集群与查因状态：

⑥ A股最直接产业环节：
1.
2.
3.

⑦ Candidate → Shortlist：
初始Candidate总数：
通过Preliminary Validation：
进入Shortlist：
淘汰数量：
主要淘汰原因：
下表范围：全部Shortlist / 代表性样本

⑧ 产业 / 管线价值排序：
1.
2.
3.

⑨ 交易排序：
1.
2.
3.

⑩ Core Pool：
商业化：催化 / L / E / Evidence / 预期差 / T_static
Biotech：催化 / L / P / Evidence / 预期差 / T_static

⑪ Auction Conditions：

⑫ Watch Pool：

⑬ 最容易误炒：

⑭ 今日最大风险：

⑮ 推翻条件：
```

## 产业链模板

AI硬件：

```text
云厂商Capex → GPU → AI服务器 → 交换机 → 光模块 → CPO/NPO → 激光器 → 光器件 → PCB → CCL → 铜箔 → 散热 → 电源
```

半导体：

```text
终端需求 → 晶圆制造 → 半导体设备 → 半导体材料 → 零部件 → 封装 → 测试
```

存储：

```text
AI需求 → HBM/DRAM/NAND → 晶圆 → TSV/先进封装 → 材料 → 设备
```

光通信：

```text
AI集群规模 → 交换机 → 800G/1.6T → 光模块 → CPO/NPO → CW Laser → InP → FAU/DFAU → 保偏光纤 → 散热
```

创新药：

```text
海外临床/监管催化 → 靶点 → 技术平台 → 适应症 → 同靶点/同平台A股管线 → P1-P5 → 临床数据质量 → 监管路径 → 授权/商业化价值 → 真实传导的递送/CXO/耗材
```

创新药必须区分靶点、路线、适应症、阶段、可比性、权利归属和竞争数据。一个癌症药成功不等于全部创新药利好；没有收入也不等于P5或纯概念。

## 防漏与防错终检

提交前确认：双雷达均已运行；coverage_log包含Universe和checked/total且状态符合覆盖契约；Event Radar没有把价格、成交量或ETF检查计入company_watchlist.checked；重大事件未因股价不涨而丢失；未归因信号未被强行解释；时间关系和替代原因已检查；一级信源已追溯；Candidate漏斗数量和表格范围已披露；核心三表逐行写明催化和证券代码、维度分列且排序口径明确；A股产品/管线关系明确；早期线索已交叉；技术路线反证已查；位置与Price-in独立评估；9:25前未使用未来数据；Candidate先初筛再深验；商业化与Biotech使用正确成熟度模型；核心池没有凑数。
