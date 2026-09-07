# 数据输入、时间窗口与指标口径

## 时间窗口

主时区统一为`Asia/Shanghai`，同时记录对应美国东部时间和UTC偏移。

默认隔夜窗口：

1. 起点为上一个A股交易日15:00（北京时间）；
2. 终点为报告明确的数据截止时间；
3. Market Radar以最近一个已完成美国常规交易时段为主体，并纳入窗口内盘前/盘后重要异动；
4. 美国休市时明确“无美国常规交易时段”，仍扫描窗口内公司、监管、宏观和全球产业事件；
5. 周末/长假按日期区分新增信息，不把多日事件混写成“昨夜”；
6. 报告截止后的事件不回写成此前已知事实。

## 数据源优先级

1. 公司、监管、交易所、政府、正式电话会或法定文件；
2. 市场数据供应方、行业组织、专业价格/产业数据；
3. 权威媒体事实报道，并继续追原始来源；
4. 聚合行情或二级研究作补充；
5. 社交媒体/市场讨论只作线索。

来源冲突未解决时写`Unknown`，不挑选最符合叙事的数据。

## Search Scope与数据缺口

完整报告开头至少写：

```text
report_generated_at:
cutoff_at:
timezone: Asia/Shanghai
us_session_date:
price_source:
search_scope: sufficient | partial | unavailable
known_data_gaps:
```

`search_scope`定义见[discovery-and-driver.md](discovery-and-driver.md)。不再要求固定31家公司、13方向或所有Top20榜全部完成才允许输出研究结论；但关键缺口可能改变Theme发现或Driver判断时必须标`partial`并降低置信度。

## 价格与成交

- 事件日涨跌、跳空和盘前/盘后异动使用对应时段未复权交易价格，并检查拆股、分红、合并、停复牌和代码变更；
- 历史收益和技术指标使用一致的前复权/总回报序列；
- `Dollar Volume`：优先`sum(price × volume)`；只有日线时可用成交量×VWAP，缺VWAP可用收盘价代理并标`proxy`；
- `Relative Volume`：已完成常规时段成交量 ÷ 前20个完整常规时段成交量中位数；
- `Abnormal Return`：个股同一时段收益减预先声明的行业ETF或同行篮子；
- `Sector Diffusion`：样本内与Driver方向一致且异常收益绝对值≥1个百分点的公司数 ÷ 有效样本数；样本<5只时只定性。

数据拿不到时写Unknown，不临时发明阈值。

## 技术指标

确定性计算使用`scripts/compute_indicators.py`：

- 输入：交易日升序UTF-8 CSV，至少`date,close`；
- MA5/10/20/60：最近N个有效交易日收盘价算术平均；
- RSI9：Wilder方法；不足10个有效收盘价为Unknown；
- BIAS20：`(close / MA20 - 1) × 100%`；
- T_static完整指标原则上至少60个有效交易日；不足则对应维度Unknown；
- 重复日期保留最后一条并记录警告；非正数/非有限close报错；不插值。

技术指标只用于执行位置，不得作为产业、客户、订单或管线真实性证据。
