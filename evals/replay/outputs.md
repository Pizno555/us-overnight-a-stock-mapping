# Runtime Replay Outputs

以下为同一Codex交互会话在读取Skill并检索真实历史来源后形成的关键输出。它们是模型执行证据，但不是独立provider runner、自动盲测或全市场扫描证据。

## Case 1：Moderna癌症疫苗

- 事件：个性化mRNA肿瘤新抗原疗法Ⅲ期顶线成功，事件等级S；完整效应量和OS尚未公开。
- 市场：MRNA、MRK和生物科技ETF同向扩散，属于A∩B。
- 映射：近岸蛋白、诺唯赞具备通用mRNA上游产品证据，但没有项目级客户、订单或收入证据；沃森生物的预防性疫苗平台不能直接等同。
- 池：`core_pool为空`；近岸蛋白、诺唯赞进入watch_pool。
- 覆盖：Event Radar和Market Radar均为 `partial`，因为没有默认Watchlist与市场Universe分母。

## Case 2：NVIDIA Blackwell

- Observed Facts：NVIDIA正式发布Blackwell，AWS等主要云厂商确认采用；次日NVDA价格反应约+1.7%。
- Hypotheses：此前预期、宏观压制、事件盈利兑现期较远、产业弹性可能分布在供应链；均不是结论。
- Evidence：官方产品和客户采用支持产业意义；缺少一致预期、期权和完整事件前行情，不能证明Price-in或“市场没看懂”。
- Confidence：事件为High，弱价格原因是Unknown。
- A股：只进入产品/客户验证流程，不能仅凭Blackwell名称把所有AI硬件股放入Core。

## Case 3：光通信集群回撤

- Observed Facts：AAOI、LITE、COHR同步显著下跌；未找到时间匹配的共同一级负面公告。
- 状态：`UNRESOLVED SIGNAL`。获利回吐是低至中置信假设，不是已确认催化。
- A股：只能形成风险监控方向，不能写成光通信需求恶化，`core_pool为空`。
- 下一步：检查同一时刻成交、期权、ETF、此前涨幅、客户Capex和各公司公告。

## Case 4：Soho House收购要约

- 归因：SEC公司公告能够解释主要异动；属于company-specific并购事件。
- 映射：不能从单家公司收购溢价推导美国酒店或消费行业景气变化。
- A股：酒店、会员制消费或地产公司均不因该事件获得真实产业映射，`core_pool为空`。

## Case 5：Good Friday休市

- 交易时段：美国常规股票市场休市，Market Radar常规时段为 `not_applicable`，不得生成当日涨跌、RVOL或扩散数据。
- 事件雷达：仍应扫描隔夜窗口内公司、监管和全球产业事件；本次覆盖不足，因此Event Radar为 `partial`。
- 结论：没有被验证的合格海外产业催化，`core_pool为空`；不得用前一交易日行情冒充“昨夜异动”。
