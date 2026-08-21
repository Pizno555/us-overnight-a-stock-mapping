# Trigger Evaluation Summary

评测日期：2026-08-21

评测配置：`evals/semantic_config.json`；阈值 `0.33`。

| Bucket | 通过/总数 | 通过率 |
|---|---:|---:|
| should_trigger | 8/8 | 100% |
| should_not_trigger | 8/8 | 100% |
| near_neighbor | 6/6 | 100% |

- False positives：0
- False negatives：0
- Precision：1.0
- Recall：1.0

近邻覆盖：`a-stock-trading-review`、`a-stock-evidence-research`、`a-stock-investment-analysis`、`serenity-skill`，以及无隔夜锚点的盘前核心池和A股业务验证请求。

说明：这是基于专属语义配置的本地确定性路由评测，不是外部模型盲测；未来新增真实误触发案例时应进入回归集。
