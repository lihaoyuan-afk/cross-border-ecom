package com.dashboard.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("traffic_stats")
public class TrafficStats {

    @TableId(type = IdType.AUTO)
    private Long id;

    private LocalDate date;

    private Integer sessions;

    private Integer pageViews;

    private Integer conversions;

    private LocalDateTime createdAt;
}
