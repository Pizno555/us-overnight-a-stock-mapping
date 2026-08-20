# Output Risk Profile

## 高风险失效模式

| 风险 | 自检与修复 |
|---|---|
| 数据源不完整却声称全量扫描 | coverage_log必须包含Universe、checked/total、Mover榜和ETF分母；无分母最高partial，并降低置信度 |
| 非核心行业发生重大事件但价格未进榜 | 13个Radar Registry方向分别检查非价格Discovery Anchor；缺任一方向或只看ETF/涨跌榜时Event Radar最高partial |
| Watchlist固定与动态主体混算导致分母漂移 | 固定31家、dynamic_watchlist、event_specific_additions分别记分母，按法定主体去重后再计算active total |
| 把价格异动强行归因 | 使用A∩B/A-B/B-A；未归因保持UNRESOLVED SIGNAL |
| 与其他A股Skill抢路由 | 只在“海外隔夜锚点+A股映射”同时存在时主导；复合任务输出handoff_packet |
| 概念联想冒充真实映射 | Candidate先初筛，仅Shortlist执行10步深验；必须给反证和推翻条件 |
| 9:25前使用未来数据 | 只允许T_static + Auction Conditions；真实竞价必须带时间戳 |
| Biotech被错误套用收入模型 | 强制使用P1-P5，并核验适应症、路线、阶段和权利 |
| 指标口径漂移 | 使用data-and-metrics-contract及compute_indicators.py；输入不足输出Unknown |
| 报告过长掩盖关键结论 | 先给3-8条重点和盘前摘要；无内容模块明确写“无”而不填充噪声 |

## 发布前终检

检查数据截止、时区、覆盖率、来源层级、归因置信度、L/E或P/Evidence、双排序、核心池门槛、反证、推翻条件和竞价时序。任何关键字段无法验证时保留 `Unknown`。
