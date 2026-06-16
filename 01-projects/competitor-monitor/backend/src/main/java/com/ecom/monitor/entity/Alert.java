package com.ecom.monitor.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/** 竞品变动预警记录 */
@Data
@TableName("alerts")
public class Alert {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String asin;

    /** 预警类型：PRICE_DROP / PRICE_RISE / BSR_IMPROVE / BSR_DROP */
    private String alertType;

    /** 变化前的数值 */
    private BigDecimal oldValue;

    /** 变化后的数值 */
    private BigDecimal newValue;

    /** 变化百分比（负=下跌，正=上涨） */
    private BigDecimal changePct;

    /** 是否已读：0=未读，1=已读 */
    private Integer isRead;

    /** 预警触发时间 */
    private LocalDateTime triggeredAt;
}
