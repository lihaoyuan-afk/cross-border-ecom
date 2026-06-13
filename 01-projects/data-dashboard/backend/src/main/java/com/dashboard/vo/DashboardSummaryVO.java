package com.dashboard.vo;

import lombok.Data;

import java.math.BigDecimal;

/**
 * 看板核心指标汇总 VO
 * 包含销售、广告、流量三大模块的关键指标及环比变化
 */
@Data
public class DashboardSummaryVO {

    // ── 销售模块 ──────────────────────────────────────
    /** 时间段内总销售额（元） */
    private BigDecimal totalRevenue;

    /** 时间段内总订单量 */
    private Integer totalOrders;

    /** 平均客单价（元） */
    private BigDecimal avgOrderValue;

    /** 退款率（退款数/总订单数） */
    private BigDecimal refundRate;

    // ── 广告模块 ──────────────────────────────────────
    /** 总广告花费（元） */
    private BigDecimal totalAdSpend;

    /** 平均 ACoS = 广告花费 / 广告销售额 */
    private BigDecimal avgAcos;

    /** 平均 ROAS = 广告销售额 / 广告花费 */
    private BigDecimal avgRoas;

    /** 平均 CTR = 点击量 / 曝光量 */
    private BigDecimal avgCtr;

    // ── 流量模块 ──────────────────────────────────────
    /** 总会话数 */
    private Integer totalSessions;

    /** 整体转化率 = 总成单数 / 总会话数 */
    private BigDecimal conversionRate;

    /** 总页面浏览量 */
    private Integer totalPageViews;

    // ── 环比变化（与上一个相同时长周期对比）──────────
    /** 销售额环比变化率（正值表示上涨，负值下跌） */
    private BigDecimal revenueChange;

    /** 订单量环比变化率 */
    private BigDecimal ordersChange;

    /** ACoS 环比变化率（正值表示 ACoS 上升，即效果变差） */
    private BigDecimal acosChange;

    /** 转化率环比变化率 */
    private BigDecimal conversionRateChange;
}
