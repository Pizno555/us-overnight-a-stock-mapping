# 源设计追踪与版本说明

## input_files

- `references/source-design-v1.0.md`：`file-backed fixture`，来自用户提供的 `us-overnight-a-stock-mapping-v1.0.md`。
- 原文件SHA-256：`A8B9389D8AC5648D0EC14039BF83A84354FE8EED72219402850A3D5780061D88`。
- 原文件共2765行；复制件保持字节级一致，用于审计，不作为每次执行时必须全量加载的入口上下文。

## 版本说明

- 源设计标题和头部版本字段为 `v1.0`。
- 源设计末尾包含“v1.3相对v1.2”的四项修正说明，但未同步修改标题。
- 本包把源规范标记为“v1.0（含末尾v1.3修正规则）”；面向GitHub的首个公开发行版本为 `v1.0.0`（机器清单使用SemVer `1.0.0`）。公开版本号不改变源设计文件的原始版本标记。

## 条款映射

| 源设计范围 | 落地文件 |
|---|---|
| 0–18：目标、双雷达、归因、催化、产业链、L级 | `SKILL.md`、`radars-and-attribution.md` |
| 19–24：Candidate、Shortlist、10步法、E/P/Evidence、同行与反证 | `a-share-validation.md` |
| 25–31：三套排名、多维向量、T_static、竞价和三类池 | `trading-and-pools.md` |
| 32–38：每日输出、摘要和产业模板 | `output-spec.md` |
| 39–44：防漏、防错、禁止项、决策树和最终原则 | `SKILL.md`及各参考文件终检规则 |
| 工程补强：近邻路由 | `routing-and-handoffs.md`、`evals/trigger_cases.json` |
| 工程补强：数据与指标口径 | `data-and-metrics-contract.md`、`scripts/compute_indicators.py` |
| 工程补强：扫描覆盖分母、行业发现锚点与Event/Market计数边界 | `radar-scan-coverage-contract.md`、`evals/output/cases.jsonl` |
| 工程补强：核心三表与Candidate漏斗展示契约 | `output-spec.md`、`evals/output/cases.jsonl` |
| 工程补强：真实历史回放 | `evals/replay/`、`reports/runtime-replay-summary.md` |

## output contract

完整运行输出编号0–17的18个模块，并包含数据截止、coverage_log、双雷达、未归因信号、背离、Candidate漏斗、A股初筛/深验、核心三表、分列的决策维度、产业/交易双排序、Auction Conditions、Core/Watch/Exclude及推翻条件。窄请求可只输出相关模块，但不得跳过它依赖的上游验证。

## rollback boundary

回滚仅限本Skill目录。不得修改、删除或覆盖 `a-stock-trading-review`、`a-stock-evidence-research`、`a-stock-investment-analysis`、`serenity-skill`，不得更改用户行情文件或Codex全局配置。回滚公开发行v1.0.0的本次修订时，只撤销核心三表、Candidate漏斗、Event Radar checked计数边界及对应评测/报告；公开发行前的本地开发沿革用于审计，不作为GitHub版本序列。

## 变更记录

- `1.0.0`：依据源设计生成的首版个人Skill。
- `1.1.0`：收紧海外隔夜锚点路由；新增四个近邻Skill交接；定义时间、覆盖和指标口径；增加确定性指标脚本、触发/输出评测、Skill IR和Production治理元数据；统一18模块和中文UI。
- `1.2.0`：新增可审计的Radar Scan Coverage Contract；无Universe和分母时禁止标记covered；加入5个真实历史交互式回放并与provider-runner证据分开；修复源设计副本的字节级一致性；补充Windows UTF-8验证复现说明。
- `1.2.1`：为13个Radar Registry方向增加非价格Discovery Anchor覆盖契约；把模糊的mandatory_32修正为fixed_31、dynamic_watchlist与event_specific_additions三段分母；发行目标收敛为OpenAI/Codex并重新生成分发审计。
- `v1.0.0`（首个GitHub公开发行）：在上述本地开发基线之上，固定三张核心结果表及其排序、证券代码和分列展示要求；强制披露Candidate→Preliminary Validation→Shortlist漏斗及展示范围；规定Event Radar主体检查只认一级信源或法定披露入口，价格、成交量和ETF仅计入Market Radar；新增真实运行失败形态的静态回归案例。公开版本从v1.0.0起重新编号。
