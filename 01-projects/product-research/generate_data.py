"""
Amazon 选品分析 - 模拟数据生成脚本
生成包含 200 个 Amazon 产品的模拟数据集并保存为 CSV
运行：python generate_data.py
"""

import random
import math
import csv
import os
from datetime import datetime, timedelta

random.seed(2024)

# ── 类目配置 ────────────────────────────────────────────────
CATEGORIES = {
    "无线耳机": {
        "price_range": (15, 80),
        "bsr_range": (1, 8000),
        "brands": ["SoundPro", "AuraTech", "BassBoom", "WaveSound", "ClearAudio"],
        "title_templates": [
            "{brand} Wireless Earbuds Bluetooth 5.3 with {feat} - {color}",
            "{brand} TWS Bluetooth Headphones {feat} IPX7 Waterproof",
            "Wireless Earbuds {feat} 40H Playtime Active Noise Cancelling - {color}",
        ],
    },
    "手机支架": {
        "price_range": (8, 35),
        "bsr_range": (50, 15000),
        "brands": ["GripMax", "MobiMount", "FlexiHold", "StandPro", "QuickClip"],
        "title_templates": [
            "{brand} Phone Mount for Car {feat} 360° Rotation Dashboard Holder",
            "Universal Car Phone Holder {feat} Strong Suction Cup - {brand}",
            "{brand} Desk Phone Stand {feat} Adjustable Height for iPhone Android",
        ],
    },
    "智能家居": {
        "price_range": (12, 60),
        "bsr_range": (500, 20000),
        "brands": ["SmartLink", "HomeIQ", "NexaHome", "EcoSmart", "LumiPro"],
        "title_templates": [
            "{brand} Smart Plug WiFi Outlet {feat} Works with Alexa Google Home",
            "{brand} LED Smart Bulb {feat} 16 Million Colors Voice Control",
            "Smart Power Strip {feat} 4 USB Ports Surge Protector - {brand}",
        ],
    },
    "运动水壶": {
        "price_range": (10, 45),
        "bsr_range": (200, 12000),
        "brands": ["HydroFlow", "PeakSip", "AquaFit", "TrailDrop", "ClearPeak"],
        "title_templates": [
            "{brand} Insulated Water Bottle {feat} Stainless Steel BPA Free",
            "{brand} Sports Water Bottle {feat} Leak-Proof Lid 32oz - {color}",
            "Motivational Water Bottle {feat} with Time Marker 64oz - {brand}",
        ],
    },
}

FEATURES = [
    "Deep Bass", "Touch Control", "Fast Charging", "Magnetic Charging",
    "Auto-Pairing", "Foldable Design", "Built-in Mic", "LED Display",
    "Ergonomic Design", "One-Step Setup", "Wide Compatibility",
    "Premium Sound Quality",
]

COLORS = ["Black", "White", "Navy Blue", "Rose Gold", "Forest Green", "Midnight Gray"]


def bsr_to_monthly_sales(bsr: int, category: str) -> int:
    """根据 BSR 估算月销量（参考行业经验公式）"""
    base_map = {
        "无线耳机":  12000,
        "手机支架":  8000,
        "智能家居":  6000,
        "运动水壶":  9000,
    }
    base = base_map.get(category, 8000)
    # 销量 ≈ base / BSR^0.55，BSR 越低销量越高
    monthly = int(base / math.pow(bsr, 0.55))
    # 加入 ±20% 随机波动
    return max(1, int(monthly * random.uniform(0.8, 1.2)))


def generate_asin() -> str:
    return "B0" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))


def generate_products(n: int = 200) -> list[dict]:
    products = []
    per_category = n // len(CATEGORIES)

    for category, cfg in CATEGORIES.items():
        for _ in range(per_category):
            brand = random.choice(cfg["brands"])
            feat = random.choice(FEATURES)
            color = random.choice(COLORS)
            template = random.choice(cfg["title_templates"])
            title = template.format(brand=brand, feat=feat, color=color)

            price = round(random.uniform(*cfg["price_range"]), 2)
            bsr = random.randint(*cfg["bsr_range"])
            rating = round(random.uniform(3.5, 5.0), 1)
            # 高 BSR 商品评价数少，低 BSR 评价数多
            review_base = max(5, int(5000 / math.sqrt(bsr)))
            reviews = int(review_base * random.uniform(0.5, 2.5))

            monthly_sales = bsr_to_monthly_sales(bsr, category)
            monthly_revenue = round(monthly_sales * price, 2)

            # 上架时间：6个月~3年前
            days_ago = random.randint(180, 1095)
            listed_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

            products.append({
                "asin":           generate_asin(),
                "title":          title,
                "brand":          brand,
                "category":       category,
                "price":          price,
                "bsr":            bsr,
                "rating":         rating,
                "reviews":        reviews,
                "monthly_sales":  monthly_sales,
                "monthly_revenue": monthly_revenue,
                "listed_date":    listed_date,
            })

    random.shuffle(products)
    return products


def score_product(row: dict) -> float:
    """
    选品综合评分（0~100）
    维度：BSR 排名、评价数、评分、月销售额、价格合理性
    """
    # BSR 分（40%）：排名越低分越高，以类目最大 BSR 归一化
    bsr_max = 20000
    bsr_score = max(0, 1 - row["bsr"] / bsr_max) * 100

    # 评价数分（20%）：50~500 最佳，太少不稳定，太多竞争大
    rv = row["reviews"]
    if rv < 50:
        review_score = rv / 50 * 60
    elif rv <= 500:
        review_score = 60 + (rv - 50) / 450 * 40
    elif rv <= 2000:
        review_score = 100 - (rv - 500) / 1500 * 30
    else:
        review_score = max(20, 70 - (rv - 2000) / 500 * 5)

    # 评分分（20%）
    rating_score = (row["rating"] - 1) / 4 * 100

    # 月销售额分（10%）：越高越好，上限 $15000
    revenue_score = min(100, row["monthly_revenue"] / 15000 * 100)

    # 价格区间分（10%）：$15~$50 是跨境电商最优区间
    p = row["price"]
    if 15 <= p <= 50:
        price_score = 100
    elif p < 15:
        price_score = p / 15 * 80
    else:
        price_score = max(20, 100 - (p - 50) / 30 * 50)

    total = (
        bsr_score    * 0.40 +
        review_score * 0.20 +
        rating_score * 0.20 +
        revenue_score * 0.10 +
        price_score  * 0.10
    )
    return round(total, 1)


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "amazon_products.csv")

    products = generate_products(200)
    for p in products:
        p["score"] = score_product(p)

    fieldnames = [
        "asin", "title", "brand", "category", "price",
        "bsr", "rating", "reviews", "monthly_sales",
        "monthly_revenue", "listed_date", "score",
    ]

    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print(f"[OK] Generated {len(products)} products -> {out_path}")
    scores = [p["score"] for p in products]
    print(f"     score: min={min(scores):.1f}  avg={sum(scores)/len(scores):.1f}  max={max(scores):.1f}")


if __name__ == "__main__":
    main()
