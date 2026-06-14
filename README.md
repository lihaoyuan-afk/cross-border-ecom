# 跨境电商学习与求职工作区

> 软件工程本科毕业，零基础转型跨境电商运营，目标岗位：**运营助理 / 数据运营助理 / 独立站运营**。  
> 目标平台：Amazon、Shopify。

---

## 项目展示

### 店铺数据看板（data-dashboard）

> Spring Boot 3 + Vue 3 + ECharts + MySQL | 还原 Amazon 运营日常数据监控场景

**总览页** — 核心指标卡片 + 销售趋势 + 广告 ACoS/ROAS + 流量漏斗 + 库存状态

![数据看板总览](docs/screenshots/data-dashboard-home.png)

**广告 & 库存模块** — ACoS 趋势线、ROAS 变化、可销天数预警标红

![数据看板广告模块](docs/screenshots/data-dashboard-ads.png)

**功能亮点：**
- 整合销售、广告、流量、库存 4 大模块，聚合 12 项核心运营指标
- 广告表现模块追踪 ACoS（20%～38%）、CTR（1.5%～3.5%）等关键指标
- 库存可销天数自动预警（橙色低库存 / 红色断货）
- 支持 7 / 30 / 90 天 / 全部时间维度切换
- 覆盖 180 天模拟数据，含情人节、618 等大促节点

---

### 选品分析工具（product-research）

> Python + pandas + Streamlit + Plotly | 数据驱动的 Amazon 选品决策系统

**市场概览** — 类目筛选、价格区间、BSR 范围多维过滤，实时更新图表

![选品工具市场概览](docs/screenshots/product-research-overview.png)

**选品评分** — BSR/评价数/评分/月销售额/价格五维加权评分，Top N 动态排行

![选品工具评分](docs/screenshots/product-research-scoring.png)

**关键词分析** — 标题高频词词频柱状图 + ProgressColumn 频次表

![选品工具关键词分析](docs/screenshots/product-research-keywords.png)

**竞争度分析** — 各类目综合雷达图 + 机会象限（评价门槛 vs 市场规模）

![选品工具竞争分析](docs/screenshots/product-research-competition.png)

**功能亮点：**
- 数据集覆盖 200 个产品、4 大类目、20 个品牌
- 5 维加权评分：BSR（40%）、评价数（20%）、产品评分（20%）、月销售额（10%）、价格合理性（10%）
- 4 个功能标签页、8 种 Plotly 交互图表
- 侧边栏多维筛选，Top N 商品（5～50）动态可调

---

### 竞品监控系统（competitor-monitor）

> Spring Boot 3 + MyBatis-Plus + Vue 3 + ECharts + MySQL | 自动化竞品预警

**功能亮点：**
- 覆盖 50 个 ASIN、5 大品类，90 天历史数据 4,500+ 条
- 每 5 分钟定时扫描，支持价格下跌 / 上涨 / BSR 异动 4 种预警类型，自动邮件通知
- Caffeine 缓存热点配置（TTL 5 分钟），Dashboard 接口响应时间降低约 60%
- 支持 7 / 30 / 90 天趋势折线图，移动端响应式
- 一键导出 BOM UTF-8 CSV，直接兼容 Excel

---

### Amazon Listing 优化引擎（listing-optimizer）

> Python Flask + Vue 3 | Listing 质量评分 + AI 改写建议

**功能亮点：**
- 8 维加权评分模型（标题长度、关键词密度、Bullet 数量/长度、描述完整度、图片数量、价格竞争力、评论数），输出 0～100 分及 A/B/C/D 四级评级
- 按高 / 中 / 低 3 个优先级返回分项优化建议
- 集成 AI 接口，根据评分弱项生成英文 Listing 重写方案，支持 mock 模式无 Key 演示

---

## 目录结构

