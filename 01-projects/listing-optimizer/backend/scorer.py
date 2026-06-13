"""
Amazon Listing 质量评分引擎
基于 Amazon A9 算法核心排名因素设计的 8 维评分模型
"""

from dataclasses import dataclass, field
from typing import Optional
import re


@dataclass
class DimensionScore:
    name: str           # 维度名称
    score: float        # 得分 0-10
    weight: float       # 权重
    issue: str          # 问题描述
    suggestion: str     # 改进方向


@dataclass
class ScoringResult:
    dimensions: list[DimensionScore] = field(default_factory=list)
    total_score: float = 0.0        # 加权总分（0-100）
    grade: str = ""                 # 等级：A/B/C/D
    summary: str = ""               # 总体评价


def score_title_length(title: str) -> DimensionScore:
    """
    维度1：标题长度
    Amazon 建议标题 80-200 字符，过短缺乏关键词，过长被截断
    """
    length = len(title.strip())
    if 80 <= length <= 200:
        score = 10.0
        issue = f"标题长度 {length} 字符，处于最优区间 (80-200)"
        suggestion = "保持现有标题长度"
    elif 60 <= length < 80:
        score = 6.0
        issue = f"标题偏短 ({length} 字符)，可能关键词覆盖不足"
        suggestion = "建议扩展至 80-200 字符，补充品牌词/型号/核心使用场景"
    elif length < 60:
        score = 3.0
        issue = f"标题过短 ({length} 字符)，严重影响 SEO 覆盖"
        suggestion = "需大幅补充关键词，至少达到 80 字符"
    elif 200 < length <= 250:
        score = 7.0
        issue = f"标题偏长 ({length} 字符)，移动端会被截断"
        suggestion = "适当压缩至 200 字符以内，保留最重要的关键词"
    else:
        score = 4.0
        issue = f"标题过长 ({length} 字符)，超出 Amazon 推荐上限"
        suggestion = "压缩至 200 字符，删除重复词、语气词及非核心信息"

    return DimensionScore("标题长度", score, 2.0, issue, suggestion)


def score_keyword_density(title: str) -> DimensionScore:
    """
    维度2：标题关键词密度
    主关键词（标题首个名词短语）应出现 1-2 次，避免堆砌
    """
    words = title.lower().split()
    total_words = len(words)

    if total_words == 0:
        return DimensionScore("关键词密度", 0, 2.0, "标题为空", "请填写标题")

    # 统计词频，过滤停用词
    stopwords = {
        "a", "an", "the", "and", "or", "for", "with", "in", "on", "at",
        "to", "of", "by", "is", "are", "be", "that", "this", "it", "as"
    }
    word_freq: dict[str, int] = {}
    for w in words:
        clean = re.sub(r"[^a-z0-9]", "", w)
        if clean and clean not in stopwords and len(clean) > 2:
            word_freq[clean] = word_freq.get(clean, 0) + 1

    if not word_freq:
        return DimensionScore("关键词密度", 5.0, 2.0, "无法识别有效关键词", "请确保标题包含英文关键词")

    max_count = max(word_freq.values())
    repeated_words = [w for w, c in word_freq.items() if c >= 3]

    if max_count <= 2 and not repeated_words:
        score = 10.0
        issue = "关键词分布自然，无明显堆砌"
        suggestion = "关键词密度良好，保持现状"
    elif max_count == 2:
        score = 8.0
        issue = "主关键词出现 2 次，处于合理范围"
        suggestion = "注意避免同一词出现超过 2 次"
    elif repeated_words:
        score = max(2.0, 7.0 - len(repeated_words) * 2)
        issue = f"以下词重复出现 3+ 次，可能触发 Amazon 关键词堆砌惩罚：{', '.join(repeated_words[:3])}"
        suggestion = "删除重复词，用同义词或长尾词替换"
    else:
        score = 6.0
        issue = "关键词分布一般"
        suggestion = "确保核心关键词自然融入标题"

    return DimensionScore("关键词密度", score, 2.0, issue, suggestion)


def score_bullet_count(bullets: list[str]) -> DimensionScore:
    """
    维度3：Bullet Points 数量
    Amazon 允许最多 5 条，5 条展示最完整，少于 3 条严重减分
    """
    count = len([b for b in bullets if b.strip()])

    if count == 5:
        score = 10.0
        issue = "5 条 Bullet Points，充分利用了 Amazon 展示空间"
        suggestion = "保持 5 条数量"
    elif count == 4:
        score = 7.0
        issue = f"当前 {count} 条 Bullet，未充分利用展示空间"
        suggestion = "补充第 5 条，可覆盖：保修/售后、使用场景、兼容性等"
    elif count == 3:
        score = 5.0
        issue = f"当前 {count} 条 Bullet，信息量不足"
        suggestion = "至少补充到 5 条，每条围绕一个独立卖点展开"
    elif count > 0:
        score = max(1.0, float(count) * 1.5)
        issue = f"仅 {count} 条 Bullet，严重缺乏产品信息"
        suggestion = "紧急补充至 5 条完整 Bullet Points"
    else:
        score = 0.0
        issue = "未填写任何 Bullet Points"
        suggestion = "必须填写 5 条 Bullet Points，这是转化率的核心影响因素"

    return DimensionScore("Bullet数量", score, 2.0, issue, suggestion)


