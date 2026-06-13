-- ============================================================
-- 跨境电商数据看板 - 数据库初始化脚本
-- 数据库: MySQL 8.0+
-- ============================================================

CREATE DATABASE IF NOT EXISTS data_dashboard
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE data_dashboard;

-- ------------------------------------------------------------
-- 每日销售数据表
-- 记录每天的销售额、订单量、客单价、退款数
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS daily_sales (
    id            BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    date          DATE           NOT NULL            COMMENT '统计日期',
    revenue       DECIMAL(12, 2) NOT NULL            COMMENT '销售额（元）',
    orders        INT            NOT NULL DEFAULT 0  COMMENT '订单量',
    avg_order_value DECIMAL(10, 2) NOT NULL          COMMENT '客单价（元）',
    refund_count  INT            NOT NULL DEFAULT 0  COMMENT '退款笔数',
    created_at    TIMESTAMP      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_date (date)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '每日销售数据';

-- ------------------------------------------------------------
-- 广告表现数据表
-- 记录每天的广告花费、曝光量、点击量、广告带来的销售额
-- ACoS = ad_spend / ad_revenue × 100%
-- ROAS = ad_revenue / ad_spend
-- CTR  = clicks / impressions × 100%
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ad_performance (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    date        DATE           NOT NULL            COMMENT '统计日期',
    ad_spend    DECIMAL(10, 2) NOT NULL            COMMENT '广告花费（元）',
    impressions INT            NOT NULL DEFAULT 0  COMMENT '广告曝光量（次）',
    clicks      INT            NOT NULL DEFAULT 0  COMMENT '广告点击量（次）',
    ad_revenue  DECIMAL(12, 2) NOT NULL            COMMENT '广告带来的销售额（元）',
    created_at  TIMESTAMP      DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_date (date)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '广告表现数据';

-- ------------------------------------------------------------
-- 流量统计数据表
-- 记录每天的访客会话数、页面浏览量、成单转化数
-- 转化率 = conversions / sessions × 100%
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS traffic_stats (
    id          BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    date        DATE  NOT NULL           COMMENT '统计日期',
    sessions    INT   NOT NULL DEFAULT 0 COMMENT '会话数（独立访客）',
    page_views  INT   NOT NULL DEFAULT 0 COMMENT '页面浏览量（PV）',
    conversions INT   NOT NULL DEFAULT 0 COMMENT '转化数（成单数）',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_date (date)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '流量统计数据';

-- ------------------------------------------------------------
-- 库存数据表
-- 记录每个SKU的当前库存、日均销量和预警阈值
-- 库存可销天数 = stock_qty / daily_sales_avg
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS inventory (
    id               BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    sku              VARCHAR(50)    NOT NULL            COMMENT 'SKU编码',
    product_name     VARCHAR(200)   NOT NULL            COMMENT '商品名称',
    stock_qty        INT            NOT NULL DEFAULT 0  COMMENT '当前库存数量（件）',
    daily_sales_avg  DECIMAL(8, 2)  NOT NULL DEFAULT 0  COMMENT '近30天日均销量',
    alert_threshold  INT            NOT NULL DEFAULT 30 COMMENT '预警阈值（低于此可销天数触发预警）',
    updated_at       TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
                                    ON UPDATE CURRENT_TIMESTAMP COMMENT '最后更新时间',
    UNIQUE KEY uk_sku (sku)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '库存数据';
