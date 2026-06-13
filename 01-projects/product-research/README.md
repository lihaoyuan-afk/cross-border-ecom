# Amazon 选品分析工具

基于 Python + pandas + Streamlit 构建的跨境电商选品辅助决策系统，模拟真实 Amazon 产品数据，提供多维度市场分析。

## 功能模块

| 标签页 | 功能 |
|--------|------|
| 📊 市场概览 | 类目商品数、平均价格/BSR/月销售额、价格与评分分布直方图 |
| 🏆 选品评分 | 五维加权评分（BSR/评价数/评分/月销售额/价格）、Top N 商品排名、BSR × 月销售额散点图 |
| 🔑 关键词分析 | 标题词频统计、Top 30 高频词、各类目关键词对比 |
| ⚔️ 竞争度分析 | 竞争指数、雷达图多维对比、机会象限（进入门槛 vs 市场规模） |

## 选品评分权重

```
BSR 排名      40%  （排名越低分越高）
评价数        20%  （50~500 条最佳，过多竞争过大）
产品评分      20%  （越高越好）
月销售额      10%  （估算值，BSR 推算）
价格合理性    10%  （$15~$50 跨境最优区间）
```

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt

# 生成模拟数据（首次运行）
python generate_data.py

# 启动应用
streamlit run app.py
```

访问 http://localhost:8501

## 技术栈

- **Python 3.11+**
- **pandas** — 数据处理与聚合分析
- **Streamlit** — 交互式 Web 应用框架
- **Plotly** — 可交互图表（柱状图、散点图、雷达图）

## 项目结构

```
product-research/
├── app.py               # Streamlit 主应用
├── generate_data.py     # 模拟数据生成脚本
├── requirements.txt
└── data/
    └── amazon_products.csv   # 200 条模拟产品数据
```
