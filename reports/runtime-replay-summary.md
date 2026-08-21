# Runtime Replay Summary

日期：2026-08-20  
当前公开版本：v1.0.0  
历史交互回放基线：v1.2.0  
覆盖率开发基线：v1.2.1  

以下5项回放属于历史开发证据，本次发行未把旧回放冒充重跑。

## 证据边界

- 5个案例均使用真实历史日期和可追溯网页来源，由当前Codex交互会话实际检索并生成输出。
- `execution.kind=model`，但不是Yao provider runner或独立模型盲测；精确模型ID、token和自动runner日志不可用。
- 回放只证明关键决策约束在这些案例中得到执行，不证明雷达完成全市场扫描，也不证明长期漏报率。
- 所有案例的覆盖状态均保守标记为 `partial` 或适用的 `not_applicable`。

| Case | 类型 | 关键结果 | 交互式模型回放 | Provider runner | 人工盲审 |
|---|---|---|---|---|---|
| Moderna 2026-08-19 | Biotech重大事件 | 区分肿瘤mRNA；Core为空 | Pass | Pending | Pending |
| Blackwell 2024-03-18 | 强事件弱价格 | 保持背离假设边界 | Pass | Pending | Pending |
| 光通信 2026-05-19 | 无共同一级催化集群 | UNRESOLVED；Core为空 | Pass | Pending | Pending |
| Soho House 2024-12-19 | 单一公司异动 | 并购事件不宽泛映射 | Pass | Pending | Pending |
| Good Friday 2024-03-29 | 无常规交易时段 | 不伪造行情；Core为空 | Pass | Pending | Pending |

## 当前结论

真实案例回放由0个增加到5个，说明Skill在本次交互执行中能守住归因、Biotech、公司/产业事件、休市和空核心池边界。由于缺少独立provider runner、完整扫描分母和人工盲审，这些结果不能替代长期运行证据，也不应写成“真实有效率100%”。
