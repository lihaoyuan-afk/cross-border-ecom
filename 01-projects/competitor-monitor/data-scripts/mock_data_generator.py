# ============================================================
# 文件：data-scripts/mock_data_generator.py
# 作用：生成 50 个 3C 商品的 90 天模拟数据并写入 MySQL
# 运行：python mock_data_generator.py
# 依赖：pip install -r requirements.txt
# ============================================================

import pymysql
import numpy as np
import random
import string
from datetime import datetime, timedelta

# ---- 数据库连接配置（请修改密码）----
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',   # 修改为你的 MySQL 密码
    'database': 'competitor_monitor',
    'charset': 'utf8mb4',
}

# ---- 全局参数 ----
NUM_PRODUCTS = 50
NUM_DAYS = 90
PRICE_VOLATILITY = 0.15  # 价格最大波动幅度 ±15%
ALERT_THRESHOLD = 0.10   # 触发预警的价格变化阈值 10%

random.seed(42)
np.random.seed(42)

# ---- 3C 商品类目模板：每个模板生成 10 个商品 ----
PRODUCT_TEMPLATES = [
    {
        'sub_category': 'Wireless Earbuds',
        'brands': ['SoundCore', 'JLab', 'Tozo', 'Mpow', 'Tribit'],
        'title_tpl': '{brand} Wireless Earbuds Bluetooth 5.3 IPX7 Waterproof 48H Playtime',
        'price_range': (19.99, 59.99),
        'bsr_range':   (500, 50000),
        'review_range': (50, 3000),
    },
    {
        'sub_category': 'USB Hubs',
        'brands': ['Anker', 'Sabrent', 'uni', 'Atolla', 'Hiearcool'],
        'title_tpl': '{brand} USB C Hub 7-in-1 Multiport Adapter 4K HDMI USB 3.0 100W PD',
        'price_range': (15.99, 49.99),
        'bsr_range':   (1000, 80000),
        'review_range': (200, 8000),
    },
    {
        'sub_category': 'Phone Cases',
        'brands': ['Spigen', 'ESR', 'DTTO', 'Caseology', 'Ringke'],
        'title_tpl': '{brand} Case for iPhone 15 Pro Military Grade Drop Protection Clear',
        'price_range': (9.99, 29.99),
        'bsr_range':   (200, 30000),
        'review_range': (500, 15000),
    },
    {
        'sub_category': 'Portable Chargers',
        'brands': ['Anker', 'INIU', 'Baseus', 'VRURC', 'Miady'],
        'title_tpl': '{brand} Portable Charger 20000mAh Power Bank PD 22.5W Fast Charging',
        'price_range': (19.99, 45.99),
        'bsr_range':   (300, 40000),
        'review_range': (300, 10000),
    },
    {
        'sub_category': 'Webcams',
        'brands': ['Logitech', 'NexiGo', 'Razer', 'OBSBOT', 'Vitade'],
        'title_tpl': '{brand} 1080P HD Webcam with Noise Canceling Mic Auto Focus for Streaming',
        'price_range': (29.99, 89.99),
        'bsr_range':   (1000, 60000),
        'review_range': (100, 5000),
    },
]


def gen_asin():
    """生成随机 Amazon ASIN（B + 9位大写字母数字）"""
    chars = string.ascii_uppercase + string.digits
    return 'B' + ''.join(random.choices(chars, k=9))


