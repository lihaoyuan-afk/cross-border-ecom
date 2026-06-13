package com.ecom.monitor.dto;

import lombok.Data;
import java.math.BigDecimal;

/** 首页看板汇总数据 */
@Data
public class DashboardOverviewDTO {

    /** 总监控商品数 */
    private Long totalProducts;

    /** 今日触发预警数 */
    private Long todayAlerts;

    /** 未读预警总数 */
    private Long unreadAlerts;

    /** 过去 7 天价格平均变化率（%，负=下跌） */
    private BigDecimal avgPriceChangePct;

    /** 近 24 小时价格下跌预警数 */
    private Long recentPriceDrops;
}
