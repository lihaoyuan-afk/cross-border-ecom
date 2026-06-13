package com.dashboard.vo;

import lombok.Data;

import java.math.BigDecimal;

/** 广告表现数据项（折线图 + 表格用） */
@Data
public class AdsPerformanceVO {

    /** 日期（yyyy-MM-dd） */
    private String date;

    /** 广告花费（元） */
    private BigDecimal adSpend;

    /** 曝光量 */
    private Integer impressions;

    /** 点击量 */
    private Integer clicks;

    /** 广告销售额（元） */
    private BigDecimal adRevenue;

    /** ACoS = ad_spend / ad_revenue */
    private BigDecimal acos;

    /** ROAS = ad_revenue / ad_spend */
    private BigDecimal roas;

    /** CTR = clicks / impressions */
    private BigDecimal ctr;
}
