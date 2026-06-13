"""
AI 优化建议模块
- generate_suggestions: 基于规则生成中文优化建议（无需 API）
- rewrite_with_ai: 调用 OpenAI API 重写 Listing（无 Key 时返回 mock 数据）
"""

import os
from typing import Optional


# ──────────────────────────────────────────────
# 规则引擎：基于评分低分项生成中文建议
# ──────────────────────────────────────────────

# 每个维度的详细优化建议库（score 阈值 → 建议文本）
RULE_SUGGESTIONS: dict[str, list[tuple[float, str]]] = {
    "标题长度": [
        (5.0, "【紧急】标题严重过短，建议格式：[品牌] + [核心关键词] + [产品型号/规格] + [适用场景] + [Pack/Count]"),
        (7.0, "标题长度不足，可在现有基础上补充：目标人群描述、兼容型号、材质工艺等信息"),
        (8.5, "标题略短，建议补充 1-2 个长尾关键词以提高搜索覆盖"),
    ],
    "关键词密度": [
        (5.0, "【紧急】标题存在严重关键词堆砌，Amazon 可能会降低 Listing 权重甚至下架，立即移除重复关键词"),
        (7.0, "标题关键词有轻微重复，建议使用同义词或长尾变体替换重复词"),
        (9.0, "关键词密度基本合理，确保主关键词自然出现在标题前 80 字符内"),
    ],
    "Bullet数量": [
        (3.0, "【紧急】Bullet Points 数量严重不足，必须补充至 5 条。参考结构：①核心功能 ②材质/规格 ③使用场景 ④兼容性 ⑤售后保障"),
        (6.0, "Bullet 数量不足，补充缺失的条目，建议最后一条写品牌保障/退换货政策增加信任感"),
        (8.5, "接近满配，补充最后 1 条 Bullet 即可，建议写竞争差异点或独特卖点"),
    ],
    "Bullet长度": [
        (5.0, "【紧急】Bullet 内容过于简短，重写格式建议：[大写开头关键词] + [功能说明（30字）] + [用户收益（30字）] + [数据/规格（20字）]"),
        (7.0, "Bullet 长度偏短，为每条增加：使用场景举例、具体数据参数、或用户痛点解决方案"),
        (9.0, "Bullet 长度略显不足，可适当补充产品细节，但避免超过 250 字符"),
    ],
    "描述长度": [
        (3.0, "【紧急】产品描述几乎为空，立即补充完整描述。结构：①引导段（产品定位/人群）②核心卖点展开（3-4段）③使用说明 ④品牌故事 ⑤FAQ"),
        (6.0, "描述不足 1000 字符，扩充建议：增加 FAQ（3-5 个常见问题）、使用步骤说明、与竞品的差异化说明"),
        (8.5, "描述长度接近达标，再补充 1-2 段使用场景或目标人群描述即可"),
    ],
    "图片数量": [
        (3.0, "【紧急】图片严重不足，立即补充。7 张图片建议分配：①白底主图 ②场景图 ③细节/工艺图 ④尺寸对比图 ⑤功能信息图 ⑥使用步骤图 ⑦多变体展示图"),
        (6.0, "图片数量不足，补充重点：信息图（展示核心规格和卖点）、场景图（买家代入感）"),
        (8.5, "差 1-2 张达到满配，建议补充信息图或节日场景图"),
    ],
    "价格竞争力": [
        (4.0, "定价明显偏高，建议：①重新调研竞品价格带 ②评估是否有差异化支撑溢价 ③考虑使用 Coupon 降低心理价位"),
        (7.0, "定价略高，建议：增加产品评论数量和 A+ Content 来强化溢价感知"),
        (9.0, "价格竞争力良好，持续监控竞品定价，建议使用 Repricing 工具"),
    ],
    "评论数量": [
        (3.0, "【紧急】评论数严重不足，合规积累路径：①开启 Request a Review 自动化 ②申请加入 Vine 计划（新品期免费）③优化包装加入引导卡片"),
        (6.0, "评论数量偏少，建议：设置自动 Follow-up 邮件序列，在送达后 7-14 天请求评论"),
        (8.5, "评论基础良好，重点维护评论质量：及时回复差评，展示品牌负责任的态度"),
    ],
}


