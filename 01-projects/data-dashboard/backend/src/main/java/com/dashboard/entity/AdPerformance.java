package com.dashboard.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("ad_performance")
public class AdPerformance {

    @TableId(type = IdType.AUTO)
    private Long id;

    private LocalDate date;

    private BigDecimal adSpend;

    private Integer impressions;

    private Integer clicks;

    private BigDecimal adRevenue;

    private LocalDateTime createdAt;
}
