# Radar Scan Coverage Contract

本契约定义雷达“扫了什么”和何时允许标记 `covered`。它不要求建设数据库或固定爬虫，但要求每次完整运行给出可复核的扫描宇宙、分母、实际检查数量和失败项。

## 通用规则

- `covered` 只表示按本契约声明的宇宙完成扫描，不表示互联网绝对无遗漏。
- 没有 `universe`、`total` 和 `checked` 时，状态最高只能是 `partial`。
- 搜索引擎结果页、新闻摘要或少数已知标的行情不能单独支持 `covered`。
- 同一对象重复出现在多个来源时按对象去重；来源检查数和对象检查数分开记录。
- 任何访问失败、延迟、付费墙、索引滞后或时区缺口都进入 `failed_or_missing`。
- `not_applicable` 必须说明原因，不能用于掩盖未扫描。

## Event Radar覆盖

### company_watchlist

`active_watchlist` 为 [radars-and-attribution.md](radars-and-attribution.md) 所列31家固定Watchlist，加上运行前已知的 `dynamic_watchlist`，以及扫描中发现的 `event_specific_additions`。三者按公司或法定主体去重；动态项不得回填成固定项以凑分母。

`company_watchlist.checked`只计算已实际检查至少一个适用的公司一级信源或法定披露入口的主体。股票价格、涨跌幅、成交量、ETF、板块行情或Mover榜检查全部属于Market Radar，不能计入`company_watchlist.checked`或`primary_source_checked`，也不能提高Event Radar覆盖率。报告不得用“价格已检查”“行情已覆盖”替代Event Radar的主体检查。

每次记录：

```text
company_watchlist:
  universe: fixed_31 + dynamic_watchlist + event_specific_additions
  fixed_total: 31
  dynamic_total:
  event_specific_total:
  total:
  checked:
  primary_source_checked:
  additions:
  failed_or_missing:
  status:
```

只有同时满足以下条件才可标记 `covered`：

1. `checked = total`；
2. 每家公司至少检查一个适用的公司一级信源或法定披露入口；
3. 当期新增事件主体已计入分母；
4. 失败项为0。

只查部分龙头、媒体汇总或搜索结果时标记 `partial`。

### sector_registry_coverage

Event Radar还必须主动覆盖13个Radar Registry方向，防止“事件重大但价格未进榜”被Market Radar漏掉。每个方向至少配置一个可审计的非价格型 `Discovery Anchor`；锚点可以是公司一级信源、政府/监管源、行业协会、正式大会或事件日历。ETF、涨跌榜和价格源只能辅助，不能作为某方向唯一锚点。

最低默认锚点如下；运行时可用更贴合当期事件的同等级来源替换，但必须记录名称、入口、截止时间和替换理由：

| Registry方向 | 最低Discovery Anchors |
|---|---|
| AI硬件 | NVIDIA/Broadcom公司一级信源与SEC入口；正式产品发布或财报日历 |
| 光通信 | Lumentum/Coherent/Fabrinet公司一级信源；OFC正式会议信息 |
| 半导体 | TSMC/ASML/Applied Materials公司一级信源；BIS/CHIPS或SEMI正式来源 |
| 存储 | Micron/SanDisk公司一级信源与SEC入口 |
| PCB/CCL | IPC正式产业信息；TTM Technologies公司一级信源与SEC入口 |
| 先进封装 | TSMC/Amkor/ASE公司一级信源；SEMI正式产业信息 |
| 机器人 | Teradyne/ABB/Rockwell Automation公司一级信源；IFR正式产业信息 |
| 创新药 | FDA、ClinicalTrials.gov；Merck/Eli Lilly等固定公司一级信源 |
| 生物科技 | FDA、NIH、ClinicalTrials.gov；固定Biotech与当期动态主体一级信源 |
| 新能源 | DOE/EIA；Tesla/First Solar/Enphase公司一级信源 |
| 有色 | USGS、LME/CME正式公告；当期关键矿企一级信源 |
| 电力设备 | DOE/FERC；Eaton/GE Vernova公司一级信源 |
| 商业航天 | NASA、FAA、DoD；Rocket Lab/Intuitive Machines公司一级信源与SEC入口 |

每次记录：

