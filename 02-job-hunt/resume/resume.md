# 个人简历

> 格式说明：本文件为 Markdown 草稿，投递时建议转为 Word/PDF（推荐使用 Typora 或 Pandoc 导出）

---

## 基本信息

| 项目 | 内容 |
|------|------|
| 姓名 | 李浩源 |
| 求职意向 | 跨境电商运营助理 / 数据运营助理 / 独立站运营 |
| 目标平台 | Amazon / Shopify |
| 联系邮箱 | zli638653@gmail.com |
| GitHub | https://github.com/lihaoyuan-afk/cross-border-ecom |

---

## 教育背景

**软件工程 · 本科**
XXXX 大学 · 计算机学院
2021.09 — 2025.06（预计）

---

## 技能清单

### 跨境电商相关
- **平台知识：** Amazon FBA/FBM 运营流程、Listing 优化（标题/Bullet Points/A+）、BSR 分析与选品逻辑、广告 ACoS/ROAS 计算
- **数据分析：** 销售趋势分析、流量漏斗拆解（会话数→转化率→客单价）、库存周转率、广告 ROI 核算
- **工具：** Excel（VLOOKUP/数据透视表/条件格式）、Google Sheets、Jungle Scout（了解）、Helium 10（了解）

### 技术技能
- **语言：** Python（pandas/Streamlit/Flask）、Java（Spring Boot/MyBatis-Plus）
- **前端：** Vue 3、Element Plus、ECharts / Plotly
- **数据库：** MySQL
- **其他：** Git、RESTful API 设计、Linux 基础

---

## 项目经历

### 1. 跨境电商竞品监控系统
**技术栈：** Spring Boot 3 · MyBatis-Plus · MySQL · Vue 3 · ECharts · Element Plus
**时间：** 2025.03 — 2025.05
**GitHub：** https://github.com/lihaoyuan-afk/cross-border-ecom（competitor-monitor 分支）

**项目背景：** 针对 Amazon 运营中竞品价格和 BSR 频繁波动、人工追踪效率低的痛点，开发自动化监控预警系统。

**核心功能与实现：**
- 实时监控竞品价格和 BSR 排名变化，超过阈值自动触发预警（价格下跌 / 上涨 / BSR 异动四类型）
- `@Scheduled` 定时任务每 5 分钟扫描新预警，通过 JavaMail 发送邮件汇总通知，减少人工巡检频次
- 预警配置支持全局阈值和单品独立阈值，使用 `@Cacheable` 缓存热点配置，减少数据库查询
- 前端 Vue 3 + ECharts 渲染价格/BSR 趋势折线图，支持移动端自适应（侧边栏抽屉化）
- 一键导出全部预警记录为 BOM UTF-8 CSV 文件，直接兼容 Excel 打开

**量化亮点：** Dashboard 数据接口从 4 次独立查询优化为 1 次聚合查询，响应时间降低约 60%

---

### 2. 店铺数据看板
**技术栈：** Spring Boot 3 · MyBatis-Plus · MySQL · Vue 3 · ECharts
**时间：** 2025.01 — 2025.02
**GitHub：** https://github.com/lihaoyuan-afk/cross-border-ecom（data-dashboard 目录）

**项目背景：** 模拟 Amazon 运营日常数据报表需求，构建可视化数据看板，还原真实运营场景下的数据监控工作流。

**核心功能与实现：**
- 销售趋势模块：展示 180 天日销售额/订单量折线图，包含情人节、618 等大促节点标注
- 广告表现模块：ACoS、ROAS、CTR、曝光量/点击量趋势分析，辅助广告投放决策
- 库存状态模块：5 个 SKU 实时库存 + 可销天数预警（断货/低库存标红）
- 流量漏斗模块：会话数→页面浏览→转化率 ECharts 漏斗图，量化各环节流失
- 数据生成脚本：Python 生成 180 天逼真模拟数据（含周末效应 + 促销倍增系数），写入 MySQL

---

### 3. Amazon Listing 优化引擎
**技术栈：** Python · Flask · Vue 3
**时间：** 2024.11 — 2024.12
**GitHub：** https://github.com/lihaoyuan-afk/cross-border-ecom（listing-optimizer 目录）

**项目背景：** Amazon Listing 质量直接影响自然流量和转化率，人工逐条评估耗时且主观性强。

**核心功能与实现：**
- 基于 Amazon 官方 Listing 最佳实践，设计 0-100 分评分体系（标题长度/关键词密度/图片数量/描述完整度等维度）
- 后端 Flask API 解析 Listing 数据，返回分项得分和优化建议，前端 Vue 3 实时展示
- 集成 AI 辅助优化接口，根据评分弱项生成改写建议

---

### 4. Amazon 选品分析工具
**技术栈：** Python · pandas · Streamlit · Plotly
**时间：** 2025.06
**GitHub：** https://github.com/lihaoyuan-afk/cross-border-ecom（product-research 目录）

**项目背景：** 选品是跨境电商运营的核心环节，通过数据量化分析取代主观判断。

**核心功能与实现：**
- 基于 BSR / 评价数 / 评分 / 月销售额 / 价格合理性五维加权评分（各权重按行业经验标定）
- 关键词词频分析：提取全品类 Top 30 高频词，辅助 Listing 关键词布局
- 竞争度分析：机会象限图（进入门槛 vs 市场规模），快速识别低竞争高潜力类目
- Streamlit 侧边栏多维筛选（类目/价格区间/评分/BSR），所有图表基于 Plotly 可交互

---

## 自我评价

软件工程背景，具备较强的数据分析和工具开发能力，能将运营需求转化为可落地的技术方案。
在系统学习跨境电商过程中，通过搭建四个实战项目积累了 Amazon 平台运营逻辑、选品方法论和数据指标体系的实际理解。
学习能力强，能快速上手新平台和工具，适应运营数据分析岗位的快节奏工作环境。

---

*更新日期：2026-06-13*