def generate_products():
    """生成 50 个商品基础数据"""
    products = []
    used_asins = set()
    # 每个模板生成 10 个商品
    for tmpl in PRODUCT_TEMPLATES:
        for _ in range(NUM_PRODUCTS // len(PRODUCT_TEMPLATES)):
            asin = gen_asin()
            while asin in used_asins:
                asin = gen_asin()
            used_asins.add(asin)
            brand = random.choice(tmpl['brands'])
            products.append({
                'asin':         asin,
                'title':        tmpl['title_tpl'].format(brand=brand),
                'category':     'Electronics',
                'sub_category': tmpl['sub_category'],
                'brand':        brand,
                'tmpl':         tmpl,  # 保留模板引用，生成历史数据时用
                'created_at':   datetime.now() - timedelta(days=NUM_DAYS),
            })
    return products


def gen_price_history(asin, base_price):
    """
    随机游走模拟 90 天价格波动。
    - 每日变动：正态分布小幅波动，5% 概率触发促销大跌
    - 单日最大变动限制在 ±8%，总体不超出基准价的 60%~130%
    """
    records = []
    start = datetime.now() - timedelta(days=NUM_DAYS)
    price = base_price

    for day in range(1, NUM_DAYS + 1):
        # 5% 概率促销，降价 20%~35%
        if random.random() < 0.05:
            delta = random.uniform(-0.35, -0.20)
        else:
            delta = np.random.normal(0, PRICE_VOLATILITY / 10)

        delta = max(min(delta, 0.08), -0.08)
        price = round(price * (1 + delta), 2)
        price = max(base_price * 0.60, min(price, base_price * 1.30))

        records.append({
            'asin': asin,
            'price': price,
            'recorded_at': start + timedelta(days=day),
        })
    return records


def gen_bsr_history(asin, base_bsr, category):
    """
    模拟 BSR 排名 90 天变化：整体缓慢改善（排名下降），叠加随机噪声。
    BSR 越小越好（1 = 全品类第一）。
    """
    records = []
    start = datetime.now() - timedelta(days=NUM_DAYS)
    rank = base_bsr
    # 整体趋势：90 天改善约 10%
    daily_improve = (base_bsr * 0.10) / NUM_DAYS

    for day in range(1, NUM_DAYS + 1):
        noise = np.random.normal(0, rank * 0.05)
        rank = max(1, int(rank - daily_improve + noise))
        records.append({
            'asin': asin,
            'bsr_rank': rank,
            'category': category,
            'recorded_at': start + timedelta(days=day),
        })
    return records


def gen_review_history(asin, initial_count, initial_rating):
    """
    模拟评论数随时间增长（泊松分布，每天随机新增若干条）。
    评分在初始值附近小幅随机游走，稳定在 3.8~4.9 之间。
    """
    records = []
    start = datetime.now() - timedelta(days=NUM_DAYS)
    count = initial_count
    rating = initial_rating
    daily_avg = random.randint(2, 15)  # 该商品日均新增评论数

    for day in range(1, NUM_DAYS + 1):
        count += int(np.random.poisson(daily_avg))
        rating = round(max(3.8, min(4.9, rating + np.random.normal(0, 0.02))), 1)
        records.append({
            'asin': asin,
            'review_count': count,
            'rating': rating,
            'recorded_at': start + timedelta(days=day),
        })
    return records


def gen_alerts(all_price_records):
    """
    扫描价格历史，生成预警记录。
    相邻两天价格变化超过 ALERT_THRESHOLD（10%）时触发。
    """
    alerts = []
    # 按 ASIN 分组
    by_asin = {}
    for r in all_price_records:
        by_asin.setdefault(r['asin'], []).append(r)

    for asin, records in by_asin.items():
        records.sort(key=lambda x: x['recorded_at'])
        for i in range(1, len(records)):
            old_p = records[i - 1]['price']
            new_p = records[i]['price']
            pct = (new_p - old_p) / old_p

            if abs(pct) >= ALERT_THRESHOLD:
                alerts.append({
                    'asin':         asin,
                    'alert_type':   'PRICE_DROP' if pct < 0 else 'PRICE_RISE',
                    'old_value':    old_p,
                    'new_value':    new_p,
                    'change_pct':   round(pct * 100, 2),
                    'is_read':      random.choice([0, 0, 0, 1]),  # 75% 未读
                    'triggered_at': records[i]['recorded_at'],
                })
    return alerts


def batch_insert(cursor, sql, data, batch_size=1000):
    """分批批量插入，避免单次数据量过大"""
    for i in range(0, len(data), batch_size):
        cursor.executemany(sql, data[i:i + batch_size])


def write_to_db(conn, products, price_records, bsr_records, review_records, alerts):
    """将所有模拟数据写入 MySQL"""
    cur = conn.cursor()

    print('  写入商品基础数据...')
    batch_insert(cur,
        'INSERT INTO products (asin,title,category,sub_category,brand,created_at) '
        'VALUES (%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE title=VALUES(title)',
        [(p['asin'], p['title'], p['category'], p['sub_category'],
          p['brand'], p['created_at']) for p in products]
    )
    print(f'    ✓ {len(products)} 条')

    print('  写入价格历史...')
    batch_insert(cur,
        'INSERT INTO price_history (asin,price,recorded_at) VALUES (%s,%s,%s)',
        [(r['asin'], r['price'], r['recorded_at']) for r in price_records]
    )
    print(f'    ✓ {len(price_records)} 条')

    print('  写入 BSR 历史...')
    batch_insert(cur,
        'INSERT INTO bsr_history (asin,bsr_rank,category,recorded_at) VALUES (%s,%s,%s,%s)',
        [(r['asin'], r['bsr_rank'], r['category'], r['recorded_at']) for r in bsr_records]
    )
    print(f'    ✓ {len(bsr_records)} 条')

    print('  写入评论数据...')
    batch_insert(cur,
        'INSERT INTO review_stats (asin,review_count,rating,recorded_at) VALUES (%s,%s,%s,%s)',
        [(r['asin'], r['review_count'], r['rating'], r['recorded_at']) for r in review_records]
    )
    print(f'    ✓ {len(review_records)} 条')

    print('  写入预警记录...')
    batch_insert(cur,
        'INSERT INTO alerts (asin,alert_type,old_value,new_value,change_pct,is_read,triggered_at) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s)',
        [(a['asin'], a['alert_type'], a['old_value'], a['new_value'],
          a['change_pct'], a['is_read'], a['triggered_at']) for a in alerts]
    )
    print(f'    ✓ {len(alerts)} 条')

    conn.commit()
    cur.close()


def main():
    print('=' * 55)
    print('跨境电商竞品监控系统 —— 模拟数据生成器')
    print('=' * 55)

    print('\n[1/4] 生成商品基础数据...')
    products = generate_products()

    print('\n[2/4] 生成 90 天历史数据...')
    price_records, bsr_records, review_records = [], [], []
    for p in products:
        tmpl = p['tmpl']
        base_price   = round(random.uniform(*tmpl['price_range']), 2)
        base_bsr     = random.randint(*tmpl['bsr_range'])
        init_reviews = random.randint(*tmpl['review_range'])
        init_rating  = round(random.uniform(3.9, 4.7), 1)

        price_records.extend(gen_price_history(p['asin'], base_price))
        bsr_records.extend(gen_bsr_history(p['asin'], base_bsr, p['category']))
        review_records.extend(gen_review_history(p['asin'], init_reviews, init_rating))

    print(f'  价格记录：{len(price_records)} 条')
    print(f'  BSR 记录：{len(bsr_records)} 条')
    print(f'  评论记录：{len(review_records)} 条')

    print('\n[3/4] 生成预警记录...')
    alerts = gen_alerts(price_records)
    print(f'  触发预警：{len(alerts)} 条')

    print('\n[4/4] 写入 MySQL...')
    try:
        conn = pymysql.connect(**DB_CONFIG)
        write_to_db(conn, products, price_records, bsr_records, review_records, alerts)
        conn.close()
        print('\n✅ 数据生成完成！')
    except pymysql.Error as e:
        print(f'\n❌ 数据库连接失败：{e}')
        print('请检查 DB_CONFIG 中的配置是否正确，并确认已执行 sql/init.sql')


if __name__ == '__main__':
    main()
