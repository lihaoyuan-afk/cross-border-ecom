package com.dashboard.vo;

import lombok.Data;

import java.math.BigDecimal;

/** 销售趋势数据项（折线图用） */
@Data
public class SalesTrendVO {

    /** 时间标签（day模式=yyyy-MM-dd，week=第N周，month=yyyy-MM） */
    private String period;

    /** 销售额（元） */
    private BigDecimal revenue;

    /** 订单量 */
    private Integer orders;

    /** 客单价（元） */
    private BigDecimal avgOrderValue;
}
