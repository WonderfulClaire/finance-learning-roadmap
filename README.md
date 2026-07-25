<p align="center">
  <img src="assets/roadmap.svg" alt="个人理财系统学习路线" width="720"/>
</p>

<h1 align="center">📈 个人理财系统学习路线</h1>
<h3 align="center">从「复利 vs 通胀」到「资产配置 + 量化初探」，零基础也能看懂的中文开源教程</h3>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"/>
  <img src="https://img.shields.io/badge/语言-中文-ff69b4.svg" alt="Lang"/>
  <img src="https://img.shields.io/badge/课程-9%20modules-blue.svg" alt="Modules"/>
  <img src="https://img.shields.io/badge/工具-Python%20零依赖-orange.svg" alt="Tools"/>
  <img src="https://img.shields.io/github/stars/WonderfulClaire/finance-learning-roadmap?style=social" alt="Stars"/>
</p>

<p align="center">
  <b>A systematic, beginner-friendly, open-source personal-finance curriculum in Chinese.</b><br/>
  Built for people who want to <i>actually understand</i> money — not get rich quick.
</p>

<p align="center">
  🌐 <a href="index.html">在线交互式计算器</a> &nbsp;·&nbsp; 🇬🇧 <a href="README_EN.md">English README</a> &nbsp;·&nbsp; 📑 <a href="INDEX.md">目录索引</a>
</p>

---

## ✨ 这是个什么项目？

市面上的理财内容两极分化：要么满屏"年化 30%"的焦虑营销，要么是一上来就丢你一堆金融工程公式。
**这个仓库想做中间那条没人做好的路**：

> **用普通人能懂的语言，把理财的核心认知框架系统讲清楚，并配上能自己跑的计算器。**

- 🧭 **系统化**：9 节课从启航 → 基础 → 权益 → 策略 → 进阶，循序渐进
- 🧰 **可实操**：`tools/` 下 5 个零依赖 Python 工具，概念当场算给你看
- 📖 **重认知**：不荐股、不承诺收益，只帮你建立"判断框架"
- 🆓 **完全免费**：MIT 协议，随便 fork、随便改、随便教别人

> ⚠️ **免责声明**：本仓库仅供学习交流，**不构成任何投资建议**。一切数据以公开来源为准，过往业绩不代表未来。投资有风险，决策需独立判断。

<p align="center">
  <a href="https://github.com/WonderfulClaire/finance-learning-roadmap">
    <img src="assets/share-card.png" alt="分享本仓库" width="680"/>
  </a>
  <br/>
  <span style="color:#666;font-size:13px">分享图：扫码直达仓库，欢迎转发给想理财的朋友</span>
</p>

---

## 🗺️ 学习路线图

![roadmap](assets/roadmap.svg)

五阶段、九节课，建议按顺序学，每学完一节在 [`30天打卡计划.md`](30天打卡计划.md) 打勾。

### 🖼️ 配套图示

- [资产配比甜甜圈](assets/asset-allocation.svg) — 稳健型股/债/现金/另类/保障怎么分
- [通胀侵蚀曲线](assets/inflation-erode.svg) — 名义价值 vs 实际购买力（30 年）
- [风险阶梯](assets/risk-ladder.svg) — 收益越高、波动越大
- [三类工具对比](assets/fund-types.svg) — 指数 / 主动 / 个股怎么选

---

## 📚 课程大纲

| # | 模块 | 一句话 | 链接 |
|---|---|---|---|
| M00 | 启航：为什么理财与防坑 | 复利 vs 通胀、买前必想三问、六大坑 | [docs/00](docs/00-启航-为什么理财与防坑.md) |
| M01 | 资产地图与工具箱 | 钱能去哪、五类资产、三桶管理 | [docs/01](docs/01-资产地图与工具箱.md) |
| M02 | 现金与固收 | 货基 / 存款 / 债券基金怎么挑 | [docs/02](docs/02-现金与固收.md) |
| M03 | 指数基金入门 | 为什么普通人从指数开始 + 真实持仓体检 | [docs/03](docs/03-指数基金入门.md) |
| M04 | 主动基金与股票入门 | 主动 vs 指数、股票赚什么钱 | [docs/04](docs/04-主动基金与股票入门.md) |
| M05 | 资产配置与定投 | 股债搭配、定投、再平衡 | [docs/05-资产配置与定投.md](docs/05-资产配置与定投.md) |
| M06 | 估值指标与择时 | PE/PB/百分位怎么看 | [docs/06](docs/06-估值指标与择时.md) |
| M07 | 进阶：财报与量化初探 | 三张财报表 + Python 算指标 | [docs/07](docs/07-进阶-财报与量化初探.md) |
| M08 | 保险与养老税务 | 先守后攻、个人养老金 | [docs/08](docs/08-保险与养老税务.md) |

