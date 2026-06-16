package com.ecom.monitor.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/** 预警阈值配置（asin 为 NULL 时代表全局配置） */
@Data
@TableName("alert_config")
public class AlertConfig {

    @TableId(type = IdType.AUTO)
    private Long id;

    /** 目标 ASIN，null = 全局默认配置 */
    private String asin;

    /** 价格下跌预警阈值（%） */
    private BigDecimal priceDropPct;

    /** 价格上涨预警阈值（%） */
    private BigDecimal priceRisePct;

    /** BSR 变动预警阈值（%） */
    private BigDecimal bsrChangePct;

    private LocalDateTime updatedAt;
}