def generate_suggestions(listing_data: dict, scores: dict) -> dict:
    """
    基于规则引擎为低分维度生成中文优化建议

    Args:
        listing_data: 原始 Listing 数据
        scores: 评分结果（来自 scorer.py）

    Returns:
        dict with keys: priority_actions (高优先级), improvements (其他建议), quick_wins (速效优化)
    """
    priority_actions = []   # 得分 < 5 的维度
    improvements = []       # 得分 5-7.5 的维度
    quick_wins = []         # 得分 7.5-9 的维度（小优化，高性价比）

    for dim in scores.get("dimensions", []):
        name = dim["name"]
        score = dim["score"]

        if name not in RULE_SUGGESTIONS:
            continue

        # 找到对应阈值的建议
        chosen_suggestion = None
        for threshold, suggestion_text in RULE_SUGGESTIONS[name]:
            if score <= threshold:
                chosen_suggestion = suggestion_text
                break

        if chosen_suggestion is None:
            continue  # 高分维度，无需建议

        item = {
            "dimension": name,
            "current_score": score,
            "action": chosen_suggestion,
        }

        if score < 5:
            priority_actions.append(item)
        elif score < 7.5:
            improvements.append(item)
        else:
            quick_wins.append(item)

    # 生成 SEO 优化总结
    seo_summary = _generate_seo_summary(scores)

    return {
        "priority_actions": priority_actions,
        "improvements": improvements,
        "quick_wins": quick_wins,
        "seo_summary": seo_summary,
        "total_score": scores.get("total_score"),
        "grade": scores.get("grade"),
    }


def _generate_seo_summary(scores: dict) -> str:
    """根据总分生成 SEO 优化总结文字"""
    total = scores.get("total_score", 0)
    grade = scores.get("grade", "D")

    dim_scores = {d["name"]: d["score"] for d in scores.get("dimensions", [])}
    weak_dims = [name for name, s in dim_scores.items() if s < 6]

    if grade == "A":
        return f"当前 Listing 评分 {total} 分（A 级），整体质量优秀。建议重点关注广告投放策略和站外引流，以进一步提升 BSR 排名。"
    elif grade == "B":
        weak_str = "、".join(weak_dims) if weak_dims else "部分细节"
        return f"当前 Listing 评分 {total} 分（B 级），{weak_str} 存在优化空间。优化后预计可提升自然搜索排名 20-40%。"
    elif grade == "C":
        weak_str = "、".join(weak_dims) if weak_dims else "多个维度"
        return f"当前 Listing 评分 {total} 分（C 级），{weak_str} 需要重点改进。建议按优先级逐项优化，预计优化后转化率可提升 30-50%。"
    else:
        return f"当前 Listing 评分 {total} 分（D 级），建议全面重构 Listing。重点先解决标注【紧急】的项目，这些是影响 Amazon 排名和转化的核心因素。"


# ──────────────────────────────────────────────
# AI 重写模块：调用 OpenAI 或返回 Mock 数据
# ──────────────────────────────────────────────

MOCK_REWRITE_RESULT = {
    "optimized_title": (
        "Stainless Steel Water Bottle 32oz - Vacuum Insulated, Keeps Cold 24 Hours & Hot 12 Hours, "
        "BPA-Free Leak-Proof Lid, Wide Mouth, Perfect for Gym, Hiking, Office & Travel (Midnight Black)"
    ),
    "optimized_bullets": [
        "SUPERIOR INSULATION TECHNOLOGY: Double-wall vacuum insulation keeps beverages ice-cold for up to 24 hours "
        "and hot drinks steaming for 12 hours — ideal for all-day hydration whether you're at the gym, hiking trails, "
        "or enduring back-to-back meetings.",

        "PREMIUM 18/8 FOOD-GRADE STAINLESS STEEL: Crafted from pro-grade #304 stainless steel, this bottle is "
        "completely BPA-free, phthalate-free, and toxin-free. No metallic taste, no plastic odor — just pure, "
        "clean refreshment every sip.",

        "LEAK-PROOF ENGINEERED LID: Our reinforced twist-and-lock lid features a triple-seal silicone gasket, "
        "eliminating leaks in any orientation. Toss it in your backpack with confidence — zero spills guaranteed "
        "during commutes, workouts, or travel.",

        "WIDE MOUTH VERSATILITY: The 2.2\" wide-mouth opening accommodates standard ice cubes and is compatible "
        "with most water filters. Effortless to fill, drink from, and clean by hand or dishwasher (lid only). "
        "Fits most car cup holders and standard water bottle pockets.",

        "LIFETIME GUARANTEE & ECO COMMITMENT: Backed by our unconditional lifetime warranty — if it ever leaks "
        "or defects, we replace it, no questions asked. Each bottle replaces 167 single-use plastic bottles annually, "
        "supporting your eco-conscious lifestyle.",
    ],
    "optimized_description": (
        "Stay Hydrated, Stay Focused — All Day, Every Day\n\n"
        "Whether you're crushing a CrossFit session, grinding through a 10-hour workday, or conquering a "
        "weekend trail, your hydration companion should work as hard as you do. Our 32oz Stainless Steel "
        "Water Bottle is engineered for the relentlessly active.\n\n"

        "Why Thousands Choose This Bottle:\n"
        "Our advanced vacuum insulation outperforms standard double-wall bottles by maintaining temperature "
        "longer — verified in independent testing at both 95°F desert heat and 20°F alpine conditions. "
        "The secret lies in our precision laser-welded interior chamber that eliminates micro air gaps "
        "found in lower-quality bottles.\n\n"

        "Built for Real Life:\n"
        "Unlike bottles that look great in photos but fail after a few months, ours is constructed from "
        "medical-grade 18/8 stainless steel with a powder-coat exterior that resists chips, scratches, "
        "and condensation. The ergonomic body fits naturally in your hand during long runs.\n\n"

        "Specifications: Capacity: 32oz (946ml) | Height: 10.8\" | Diameter: 3.5\" | Weight: 13.8oz | "
        "Material: 18/8 Stainless Steel | Lid Type: Wide Mouth Leak-Proof | Compatible with: Standard "
        "ice cubes, fruit infusers, most water filters\n\n"

        "Zero-Risk Purchase: We stand behind every bottle with a lifetime replacement warranty. "
        "Join 50,000+ satisfied customers who've made the switch to sustainable, superior hydration."
    ),
    "optimization_notes": [
        "标题结构优化：品牌词 + 核心产品词 + 核心规格 + 关键属性（4个核心卖点）+ 使用场景 + 颜色变体",
        "关键词自然植入：water bottle、insulated、BPA-free、leak-proof 等高搜索量词均匀分布在标题和 Bullet 中",
        "Bullet 采用 ALL CAPS 开头格式（Amazon 最佳实践），快速传达核心卖点",
        "描述采用故事化开场 + 差异化论据 + 技术规格 + 社会证明的四段式结构",
        "痛点驱动写作：每个 Bullet 都回应了买家的核心顾虑（泡茶漏水？保温不够？不好清洗？）",
    ],
    "is_mock": True,
    "mock_notice": "当前为演示模式（未配置 OpenAI API Key）。真实 API 调用将根据您的具体产品信息生成定制化内容。",
}


