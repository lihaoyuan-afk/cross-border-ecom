package com.dashboard.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("daily_sales")
public class DailySales {

    @TableId(type = IdType.AUTO)
    private Long id;

    private LocalDate date;

    private BigDecimal revenue;

    private Integer orders;

    private BigDecimal avgOrderValue;

    private Integer refundCount;

    private LocalDateTime createdAt;
}
