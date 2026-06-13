"""
Amazon Listing 优化引擎 - Flask 后端
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from scorer import score_listing
from ai_optimizer import generate_suggestions, rewrite_with_ai

app = Flask(__name__)
CORS(app)  # 允许 Vue 开发服务器跨域


def _parse_listing(data: dict) -> dict:
    """统一解析前端传入的 listing 数据，附带默认值"""
    bullets_raw = data.get("bullets", [])
    # 支持字符串（换行分隔）或数组两种格式
    if isinstance(bullets_raw, str):
        bullets = [b.strip() for b in bullets_raw.split("\n") if b.strip()]
    else:
        bullets = [str(b).strip() for b in bullets_raw if str(b).strip()]

    return {
        "title": str(data.get("title", "")).strip(),
        "bullets": bullets,
        "description": str(data.get("description", "")).strip(),
        "image_count": int(data.get("image_count", 0)),
        "price": float(data.get("price", 0)),
        "avg_category_price": float(data.get("avg_category_price", 0)),
        "review_count": int(data.get("review_count", 0)),
        "category": str(data.get("category", "General")).strip(),
        "target_keyword": str(data.get("target_keyword", "")).strip(),
    }


@app.route("/api/score", methods=["POST"])
def api_score():
    """
    提交 Listing 数据，返回 8 维评分结果

    Request body:
        title, bullets, description, image_count,
        price, avg_category_price, review_count

    Response:
        dimensions: 各维度详情
        total_score: 加权总分 (0-100)
        grade: A/B/C/D
        summary: 总体评价
    """
    data = request.get_json(silent=True) or {}
    listing = _parse_listing(data)

    if not listing["title"]:
        return jsonify({"error": "标题不能为空"}), 400

    result = score_listing(
        title=listing["title"],
        bullets=listing["bullets"],
        description=listing["description"],
        image_count=listing["image_count"],
        price=listing["price"],
        avg_category_price=listing["avg_category_price"],
        review_count=listing["review_count"],
    )
    return jsonify(result)


@app.route("/api/optimize", methods=["POST"])
def api_optimize():
    """
    获取基于规则的中文优化建议

    Request body: 同 /api/score

    Response:
        priority_actions: 高优先级（得分<5）
        improvements: 中优先级（5-7.5）
        quick_wins: 低优先级（7.5-9）
        seo_summary: SEO 总结
    """
    data = request.get_json(silent=True) or {}
    listing = _parse_listing(data)

    if not listing["title"]:
        return jsonify({"error": "标题不能为空"}), 400

    scores = score_listing(
        title=listing["title"],
        bullets=listing["bullets"],
        description=listing["description"],
        image_count=listing["image_count"],
        price=listing["price"],
        avg_category_price=listing["avg_category_price"],
        review_count=listing["review_count"],
    )

    suggestions = generate_suggestions(listing, scores)
    return jsonify(suggestions)


@app.route("/api/rewrite", methods=["POST"])
def api_rewrite():
    """
    AI 重写 Listing（有 OpenAI Key 时真实调用，否则返回 mock 数据）

    Request body: 同 /api/score，额外支持 category, target_keyword

    Response:
        optimized_title, optimized_bullets, optimized_description,
        optimization_notes, is_mock
    """
    data = request.get_json(silent=True) or {}
    listing = _parse_listing(data)

    if not listing["title"]:
        return jsonify({"error": "标题不能为空"}), 400

    result = rewrite_with_ai(listing)
    return jsonify(result)


@app.route("/api/health", methods=["GET"])
def health():
    import os
    return jsonify({
        "status": "ok",
        "ai_mode": "real" if os.environ.get("OPENAI_API_KEY") else "mock",
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
