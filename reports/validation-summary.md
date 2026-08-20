# Validation Summary

日期：2026-08-20  
版本：v1.0.0  
成熟度：Production

## 结构与上下文

- Codex `quick_validate.py`：使用 `python -X utf8` 通过；Windows默认GBK直接运行会触发中文解码错误，属于验证器调用环境限制。
- Yao `validate_skill.py`：通过，无警告。
- Yao lint：通过，无警告。
- Production初始上下文：不高于1000估算tokens。
- Skill IR 2.0 schema：通过。

## 路由评测

- should-trigger：8/8。
- should-not-trigger：8/8。
- near-neighbor：6/6。
- false positives：0；false negatives：0。
- 覆盖 `a-stock-trading-review`、`a-stock-evidence-research`、`a-stock-investment-analysis`、`serenity-skill` 四个近邻边界。

## 输出评测

- 7个静态对照案例；其中file-backed 1个、near-neighbor 1个，并新增1个来自真实运行展示问题的回归案例。
- 基线通过率0%，Skill版100%，delta +100%，回归0。
- 生成6组盲审包；尚未进行人工裁决。
- 覆盖未来数据、未归因信号、Biotech成熟度、数据缺口和复合任务交接。
- 数据缺口用例已升级：必须包含Market Universe、Watchlist/Mover/ETF分母；无分母禁止标记covered。
- 新增商业航天“事件重大但价格未进榜”用例：13个行业方向缺少非价格Discovery Anchor时，Event Radar必须降级。
- Watchlist分母已拆为固定31家、dynamic_watchlist和event_specific_additions，禁止把动态主体混入固定分母。
- 新增双催化、多A股候选的核心三表回归：要求每行重复核心催化、公司名带证券代码、决策维度分列、排序口径明确，并披露Candidate漏斗和表格范围。
- Event Radar的company_watchlist.checked只认一级信源或法定披露入口；价格、成交量和ETF检查只能进入Market Radar。

## 真实历史回放

- 5个真实历史案例已完成交互式模型回放：Moderna癌症疫苗、Blackwell强事件弱价格、无共同一级催化的光通信集群、Soho House公司级并购异动、Good Friday休市空核心池。
- 5/5守住目标边界，详情见 `reports/runtime-replay-summary.md`。
- 回放不是独立provider runner或自动盲测，不能与静态fixture合并计算“100%真实有效率”。

## 脚本与信任

- `compute_indicators.py`：65日样例运行通过，MA5/10/20/60、Wilder RSI9、BIAS20无缺失。
- Trust检查：通过；1个本地CLI脚本，0个密钥发现，0个网络脚本，无第三方运行依赖。
- 治理得分80/100，达到声明的Production最低线。

## 分发与安装

- OpenAI/Codex为唯一发行目标；Claude与Generic不属于本次发行范围，不计入release gate。
- OpenAI目标包校验：通过；1/1适配器，0失败、0警告，压缩包无越界路径或嵌套Skill入口。
- 临时目录安装模拟：通过；入口、清单、界面、总览、Review Studio和零权限契约均可读取，0失败、0警告。
- 分发对象限定为OpenAI/Codex目标；未宣称Claude或Generic原生适配通过。

## missing evidence

- 已有5个交互式模型历史回放，但尚无独立provider-runner日志、精确模型/token元数据和完整市场扫描分母。
- 尚无人工盲审裁决；静态fixture不能冒充模型执行或人工评审。
- 尚无长期误触发、漏报率和映射准确率历史。

备注：Yao统一CLI在Windows读取中文子进程输出时出现编码异常；本次直接调用同一底层 `run_output_eval.py`，底层评测和报告生成均成功。
