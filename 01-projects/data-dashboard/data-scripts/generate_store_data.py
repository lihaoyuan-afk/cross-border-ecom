"""
跨境电商数据看板 - 模拟数据生成脚本
生成 2024-01-01 到 2024-06-30 共 180 天的模拟店铺数据
并写入 MySQL 数据库

依赖安装：pip install mysql-connector-python
"""

import mysql.connector
from datetime import datetime, timedelta
import random
import math

# ============================================================
# 数据库连接配置（根据本地环境修改）
# ============================================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root123',
    'database': 'data_dashboard',
    'charset': 'utf8mb4'
}

# ============================================================
# 日期范围配置
# ============================================================
START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 6, 30)
TOTAL_DAYS = (END_DATE - START_DATE).days + 1  # 181 天

# ============================================================
# 促销节点配置：日期 -> 销售倍增系数
# 模拟电商平台的大促节点峰值
# ============================================================
PROMO_EVENTS = {
    # 情人节大促（2月11日-16日，14日峰值 ×2.2）
    '2024-02-11': 1.4,
    '2024-02-12': 1.6,
    '2024-02-13': 1.9,
    '2024-02-14': 2.2,  # 情人节当天
    '2024-02-15': 1.7,
    '2024-02-16': 1.3,

    # 女神节大促（3月7日-9日，8日峰值 ×2.0）
    '2024-03-07': 1.4,
    '2024-03-08': 2.0,  # 女神节当天
    '2024-03-09': 1.5,

    # 618 年中大促（6月15日-18日，18日峰值 ×3.0）
    '2024-06-14': 1.2,
    '2024-06-15': 1.5,
    '2024-06-16': 1.9,
    '2024-06-17': 2.5,
    '2024-06-18': 3.0,  # 618 当天
    '2024-06-19': 1.6,
    '2024-06-20': 1.2,
}


def get_daily_multiplier(date: datetime) -> float:
    """
    计算某日的销售系数
    综合考虑：促销节点 > 周末效应 > 普通工作日
    """
    date_str = date.strftime('%Y-%m-%d')

    # 优先检查是否为促销节点
    if date_str in PROMO_EVENTS:
        return PROMO_EVENTS[date_str]

    # 周末效应（周六=5，周日=6）：流量和销量更高
    if date.weekday() >= 5:
        return random.uniform(1.2, 1.4)

    # 普通工作日：基准系数
    return 1.0


def generate_daily_sales() -> list[dict]:
    """
    生成每日销售数据
    - 基础日销售额：5000元，随时间增长约30%（模拟店铺成长期）
    - 加入 ±15% 的随机波动模拟自然波动
    - 退款率：1%~5%，促销期略高
    """
    records = []
    base_revenue = 5000.0  # 元

    current = START_DATE
    while current <= END_DATE:
        days_elapsed = (current - START_DATE).days

        # 成长趋势：6个月内线性增长30%
        growth_trend = 1.0 + (days_elapsed / (TOTAL_DAYS - 1)) * 0.30

        # 促销/周末系数
        multiplier = get_daily_multiplier(current)

        # 随机波动 ±15%
        noise = random.uniform(0.85, 1.15)

        revenue = base_revenue * growth_trend * multiplier * noise
        revenue = round(revenue, 2)

        # 客单价：65~95元之间随机（促销期间略低，因为有折扣）
        if multiplier > 1.5:
            avg_order = random.uniform(58, 80)   # 大促期间促销价，客单价稍低
        else:
            avg_order = random.uniform(68, 95)

        orders = max(1, int(revenue / avg_order))
        avg_order_value = round(revenue / orders, 2)

        # 退款率：促销期间因冲动消费退款率较高
        if multiplier > 1.8:
            refund_rate = random.uniform(0.03, 0.07)
        else:
            refund_rate = random.uniform(0.01, 0.04)

        refund_count = max(0, int(orders * refund_rate))

        records.append({
            'date': current.strftime('%Y-%m-%d'),
            'revenue': revenue,
            'orders': orders,
            'avg_order_value': avg_order_value,
            'refund_count': refund_count,
        })

        current += timedelta(days=1)

    print(f"  销售数据：生成 {len(records)} 条记录")
    return records


