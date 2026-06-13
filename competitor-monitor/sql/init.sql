-- ============================================================
-- 文件：sql/init.sql
-- 作用：竞品监控系统数据库初始化脚本，创建所有表结构
-- 执行：mysql -u root -p < init.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS competitor_monitor DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE competitor_monitor;

-- ---------------------------------------------------------------
-- 1. 监控商品表：存储所有被监控的 Amazon 商品基础信息
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    id           BIGINT       AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    asin         VARCHAR(20)  NOT NULL UNIQUE COMMENT 'Amazon 商品唯一标识符（10位）',
    title        VARCHAR(500) NOT NULL     COMMENT '商品标题',
    category     VARCHAR(100)              COMMENT '一级类目，如 Electronics',
    sub_category VARCHAR(100)              COMMENT '二级类目，如 Wireless Earbuds',
    brand        VARCHAR(100)              COMMENT '品牌名称',
    created_at   DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '添加监控时间',
    INDEX idx_asin     (asin),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='监控商品基础信息表';

-- ---------------------------------------------------------------
-- 2. 价格历史表：每日价格快照，用于绘制价格走势图
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS price_history (
    id          BIGINT        AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    asin        VARCHAR(20)   NOT NULL COMMENT '关联商品 ASIN',
    price       DECIMAL(10,2) NOT NULL COMMENT '美元售价',
    currency    VARCHAR(10)   DEFAULT 'USD' COMMENT '货币单位',
    recorded_at DATETIME      NOT NULL COMMENT '价格记录时间',
    INDEX idx_asin_time (asin, recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品价格历史快照表';

-- ---------------------------------------------------------------
-- 3. BSR 排名历史表：记录商品在各类目的销量排名变化
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bsr_history (
    id          BIGINT       AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    asin        VARCHAR(20)  NOT NULL COMMENT '关联商品 ASIN',
    bsr_rank    INT          NOT NULL COMMENT 'BSR 排名值，数字越小越好',
    category    VARCHAR(100)          COMMENT '排名所在类目',
    recorded_at DATETIME     NOT NULL COMMENT '排名记录时间',
    INDEX idx_asin_time (asin, recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品 BSR 排名历史表';

-- ---------------------------------------------------------------
-- 4. 评论统计表：追踪评论数量和评分随时间的变化
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS review_stats (
    id           BIGINT       AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    asin         VARCHAR(20)  NOT NULL COMMENT '关联商品 ASIN',
    review_count INT          NOT NULL COMMENT '累计评论总数',
    rating       DECIMAL(2,1) NOT NULL COMMENT '平均评分（1.0 ~ 5.0）',
    recorded_at  DATETIME     NOT NULL COMMENT '记录时间',
    INDEX idx_asin_time (asin, recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品评论数据统计表';

-- ---------------------------------------------------------------
-- 5. 预警记录表：当价格/BSR 变化超过阈值时自动记录
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS alerts (
    id           BIGINT        AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    asin         VARCHAR(20)   NOT NULL COMMENT '触发预警的商品 ASIN',
    alert_type   VARCHAR(50)   NOT NULL COMMENT '预警类型：PRICE_DROP/PRICE_RISE/BSR_IMPROVE/BSR_DROP',
    old_value    DECIMAL(10,2) COMMENT '变化前的数值',
    new_value    DECIMAL(10,2) COMMENT '变化后的数值',
    change_pct   DECIMAL(5,2)  COMMENT '变化百分比（正=上涨，负=下跌）',
    is_read      TINYINT(1)    DEFAULT 0 COMMENT '是否已读：0=未读，1=已读',
    triggered_at DATETIME      NOT NULL COMMENT '预警触发时间',
    INDEX idx_asin      (asin),
    INDEX idx_triggered (triggered_at),
    INDEX idx_unread    (is_read, triggered_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='竞品变动预警记录表';

-- ---------------------------------------------------------------
-- 6. 预警配置表：支持全局默认配置或按 ASIN 单独配置阈值
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS alert_config (
    id             BIGINT       AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    asin           VARCHAR(20)  DEFAULT NULL COMMENT '目标 ASIN（NULL=全局默认配置）',
    price_drop_pct DECIMAL(5,2) DEFAULT 10.00 COMMENT '价格下跌预警阈值（%）',
    price_rise_pct DECIMAL(5,2) DEFAULT 15.00 COMMENT '价格上涨预警阈值（%）',
    bsr_change_pct DECIMAL(5,2) DEFAULT 20.00 COMMENT 'BSR 变动预警阈值（%）',
    updated_at     DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最后修改时间',
    UNIQUE KEY uk_asin (asin)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='预警阈值配置表';

-- 全局默认预警配置（asin 为 NULL 表示全局生效）
INSERT INTO alert_config (asin, price_drop_pct, price_rise_pct, bsr_change_pct)
VALUES (NULL, 10.00, 15.00, 20.00);