配套：📘 [术语表](docs/glossary.md) · 📚 [延伸书单与资源](docs/resources.md) · 🗓️ [30 天打卡计划](30天打卡计划.md)

---

## 🚀 快速开始

```bash
# 1. 克隆
git clone https://github.com/WonderfulClaire/finance-learning-roadmap.git
cd finance-learning-roadmap

# 2. 从 M00 开始读
#    直接打开 docs/00-启航-为什么理财与防坑.md

# 3. 跑一个工具感受复利（需 Python 3，零依赖）
python tools/compound_interest.py --principal 100000 --monthly 1000 --years 20 --rate 0.08
```

---

## 🧰 工具箱（`tools/`，全部零依赖）

| 工具 | 干嘛用 | 示例 |
|---|---|---|
| `compound_interest.py` | 复利 & 定投终值 + 72 法则 | `--principal 100000 --monthly 1000 --years 20 --rate 0.08` |
| `inflation_impact.py` | 通胀侵蚀购买力 | `--amount 100000 --years 30 --inflation 0.03` |
| `asset_allocation.py` | 按年龄/风险给股债现金配比 | `--age 28 --risk 高 --amount 100000` |
| `pe_percentile.py` | 算当前 PE 在历史的分位 | `--current 15 --history 12,13,14,15,18,20,22` |
| `fund_compare.py` | 两只基金费率/收益对比表 | 见文件内 `--help` |

---

## 🗓️ 30 天打卡

不想囤课？按 [`30天打卡计划.md`](30天打卡计划.md) 一天一主题，周末复盘。目标是建立
**「认知 → 行动 → 复盘」** 的闭环，而不是收藏吃灰。

---

## 🧪 实战案例（`examples/`，全部可复现）

把理论变成真实数字。每个案例都直接调用 `tools/` 脚本，输出真实运行结果：

| 案例 | 内容 | 工具 |
|---|---|---|
| [01 基金体检](examples/01-基金体检实战.md) | 用两只真实基金的费率、收益、估值做对比 | `fund_compare.py` |
| [02 复利滚雪球](examples/02-复利滚雪球实战.md) | 10 万 + 每月 1000 元，20 年复利与通胀侵蚀 | `compound_interest.py` + `inflation_impact.py` |
| [03 资产配置](examples/03-资产配置实战.md) | 按年龄/风险生成目标配比 + 估值分位辅助 | `asset_allocation.py` + `pe_percentile.py` |

→ 详见 [`examples/README.md`](examples/README.md)，附 [`sample-portfolio.csv`](examples/data/sample-portfolio.csv) 练习数据。

---

不想装 Python？打开 **[`index.html`](index.html)** 就能用浏览器跑交互式复利/通胀计算器（纯前端、零依赖）。若已开启 GitHub Pages，在线地址为：

```
https://wonderfulclaire.github.io/finance-learning-roadmap/
```

开启方法：仓库 `Settings → Pages → Branch: main → /(root) → Save`。

---

## 🤝 如何贡献

欢迎 PR / Issue！无论是纠偏、补案例、加工具还是翻译。**金融内容容错率低，纠错最珍贵。**
详见 [CONTRIBUTING.md](CONTRIBUTING.md)。核心红线：

- ❌ 不写"现在买 X"式建议、不承诺收益、不导流开户
- ✅ 一切以「帮读者建立正确认知框架」为准

---

## 📜 协议

[MIT](LICENSE) —— 随便用，留个署名就好。

---

## ⭐ 如果这个项目帮到了你

点个 **Star** ⭐ 是对「理财教育普惠」最大的支持，也能让更多人少踩坑。
欢迎分享给那个"想理财但不知道从哪开始"的朋友 🙌

> 理财是认知变现，慢就是快。祝你不慌不忙，稳稳变好。