def generate_ad_performance(sales_records: list[dict]) -> list[dict]:
    """
    生成广告表现数据（与销售数据联动）
    - 广告花费：占当日销售额的 15%~25%
    - ACoS 目标区间：20%~35%（行业合理范围）
    - CTR：1.5%~3.5%
    - 促销期间加大投放，ACoS 可能略高
    """
    records = []

    for sale in sales_records:
        date_str = sale['date']
        multiplier = PROMO_EVENTS.get(date_str, 1.0)

        # 促销期间加大广告预算
        if multiplier > 1.5:
            spend_ratio = random.uniform(0.22, 0.32)   # 促销期：22%~32%
            acos        = random.uniform(0.25, 0.38)   # 促销期 ACoS 略高（冲量）
        else:
            spend_ratio = random.uniform(0.15, 0.24)   # 常规：15%~24%
            acos        = random.uniform(0.20, 0.33)   # 常规 ACoS：20%~33%

        ad_spend   = round(sale['revenue'] * spend_ratio, 2)
        ad_revenue = round(ad_spend / acos, 2)  # 由 ACoS 反推广告销售额

        # 曝光量：每元花费约产生 800~1200 次曝光（CPM 约 0.8~1.2 元/千次）
        cpm_cost      = random.uniform(0.8, 1.2)          # 每千次曝光成本（元）
        impressions   = int(ad_spend / cpm_cost * 1000)

        # 点击率 CTR：1.5%~3.5%
        ctr    = random.uniform(0.015, 0.035)
        clicks = max(1, int(impressions * ctr))

        records.append({
            'date':        date_str,
            'ad_spend':    ad_spend,
            'impressions': impressions,
            'clicks':      clicks,
            'ad_revenue':  ad_revenue,
        })

    print(f"  广告数据：生成 {len(records)} 条记录")
    return records


def generate_traffic_stats(sales_records: list[dict]) -> list[dict]:
    """
    生成流量统计数据
    - 会话数与订单量正相关（由转化率反推）
    - 转化率：2%~5%（行业平均约3%）
    - 页面浏览量 = 会话数 × 每会话浏览页数（1.5~2.8）
    - 自然流量加入额外随机性：±20%
    """
    records = []

    for sale in sales_records:
        # 转化率：促销期间更高（活动引流精准）
        date_str   = sale['date']
        multiplier = PROMO_EVENTS.get(date_str, 1.0)

        if multiplier > 1.5:
            conversion_rate = random.uniform(0.038, 0.065)  # 促销期转化率更高
        else:
            conversion_rate = random.uniform(0.020, 0.045)  # 常规转化率

        # 由实际订单量反推会话数
        conversions = sale['orders']
        sessions_base = int(conversions / conversion_rate)

        # 叠加自然流量随机性（SEO、社媒等带来的波动）
        natural_noise = random.uniform(0.85, 1.20)
        sessions      = int(sessions_base * natural_noise)
        sessions      = max(sessions, conversions + 10)  # 会话数必须 >= 转化数

        # 页面浏览量：平均每会话浏览 1.5~2.8 个页面
        pages_per_session = random.uniform(1.5, 2.8)
        page_views        = int(sessions * pages_per_session)

        records.append({
            'date':        date_str,
            'sessions':    sessions,
            'page_views':  page_views,
            'conversions': conversions,
        })

    print(f"  流量数据：生成 {len(records)} 条记录")
    return records


def generate_inventory() -> list[dict]:
    """
    生成库存数据（5个 SKU）
    模拟真实情况：
    - SKU-003 智能手表：库存偏低，处于预警状态（剩余 3 天）
    - SKU-005 扩展坞：已断货（库存为 0）
    - 其余 SKU 库存健康
    """
    products = [
        {
            'sku':              'SKU-001',
            'product_name':     '无线蓝牙耳机 Pro',
            'stock_qty':        456,
            'daily_sales_avg':  8.5,
            'alert_threshold':  30,
        },
        {
            'sku':              'SKU-002',
            'product_name':     '便携充电宝 20000mAh',
            'stock_qty':        285,
            'daily_sales_avg':  5.2,
            'alert_threshold':  25,
        },
        {
            'sku':              'SKU-003',
            'product_name':     '智能手表运动版',
            'stock_qty':        11,    # ⚠ 可销天数 ≈ 2.9天，低于预警阈值
            'daily_sales_avg':  3.8,
            'alert_threshold':  20,
        },
        {
            'sku':              'SKU-004',
            'product_name':     '手机防摔保护壳',
            'stock_qty':        830,
            'daily_sales_avg':  15.3,
            'alert_threshold':  45,
        },
        {
            'sku':              'SKU-005',
            'product_name':     'USB-C 多功能扩展坞',
            'stock_qty':        0,     # ⛔ 已断货
            'daily_sales_avg':  6.1,
            'alert_threshold':  30,
        },
    ]

    print(f"  库存数据：生成 {len(products)} 个SKU")
    return products


# ============================================================
# 数据库操作函数
# ============================================================

def get_connection():
    """建立数据库连接"""
    return mysql.connector.connect(**DB_CONFIG)


def clear_tables(conn):
    """清空所有数据表（方便重复运行脚本）"""
    cursor = conn.cursor()
    tables = ['daily_sales', 'ad_performance', 'traffic_stats', 'inventory']
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
        print(f"  已清空表：{table}")
    conn.commit()
    cursor.close()


