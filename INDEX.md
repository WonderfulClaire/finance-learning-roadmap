# 📑 目录索引 · Index

> 仓库入口页。想系统学就从 M00 按顺序读；想找某个工具/概念直接跳对应章节。

## 🚀 入口
- **[README（中文）](README.md)** · **[English README](README_EN.md)** — 项目总览、课程大纲、工具箱
- **[交互式计算器 index.html](index.html)** — 浏览器里直接算复利/通胀（GitHub Pages 可托管）
- **[30 天打卡计划](30天打卡计划.md)** — 一天一主题，周末复盘
- **[实战案例](examples/)** — 真实数据 + 工具复现，可当作练习册
- **[分享图](assets/share-card.png)** — 扫码直达仓库，适合发朋友圈/小红书/即刻

---
## 📚 课程（建议顺序）

| # | 文档 | 一句话 | 配图 |
|---|---|---|---|
| M00 | [启航：为什么理财与防坑](docs/00-启航-为什么理财与防坑.md) | 复利 vs 通胀、买前必想三问、六大坑 | [通胀侵蚀](assets/inflation-erode.svg) |
| M01 | [资产地图与工具箱](docs/01-资产地图与工具箱.md) | 钱能去哪、五类资产、三桶管理 | [资产配比](assets/asset-allocation.svg) |
| M02 | [现金与固收](docs/02-现金与固收.md) | 货基 / 存款 / 债券基金怎么挑 | — |
| M03 | [指数基金入门](docs/03-指数基金入门.md) | 为什么普通人从指数开始 + 真实持仓体检 | [三类工具对比](assets/fund-types.svg) |
| M04 | [主动基金与股票入门](docs/04-主动基金与股票入门.md) | 主动 vs 指数、股票赚什么钱 | — |
| M05 | [资产配置与定投](docs/05-资产配置与定投.md) | 股债搭配、定投、再平衡 | [风险阶梯](assets/risk-ladder.svg) |
| M06 | [估值指标与择时](docs/06-估值指标与择时.md) | PE / PB / 百分位怎么看 | — |
| M07 | [进阶：财报与量化初探](docs/07-进阶-财报与量化初探.md) | 三张财报表 + Python 算指标 | — |
| M08 | [保险与养老税务](docs/08-保险与养老税务.md) | 先守后攻、个人养老金 | — |

## 🧰 工具（tools/，零依赖）

| 文件 | 用途 | 关键参数 |
|---|---|---|
| [compound_interest.py](tools/compound_interest.py) | 复利 & 定投终值 + 72 法则 | `--principal --monthly --years --rate` |
| [inflation_impact.py](tools/inflation_impact.py) | 通胀侵蚀购买力 | `--amount --years --inflation` |
| [asset_allocation.py](tools/asset_allocation.py) | 按年龄/风险给股债现金配比 | `--age --risk --amount` |
| [pe_percentile.py](tools/pe_percentile.py) | 算当前 PE 在历史的分位 | `--current --history` |
| [fund_compare.py](tools/fund_compare.py) | 两只基金费率/收益对比 | 见 `--help` |

## 🧪 实战案例（`examples/`）

| 案例 | 文档 | 练什么 | 工具 |
|---|---|---|---|
| 01 基金体检 | [01-基金体检实战.md](examples/01-基金体检实战.md) | 真实基金对比 + 持仓诊断 | `fund_compare.py` |
| 02 复利滚雪球 | [02-复利滚雪球实战.md](examples/02-复利滚雪球实战.md) | 复利曲线 + 通胀侵蚀 | `compound_interest.py` + `inflation_impact.py` |
| 03 资产配置 | [03-资产配置实战.md](examples/03-资产配置实战.md) | 目标配比 + 估值分位 | `asset_allocation.py` + `pe_percentile.py` |

- 数据集：[examples/data/sample-portfolio.csv](examples/data/sample-portfolio.csv)

## 🖼️ 图示（assets/）

- [roadmap.svg](assets/roadmap.svg) — 五阶段九课总路线图
- [asset-allocation.svg](assets/asset-allocation.svg) — 稳健型资产配比甜甜圈
- [inflation-erode.svg](assets/inflation-erode.svg) — 名义 vs 实际购买力（30 年）
- [risk-ladder.svg](assets/risk-ladder.svg) — 风险阶梯：收益越高波动越大
- [fund-types.svg](assets/fund-types.svg) — 指数 / 主动 / 个股对比卡
- [qrcode.svg](assets/qrcode.svg) — 仓库二维码
- [share-card.png / share-card.svg](assets/share-card.png) — 社交分享图（含二维码）

## 📘 参考
- [术语表](docs/glossary.md) — 一看就懂的理财黑话
- [延伸书单与资源](docs/resources.md) — 书、App、数据源
- [CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) · [LICENSE](LICENSE)

---
⚠️ 免责声明：本仓库仅供学习，不构成投资建议。
