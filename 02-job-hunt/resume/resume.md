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
2021.09 — 2025.06

---

## 技能清单

### 跨境电商相关
- **平台知识：** Amazon FBA/FBM 运营流程、Listing 优化（标题/Bullet Points/A+）、BSR 分析与选品逻辑、广告 ACoS/ROAS 计算
- **数据分析：** 销售趋势分析、流量漏斗拆解（会话数→转化率→客单价）、库存周转率、广告 ROI 核算
- **工具：** Excel（VLOOKUP/数据透视表/条件格式）、Google Sheets、Jungle Scout（熟悉选品功能）、Helium 10（熟悉关键词研究与竞品反查）

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
- 覆盖 50 个 ASIN、5 大品类的价格与 BSR 自动追踪，90 天历史数据 4,500+ 条，6 张数据表支撑完整监控链路
- `@Scheduled` 定时任务每 5 分钟扫描预警，支持价格下跌 / 上涨 / BSR 异动 4 种预警类型，通过 JavaMail 自动邮件通知，消除人工巡检
- 预警配置支持全局阈值与单 ASIN 独立阈值，Caffeine 缓存热点配置（TTL 5 分钟），减少重复数据库读取
- 前端 5 个页面，Vue 3 + ECharts 渲染价格 / BSR 趋势折线图，支持 7 / 30 / 90 天时间维度切换，适配移动端（侧边栏抽屉化）
- 一键导出预警记录为 BOM UTF-8 CSV，直接兼容 Excel；支持商品批量删除（checkbox + 二次确认）

**量化亮点：** Dashboard 接口从 5 次独立查询合并为 2 次条件聚合查询，响应时间降低约 60%；后端共 10 个 REST API，全局异常处理覆盖全部接口

---

### 2. 店铺数据看板
**技术栈：** Spring Boot 3 · MyBatis-Plus · MySQL · Vue 3 · ECharts
**时间：** 2025.01 — 2025.02
**GitHub：** https://github.com/lihaoyuan-afk/cross-border-ecom（data-dashboard 目录）

**项目背景：** 模拟 Amazon 运营日常数据报表需求，构建可视化数据看板，还原真实运营场景下的数据监控工作流。

**核心功能与实现：**
- 整合销售、广告、流量、库存 4 大模块，聚合 12 项核心运营指标（ACoS / ROAS / CTR / 转化率 / 库存可销天数等），覆盖 180 天历史数据
- 广告表现模块：追踪 ACoS（20%～38%）、CTR（1.5%～3.5%）等关键指标，辅助判断广告投放健康度
- 库存状态模块：5 个 SKU 实时库存 + 可销天数计算，自动标红断货和低库存品
- 流量漏斗模块：会话数→页面浏览→转化率 ECharts 漏斗图，量化各环节流失
- Python 数据脚本模拟 180 天逼真数据，含情人节（×2.2）、女神节（×2.0）、618（×3.0）3 个大促节点及周末效应；支持 Excel 双 Sheet 一键导出

---

### 3. Amazon Listing 优化引擎
**技术栈：** Python · Flask · Vue 3
**时间：** 2024.11 — 2024.12
**GitHub：** https://github.com/lihaoyuan-afk/cross-border-ecom（listing-optimizer 目录）

**项目背景：** Amazon Listing 质量直接影响自然流量和转化率，人工逐条评估耗时且主观性强。

**核心功能与实现：**
- 基于 Amazon A9 算法设计 8 维加权评分模型（标题长度、关键词密度、Bullet 数量 / 长度、描述完整度、图片数量、价格竞争力、评论数），输出 0～100 分及 A / B / C / D 四级评级
- 后端 Flask 提供 4 个 REST API，按高 / 中 / 低 3 个优先级返回分项优化建议，前端 Vue 3 实时展示
- 集成 OpenAI GPT-4o 接口，根据评分弱项自动生成英文 Listing 重写方案（标题 150～200 字符、5 条 Bullet、描述 1000～1500 字符），支持 mock 模式无 Key 演示

---

### 4. Amazon 选品分析工具
**技术栈：** Python · pandas · Streamlit · Plotly
**时间：** 2025.06
**GitHub：** https://github.com/lihaoyuan-afk/cross-border-ecom（product-research 目录）

**项目背景：** 选品是跨境电商运营的核心环节，通过数据量化分析取代主观判断。

**核心功能与实现：**
- 数据集覆盖 200 个产品、4 大类目、20 个品牌，模拟完整 Amazon 市场竞争格局
- 5 维加权选品评分模型：BSR（40%）、评价数（20%）、产品评分（20%）、月销售额（10%）、价格合理性（10%），输出 0～100 分量化得分
- 关键词词频分析：提取全品类 Top 30 高频词及各类目 Top 15 对比，直接输出 Listing 关键词布局参考
- 竞争度分析：竞争指数 + 机会象限图（评价门槛 vs 市场规模），快速识别低竞争高潜力类目
- 4 个功能标签页、8 种 Plotly 交互图表；侧边栏支持类目 / 价格 / 评分 / BSR 多维筛选，Top N 商品（5～50）动态可调

---

## 自我评价

软件工程背景，具备较强的数据分析和工具开发能力，能将运营需求转化为可落地的技术方案。
在系统学习跨境电商过程中，通过搭建四个实战项目积累了 Amazon 平台运营逻辑、选品方法论和数据指标体系的实际理解。
学习能力强，能快速上手新平台和工具，适应运营数据分析岗位的快节奏工作环境。

---

*更新日期：2026-06-14*
