package com.ecom.monitor.dto;

import lombok.Data;
import java.math.BigDecimal;

/** 预警配置请求体（POST /api/alerts/config） */
@Data
public class AlertConfigDTO {

    /** 目标 ASIN；为空则修改全局配置 */
    private String asin;

    private BigDecimal priceDropPct;
    private BigDecimal priceRisePct;
    private BigDecimal bsrChangePct;
}