def rewrite_with_ai(listing_data: dict) -> dict:
    """
    使用 OpenAI GPT-4 重写 Listing（无 API Key 时返回 mock 数据）

    Args:
        listing_data: 包含 title, bullets, description, category, target_keyword 的字典

    Returns:
        dict with: optimized_title, optimized_bullets, optimized_description,
                   optimization_notes, is_mock
    """
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()

    # 无 API Key 时返回专业 mock 数据，演示效果与真实调用一致
    if not api_key:
        return MOCK_REWRITE_RESULT

    return _call_openai_api(listing_data, api_key)


def _build_prompt(listing_data: dict) -> str:
    """构建发送给 GPT-4 的专业 prompt"""
    title = listing_data.get("title", "")
    bullets = listing_data.get("bullets", [])
    description = listing_data.get("description", "")
    category = listing_data.get("category", "General")
    target_keyword = listing_data.get("target_keyword", "")

    bullets_str = "\n".join(f"- {b}" for b in bullets if b.strip())

    return f"""You are an Amazon SEO specialist with 10 years of experience writing high-converting product listings.

Rewrite the following Amazon listing to maximize both search ranking (A9 algorithm) and conversion rate.

ORIGINAL LISTING:
Category: {category}
Target Keyword: {target_keyword}

Title: {title}

Bullet Points:
{bullets_str}

Description:
{description}

REQUIREMENTS:
1. Title: 150-200 characters, format: [Brand] + [Primary Keyword] + [Key Specs] + [Top 3 Benefits] + [Use Cases] + [Variant]
2. Bullets: Exactly 5 bullets, each 150-250 characters, start with ALL CAPS keyword phrase
3. Description: 1000-1500 characters, storytelling approach: hook → pain point → solution → social proof → CTA
4. Naturally integrate the target keyword 2-3 times across the full listing without stuffing
5. Use sensory and benefit-driven language (customers buy outcomes, not features)
6. Avoid: keyword stuffing, competitor mentions, pricing claims, promotional language, HTML tags (except in description)

OUTPUT FORMAT (JSON):
{{
  "optimized_title": "...",
  "optimized_bullets": ["...", "...", "...", "...", "..."],
  "optimized_description": "...",
  "optimization_notes": ["note1", "note2", "note3"]
}}

Output ONLY the JSON, no explanation."""


def _call_openai_api(listing_data: dict, api_key: str) -> dict:
    """实际调用 OpenAI API"""
    try:
        # 延迟导入，避免未安装 openai 包时报错
        import openai  # type: ignore
        import json

        client = openai.OpenAI(api_key=api_key)
        prompt = _build_prompt(listing_data)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        result = json.loads(content)
        result["is_mock"] = False
        return result

    except ImportError:
        # openai 包未安装，回退到 mock
        fallback = dict(MOCK_REWRITE_RESULT)
        fallback["mock_notice"] = "openai 包未安装（pip install openai），当前为演示模式。"
        return fallback

    except Exception as e:
        fallback = dict(MOCK_REWRITE_RESULT)
        fallback["mock_notice"] = f"API 调用出错（{str(e)[:80]}），当前为演示模式。"
        return fallback