def score_bullet_length(bullets: list[str]) -> DimensionScore:
    """
    维度4：Bullet Points 平均长度
    每条 150-250 字符最优：足够说明特性，不会显得冗长
    """
    valid_bullets = [b.strip() for b in bullets if b.strip()]
    if not valid_bullets:
        return DimensionScore("Bullet长度", 0, 1.0, "无有效 Bullet Points", "请先填写 Bullet Points")

    avg_len = sum(len(b) for b in valid_bullets) / len(valid_bullets)

    if 150 <= avg_len <= 250:
        score = 10.0
        issue = f"Bullet 平均长度 {avg_len:.0f} 字符，处于最优区间"
        suggestion = "保持当前描述深度"
    elif 100 <= avg_len < 150:
        score = 7.0
        issue = f"Bullet 平均偏短 ({avg_len:.0f} 字符)，卖点阐述不够充分"
        suggestion = "每条 Bullet 补充具体数据、材质规格或使用场景，扩展至 150+ 字符"
    elif avg_len < 100:
        score = 4.0
        issue = f"Bullet 平均过短 ({avg_len:.0f} 字符)，无法有效传递产品价值"
        suggestion = "重写所有 Bullet，每条包含：功能特点 + 用户收益 + 数据支撑"
    elif 250 < avg_len <= 350:
        score = 7.0
        issue = f"Bullet 平均偏长 ({avg_len:.0f} 字符)，部分用户可能跳过阅读"
        suggestion = "提炼核心信息，压缩至 250 字符内，突出最重要的卖点"
    else:
        score = 5.0
        issue = f"Bullet 平均过长 ({avg_len:.0f} 字符)，影响可读性"
        suggestion = "大幅压缩，每条只保留 1-2 个核心卖点"

    return DimensionScore("Bullet长度", score, 2.0, issue, suggestion)


def score_description_length(description: str) -> DimensionScore:
    """
    维度5：描述文字长度
    >1000 字符满分，description 对 A9 算法有直接影响，也影响转化
    """
    length = len(description.strip())

    if length >= 1000:
        score = 10.0
        issue = f"描述长度 {length} 字符，内容充实"
        suggestion = "保持详细描述，可考虑加入 A+ Content"
    elif length >= 600:
        score = 7.0
        issue = f"描述长度 {length} 字符，略显不足"
        suggestion = "扩展至 1000+ 字符，增加使用场景、FAQ、技术规格等内容"
    elif length >= 300:
        score = 5.0
        issue = f"描述过短 ({length} 字符)，缺乏 SEO 价值"
        suggestion = "重写描述，至少 1000 字符，覆盖：产品背景、核心卖点、人群定位、使用方法"
    elif length > 0:
        score = 2.0
        issue = f"描述极短 ({length} 字符)，几乎无 SEO 贡献"
        suggestion = "urgently 重写完整描述，这是 Amazon 算法的重要排名信号"
    else:
        score = 0.0
        issue = "未填写产品描述"
        suggestion = "必须填写 1000+ 字符的产品描述"

    return DimensionScore("描述长度", score, 1.0, issue, suggestion)


def score_image_count(image_count: int) -> DimensionScore:
    """
    维度6：图片数量
    Amazon 允许最多 7 张，主图+6张辅图，图片直接影响转化率
    """
    if image_count >= 7:
        score = 10.0
        issue = f"{image_count} 张图片，充分利用了图片展示名额"
        suggestion = "保持 7 张，确保包含：白底主图、场景图、细节图、尺寸对比图"
    elif image_count == 6:
        score = 8.0
        issue = "6 张图片，仅差 1 张达到满配"
        suggestion = "补充第 7 张，建议增加：信息图（展示核心规格）或对比图"
    elif image_count == 5:
        score = 6.0
        issue = f"{image_count} 张图片，展示空间未充分利用"
        suggestion = "补充至 7 张，增加场景图和信息图提升转化"
    elif image_count >= 3:
        score = max(3.0, float(image_count) * 1.2)
        issue = f"仅 {image_count} 张图片，转化率将受到明显影响"
        suggestion = "至少补充至 7 张，图片是 Amazon 转化的第一要素"
    elif image_count > 0:
        score = 2.0
        issue = f"仅 {image_count} 张图片，严重不足"
        suggestion = "紧急补充图片至 7 张"
    else:
        score = 0.0
        issue = "无产品图片"
        suggestion = "必须上传图片，这是 Amazon listing 的基本要求"

    return DimensionScore("图片数量", score, 1.0, issue, suggestion)


