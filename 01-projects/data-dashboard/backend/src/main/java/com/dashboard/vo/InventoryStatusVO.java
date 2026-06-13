package com.dashboard.vo;

import lombok.Data;

import java.math.BigDecimal;

/** 库存状态数据项（表格用，含预警状态） */
@Data
public class InventoryStatusVO {

    private String sku;

    private String productName;

    /** 当前库存数量（件） */
    private Integer stockQty;

    /** 日均销量 */
    private BigDecimal dailySalesAvg;

    /** 预警阈值（天） */
    private Integer alertThreshold;

    /**
     * 可销天数 = stock_qty / daily_sales_avg
     * 0 表示已断货
     */
    private BigDecimal daysRemaining;

    /**
     * 状态：NORMAL（正常）/ WARNING（预警）/ OUT_OF_STOCK（断货）
     */
    private String status;

    /** 状态显示文字（中文） */
    private String statusLabel;
}