```text
sector_registry_coverage:
  universe: 13 registry directions
  total: 13
  checked:
  directions:
    <direction>:
      anchors_planned:
      anchors_checked:
      failed_or_missing:
      status: covered | partial | unavailable
  failed_or_missing:
  status:
```

只有13个方向全部满足“至少一个适用的非价格型锚点检查成功、锚点分母明确、失败项为0”时，`sector_registry_coverage.status` 才可为 `covered`。任一方向缺锚点、只看价格/ETF、入口失效或未检查时，本项及Event Radar整体最高为 `partial`，并列出可能漏掉的非价格事件类型。

### regulatory_and_event_sources

按实际任务声明监管和事件源清单，至少记录公司披露/SEC、FDA或ClinicalTrials、BIS/Commerce、Fed/Treasury及当期适用的政府或产业源。每一类记录 `checked/total`、查询截止时间和失败项。

七层Event Radar逐层记录：

```text
event_layers:
  company_primary: checked/total
  regulator_government: checked/total
  statutory_filings: checked/total
  industry_technical: checked/total
  earnings_calls: checked/total
  authoritative_media: checked/total
  market_discussion_leads: checked/total | not_applicable(reason)
```

一级信源、监管/政府或法定披露任一关键层没有分母，或 `company_watchlist`、`sector_registry_coverage` 任一未达到 `covered` 时，Event Radar整体最高为 `partial`。市场讨论层可为 `not_applicable`，因为它只负责提供线索。

## Market Radar覆盖

### 默认市场宇宙

数据源支持时，默认宇宙为NYSE、Nasdaq和NYSE American上市的普通股及ADR。排除OTC、权证、权利、units、优先股、封闭式基金和ETF；ETF在独立宇宙检查。SPAC普通股和明显公司行动异常标的必须单列，不与产业集群混排。

若供应方无法覆盖该宇宙，报告必须改写为它实际支持的Universe，不得沿用默认名称。

```text
market_universe:
  venue_and_security_types:
  source:
  eligible_total:
  scanned_total:
  exclusions:
  as_of:
```

### 排行与成交扫描

完整Market Radar至少扫描并记录：

- 合格宇宙涨幅Top 20；
- 跌幅Top 20；
- Dollar Volume Top 20；
- Relative Volume Top 20；
- 盘前/盘后显著异动榜；
- 因公司行动、极低流动性或数据异常被隔离的标的数量。

每张榜记录请求数量、返回数量、有效数量和交集去重后的 `movers_scanned`。无法取得Dollar Volume或Relative Volume时不得把Market Radar标为 `covered`。

### ETF与板块扩散

最低ETF宇宙为 `SPY、QQQ、IWM、SOXX、SMH、XBI、IBB`，并加入当夜重点事件对应的行业ETF。记录 `checked/total`。Sector Diffusion继续按数据契约披露分子、分母和样本构成。

只有满足以下条件，Market Radar才可标记 `covered`：

1. 市场Universe、数据源、eligible/scanned分母明确；
2. 四类Top 20及盘前/盘后榜均完成；
3. 最低ETF宇宙全部检查；
4. 公司行动和低质量异动已隔离；
5. 失败项为0。

只使用精选报价、新闻头条、搜索结果或少量ETF时，必须标记 `partial`。

## coverage_log模板

```text
coverage_log:
  event_radar:
    company_watchlist: primary_or_statutory_checked/total, primary_source_checked, status
    sector_registry_coverage: checked/13, directions, failed_or_missing, status
    event_layers: 各层checked/total或not_applicable(reason)
    failed_or_missing:
    status: covered | partial | unavailable | not_applicable
  market_radar:
    universe:
    eligible_total/scanned_total:
    movers_lists: gainers, losers, dollar_volume, rvol, premarket_afterhours
    movers_scanned:
    etf_universe: checked/total
    corporate_action_exclusions:
    failed_or_missing:
    status: covered | partial | unavailable | not_applicable
  overall_status:
  confidence_impact:
```

`overall_status` 不得高于两个核心雷达中较弱者。任一核心雷达为 `partial/unavailable` 时，报告必须列出可能漏掉的事件或异动类型，并禁止使用“全量”“全部重大事件”“没有其他机会”等表述。