def score_price_competitiveness(price: float, avg_category_price: float) -> DimensionScore:
    """
    维度7：价格竞争力
    与类目均价对比，价格是 A9 算法 Buy Box 的核心因素
    """
    if avg_category_price <= 0:
        return DimensionScore("价格竞争力", 5.0, 1.0, "未提供类目均价，无法评估", "请输入类目均价以获得准确评分")

    ratio = price / avg_category_price  # 1.0 = 与均价相同

    if 0.85 <= ratio <= 1.05:
        score = 10.0
        issue = f"定价 ${price:.2f} 处于类目均价的 ±15% 区间内，竞争力强"
        suggestion = "价格竞争力良好，可关注竞品动态及时调价"
    elif 0.7 <= ratio < 0.85:
        score = 9.0
        issue = f"定价低于类目均价 {(1-ratio)*100:.0f}%，价格优势明显"
        suggestion = "价格优势强，注意毛利率，避免过度价格战"
    elif ratio < 0.7:
        score = 7.0
        issue = f"定价远低于类目均价 {(1-ratio)*100:.0f}%，可能影响品牌感知"
        suggestion = "价格过低可能让消费者质疑产品质量，评估是否有提价空间"
    elif 1.05 < ratio <= 1.2:
        score = 7.0
        issue = f"定价高于类目均价 {(ratio-1)*100:.0f}%，需要强差异化支撑"
        suggestion = "确保 Listing 品质（图片、描述）能体现溢价价值，加强评论积累"
    elif 1.2 < ratio <= 1.5:
        score = 4.0
        issue = f"定价高于类目均价 {(ratio-1)*100:.0f}%，竞争力弱"
        suggestion = "大幅高于均价需要极强的品牌力或独特卖点支撑，否则建议调整定价策略"
    else:
        score = 2.0
        issue = f"定价远高于类目均价 {(ratio-1)*100:.0f}%，难以竞争"
        suggestion = "价格策略需要重新评估，或强化差异化建立独特定位"

    return DimensionScore("价格竞争力", score, 1.0, issue, suggestion)


def score_review_count(review_count: int) -> DimensionScore:
    """
    维度8：评论数量
    >50 条为基准满分，评论是 A9 信任信号的核心，也影响点击率
    """
    if review_count >= 100:
        score = 10.0
        issue = f"{review_count} 条评论，信任基础扎实"
        suggestion = "持续维护评论质量，监控差评并及时响应"
    elif review_count >= 50:
        score = 9.0
        issue = f"{review_count} 条评论，达到基准水位"
        suggestion = "继续积累评论，100+ 条是竞争强类目的门槛"
    elif review_count >= 25:
        score = 7.0
        issue = f"{review_count} 条评论，具备基本信任度"
        suggestion = "通过 Request a Review 工具加速评论积累，目标 50+ 条"
    elif review_count >= 10:
        score = 5.0
        issue = f"{review_count} 条评论，信任信号偏弱"
        suggestion = "优先使用合规手段积累评论：Follow-up 邮件、Vine 计划、优化 IPI"
    elif review_count > 0:
        score = 3.0
        issue = f"仅 {review_count} 条评论，几乎无信任背书"
        suggestion = "新品期重点投入评论获取，可加入 Early Reviewer Program"
    else:
        score = 0.0
        issue = "暂无评论"
        suggestion = "尽快通过合规渠道获取首批评论，0 评论转化率极低"

    return DimensionScore("评论数量", score, 1.0, issue, suggestion)


def calculate_total_score(dimensions: list[DimensionScore]) -> float:
    """加权平均计算总分，映射到 0-100"""
    total_weighted = sum(d.score * d.weight for d in dimensions)
    total_weight = sum(d.weight for d in dimensions)
    # 每维 0-10，加权后映射到 0-100
    return round((total_weighted / total_weight) * 10, 1)


def get_grade(total_score: float) -> tuple[str, str]:
    """根据总分返回等级和总体评价"""
    if total_score >= 85:
        return "A", "Listing 质量优秀，已具备参与 Best Seller 竞争的基础条件"
    elif total_score >= 70:
        return "B", "Listing 质量良好，针对低分维度优化后可显著提升排名"
    elif total_score >= 55:
        return "C", "Listing 存在明显短板，建议按优先级系统性优化"
    else:
        return "D", "Listing 质量较差，需全面重构以具备基本竞争力"


def score_listing(
    title: str,
    bullets: list[str],
    description: str,
    image_count: int,
    price: float,
    avg_category_price: float,
    review_count: int,
) -> dict:
    """
    主评分函数：输入 Listing 数据，输出完整评分报告

    Returns:
        dict with keys: dimensions, total_score, grade, summary
    """
    dimensions = [
        score_title_length(title),
        score_keyword_density(title),
        score_bullet_count(bullets),
        score_bullet_length(bullets),
        score_description_length(description),
        score_image_count(image_count),
        score_price_competitiveness(price, avg_category_price),
        score_review_count(review_count),
    ]

    total_score = calculate_total_score(dimensions)
    grade, summary = get_grade(total_score)

    return {
        "dimensions": [
            {
                "name": d.name,
                "score": round(d.score, 1),
                "weight": d.weight,
                "issue": d.issue,
                "suggestion": d.suggestion,
            }
            for d in dimensions
        ],
        "total_score": total_score,
        "grade": grade,
        "summary": summary,
    }
