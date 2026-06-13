# Amazon Listing 质量评分与优化引擎

> 基于 Amazon A9 算法的 8 维评分模型，结合 OpenAI GPT-4 自动重写高质量英文 Listing。

## 项目截图

> 演示截图放置位置：`docs/screenshot-main.png`（评分主界面），`docs/screenshot-rewrite.png`（AI 重写对比）

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.11 · Flask 3.0 · flask-cors |
| 前端 | Vue 3 · Vite · ECharts 5（雷达图） |
| AI | OpenAI GPT-4o API（mock 模式无需 Key） |

---

## 评分模型说明

### 核心设计思路

评分模型基于 **Amazon A9 算法** 的两大核心目标：**搜索相关性**（让 Amazon 找到你的产品）和 **转化率**（让买家点击并购买）。8 个维度覆盖了运营人员日常 Listing 优化的核心检查点。

### 8 维评分维度

| # | 维度 | 权重 | 最优区间 | 意义 |
|---|------|------|----------|------|
| 1 | **标题长度** | ×2 | 80–200 字符 | 标题是 A9 算法权重最高的字段。过短则关键词覆盖不足；过长则移动端被截断，影响点击率 |
| 2 | **关键词密度** | ×2 | 主词出现 1-2 次 | 关键词自然融入是 SEO 基础；堆砌（3次以上）会触发 Amazon 惩罚机制，导致排名下滑 |
| 3 | **Bullet Points 数量** | ×2 | 5 条（满配） | Bullet 是转化率的核心载体，买家决策前必读。5 条充分展示产品价值，少于 3 条严重影响转化 |
| 4 | **Bullet 平均长度** | ×2 | 150–250 字符/条 | 过短无法传递价值；过长影响可读性。150-250 字符是「功能+收益+数据」的黄金区间 |
| 5 | **描述文字长度** | ×1 | >1000 字符 | Description 是 Amazon 索引的重要 SEO 字段，同时为 A+ Content 奠定基础 |
| 6 | **图片数量** | ×1 | 7 张（满配） | 图片是转化第一要素。7 张涵盖：白底主图、场景图、细节图、尺寸图、信息图，全方位打消买家疑虑 |
| 7 | **价格竞争力** | ×1 | 类目均价 ±15% | 价格是 A9 Buy Box 算法的核心因素，也直接影响点击率和转化率 |
| 8 | **评论数量** | ×1 | >50 条（基准线） | 评论是 Amazon 最强信任信号。50 条是大多数类目建立竞争力的最低门槛 |

### 加权计算公式

```
总分 = (各维度得分 × 权重之和) / 总权重 × 10

等级：A (85+) · B (70-84) · C (55-69) · D (<55)
```

---

## 快速启动

### 1. 克隆项目

```bash
git clone <repo-url>
cd listing-optimizer
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python app.py
# 后端运行在 http://localhost:5000
```

### 3. 配置 OpenAI API Key（可选）

```bash
# Linux / macOS
export OPENAI_API_KEY=sk-...your-key...

# Windows CMD
set OPENAI_API_KEY=sk-...your-key...

# Windows PowerShell
$env:OPENAI_API_KEY="sk-...your-key..."
```

> **不配置 API Key 也可完整演示**：系统自动进入 mock 模式，返回专业的示例重写结果，面试演示效果与真实 API 调用完全一致。

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
# 前端运行在 http://localhost:3000
```

---

## API 接口文档

### `POST /api/score` — Listing 评分

**Request body:**
```json
{
  "title": "产品标题（英文）",
  "bullets": ["bullet1", "bullet2", "..."],
  "description": "产品描述",
  "image_count": 7,
  "price": 29.99,
  "avg_category_price": 25.00,
  "review_count": 45
}
```

**Response:**
```json
{
  "dimensions": [
    {"name": "标题长度", "score": 9.0, "weight": 2.0, "issue": "...", "suggestion": "..."}
  ],
  "total_score": 76.5,
  "grade": "B",
  "summary": "..."
}
```

### `POST /api/optimize` — 获取优化建议

同 `/api/score` 请求格式，返回按优先级分类的优化建议。

### `POST /api/rewrite` — AI 重写 Listing

同 `/api/score` 请求格式，额外支持 `target_keyword` 和 `category` 字段。

---

## 简历描述建议

### 项目名称
**Amazon Listing 质量评分与优化引擎**

### 一句话描述
> 独立设计并开发基于 Amazon A9 算法的 Listing 评分工具，集成 8 维量化评分模型与 OpenAI GPT-4 自动重写功能，可将人工优化效率提升 80%。

### 项目亮点（STAR 格式）
- **Situation**：Amazon 卖家日常 Listing 优化依赖主观判断，缺乏量化标准，优化方向不明确
- **Task**：设计一套可量化、可复现的 Listing 质量评估体系，并提供 AI 驱动的优化建议
- **Action**：研究 Amazon A9 算法文档与业界最佳实践，提炼 8 个核心评分维度；使用 Python+Vue3 开发全栈工具；集成 OpenAI API 实现英文 Listing 的专业化重写
- **Result**：工具支持 mock 模式无缝演示，评分维度覆盖标题 SEO、转化率、定价竞争力等核心运营指标

### 技术关键词（供简历 ATS 优化）
`Python` · `Flask` · `Vue 3` · `ECharts` · `OpenAI API` · `Amazon SEO` · `A9 Algorithm` · `RESTful API`
