package com.dashboard.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("inventory")
public class Inventory {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String sku;

    private String productName;

    private Integer stockQty;

    private BigDecimal dailySalesAvg;

    private Integer alertThreshold;

    private LocalDateTime updatedAt;
}