```
cross-border-ecom/
├── 00-knowledge/                   # 行业知识专题笔记
│   ├── platforms/
│   │   ├── amazon-basics.md        # Amazon 平台基础入门
│   │   ├── amazon-ads.md           # 广告系统详解（SP/SB/SD/投放节奏）
│   │   ├── keyword-research.md     # 关键词研究方法论
│   │   └── product-selection.md    # 选品标准化五步法
│   └── glossary.md                 # 通用术语表（50+ 词条）
├── 01-projects/                    # 实战项目
│   ├── competitor-monitor/         # 竞品监控系统（Spring Boot + Vue 3）
│   ├── data-dashboard/             # 店铺数据看板（Spring Boot + Vue 3）
│   ├── listing-optimizer/          # Listing 优化引擎（Flask + Vue 3）
│   └── product-research/           # 选品分析工具（Streamlit）
├── 02-job-hunt/                    # 求职材料
│   ├── resume/resume.md            # 完整简历（4 个项目经历）
│   └── interview-prep/qa-common.md # 面试题库（11 题，含 STAR 答法）
├── 03-resources/                   # 参考资料
└── docs/screenshots/               # 项目界面截图
```

---

## 本地运行

### 选品分析工具（product-research）

```bash
cd 01-projects/product-research
pip install -r requirements.txt
streamlit run app.py
# 访问 http://localhost:8501
```

### 店铺数据看板（data-dashboard）

**前提：** MySQL 8.0+，创建数据库并导入测试数据

```bash
# 1. 初始化数据库
mysql -u root -p < 01-projects/data-dashboard/sql/init.sql

# 2. 生成 180 天模拟数据（修改 data-scripts/generate_store_data.py 中的密码）
cd 01-projects/data-dashboard/data-scripts
pip install mysql-connector-python
python generate_store_data.py

# 3. 启动后端（端口 8081）
cd 01-projects/data-dashboard/backend
DB_PASSWORD=你的数据库密码 mvn spring-boot:run

# 4. 启动前端
cd 01-projects/data-dashboard/frontend
npm install && npm run dev
# 访问 http://localhost:5173
```

### 竞品监控系统（competitor-monitor）

```bash
# 后端（端口 8080）
cd competitor-monitor/backend
DB_PASSWORD=你的数据库密码 mvn spring-boot:run

# 前端
cd competitor-monitor/frontend
npm install && npm run dev
# 访问 http://localhost:5173
```

---

## 学习进度

### 平台知识

- [x] Amazon 平台基础（FBA/FBM/BSR/ACOS）
- [x] Amazon 广告系统（SP / SB / SD 广告投放节奏）
- [x] Amazon SEO 与关键词研究方法论
- [x] 选品标准化流程（五步法 + 快速筛选清单）
- [ ] Shopify 独立站基础搭建
- [ ] Shopify + Facebook Ads 投放逻辑

### 实战项目

- [x] 选品数据分析工具（Python + Streamlit）
- [x] Listing 质量评分工具（Flask + Vue 3 + AI 优化）
- [x] 店铺销售数据看板（Spring Boot + Vue 3 + ECharts）
- [x] 竞品价格/BSR 监控预警系统（Spring Boot + Vue 3）

### 求职材料

- [x] 中文简历（4 个项目经历 + 量化亮点）
- [x] 面试题库（11 题，含平台基础 / 数据分析 / 行为题 STAR）
- [ ] 英文简历
- [ ] 模拟面试练习

---

## 知识笔记

| 文件 | 内容 |
|------|------|
| [Amazon 基础入门](00-knowledge/platforms/amazon-basics.md) | FBA/FBM 对比、BSR 原理、开店流程、运营助理日常 |
| [广告系统详解](00-knowledge/platforms/amazon-ads.md) | SP/SB/SD 广告类型、新品投放四阶段、报告分析、常见误区 |
| [关键词研究方法](00-knowledge/platforms/keyword-research.md) | 关键词分类、五步免费挖词、Listing 布局规范 |
| [选品标准化流程](00-knowledge/platforms/product-selection.md) | 选品五步法、竞争度量化标准、利润核算、10 分钟筛选清单 |
| [通用术语表](00-knowledge/glossary.md) | 50+ 词条，含平台 / 广告 / 物流 / 财务四类 |

---

*最后更新：2026-06-14*
