package com.dashboard.vo;

import lombok.Data;

import java.math.BigDecimal;

/** 流量漏斗数据（漏斗图用） */
@Data
public class TrafficFunnelVO {

    /** 第一层：总会话数 */
    private Integer totalSessions;

    /** 第二层：总页面浏览量 */
    private Integer totalPageViews;

    /** 第三层：总成单数（转化） */
    private Integer totalConversions;

    /** 会话 → 页面浏览率 */
    private BigDecimal sessionToPageViewRate;

    /** 页面浏览 → 成单转化率 */
    private BigDecimal pageViewToConversionRate;

    /** 整体转化率（会话 → 成单） */
    private BigDecimal overallConversionRate;
}