def insert_daily_sales(conn, records: list[dict]):
    """批量插入每日销售数据"""
    sql = """
        INSERT INTO daily_sales (date, revenue, orders, avg_order_value, refund_count)
        VALUES (%(date)s, %(revenue)s, %(orders)s, %(avg_order_value)s, %(refund_count)s)
    """
    cursor = conn.cursor()
    cursor.executemany(sql, records)
    conn.commit()
    print(f"  ✓ daily_sales 写入 {cursor.rowcount} 条")
    cursor.close()


def insert_ad_performance(conn, records: list[dict]):
    """批量插入广告表现数据"""
    sql = """
        INSERT INTO ad_performance (date, ad_spend, impressions, clicks, ad_revenue)
        VALUES (%(date)s, %(ad_spend)s, %(impressions)s, %(clicks)s, %(ad_revenue)s)
    """
    cursor = conn.cursor()
    cursor.executemany(sql, records)
    conn.commit()
    print(f"  ✓ ad_performance 写入 {cursor.rowcount} 条")
    cursor.close()


def insert_traffic_stats(conn, records: list[dict]):
    """批量插入流量统计数据"""
    sql = """
        INSERT INTO traffic_stats (date, sessions, page_views, conversions)
        VALUES (%(date)s, %(sessions)s, %(page_views)s, %(conversions)s)
    """
    cursor = conn.cursor()
    cursor.executemany(sql, records)
    conn.commit()
    print(f"  ✓ traffic_stats 写入 {cursor.rowcount} 条")
    cursor.close()


def insert_inventory(conn, records: list[dict]):
    """插入库存数据（使用 REPLACE INTO 支持重复运行）"""
    sql = """
        REPLACE INTO inventory (sku, product_name, stock_qty, daily_sales_avg, alert_threshold)
        VALUES (%(sku)s, %(product_name)s, %(stock_qty)s, %(daily_sales_avg)s, %(alert_threshold)s)
    """
    cursor = conn.cursor()
    cursor.executemany(sql, records)
    conn.commit()
    print(f"  ✓ inventory 写入 {cursor.rowcount} 条")
    cursor.close()


def print_data_summary(sales, ads, traffic, inventory_data):
    """打印数据摘要，方便验证"""
    total_revenue = sum(r['revenue'] for r in sales)
    total_orders  = sum(r['orders'] for r in sales)
    total_spend   = sum(r['ad_spend'] for r in ads)
    total_revenue_ad = sum(r['ad_revenue'] for r in ads)
    avg_acos      = total_spend / total_revenue_ad if total_revenue_ad > 0 else 0

    print("\n" + "=" * 50)
    print("📊 数据摘要（2024-01-01 至 2024-06-30）")
    print("=" * 50)
    print(f"  总销售额：    ¥{total_revenue:>12,.2f}")
    print(f"  总订单量：    {total_orders:>12,} 单")
    print(f"  总广告花费：  ¥{total_spend:>12,.2f}")
    print(f"  整体 ACoS：   {avg_acos * 100:>11.1f}%")
    print(f"  总会话数：    {sum(r['sessions'] for r in traffic):>12,}")
    print(f"  库存 SKU 数量：{len(inventory_data):>11}")
    print("=" * 50)


# ============================================================
# 主函数入口
# ============================================================

def main():
    random.seed(42)  # 固定随机种子，保证每次生成的数据一致

    print("🚀 开始生成模拟数据...")
    print(f"   时间范围：{START_DATE.date()} ~ {END_DATE.date()}（共 {TOTAL_DAYS} 天）\n")

    # 1. 生成数据
    print("📦 生成各模块数据：")
    sales_data     = generate_daily_sales()
    ad_data        = generate_ad_performance(sales_data)
    traffic_data   = generate_traffic_stats(sales_data)
    inventory_data = generate_inventory()

    # 2. 打印摘要
    print_data_summary(sales_data, ad_data, traffic_data, inventory_data)

    # 3. 连接数据库并写入
    print("\n💾 连接数据库并写入数据...")
    try:
        conn = get_connection()
        print("  数据库连接成功")

        # 清空旧数据
        print("\n  清空旧数据：")
        clear_tables(conn)

        # 写入新数据
        print("\n  写入新数据：")
        insert_daily_sales(conn, sales_data)
        insert_ad_performance(conn, ad_data)
        insert_traffic_stats(conn, traffic_data)
        insert_inventory(conn, inventory_data)

        conn.close()
        print("\n✅ 数据生成完成！可以启动后端服务查看看板数据。")

    except mysql.connector.Error as e:
        print(f"\n❌ 数据库错误：{e}")
        print("   请检查 DB_CONFIG 中的连接参数是否正确")
        raise


if __name__ == '__main__':
    main()
