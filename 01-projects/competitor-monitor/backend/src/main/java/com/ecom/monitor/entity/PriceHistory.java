package com.ecom.monitor.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/** 商品价格历史快照 */
@Data
@TableName("price_history")
public class PriceHistory {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String asin;

    /** 美元售价 */
    private BigDecimal price;

    /** 货币单位，默认 USD */
    private String currency;

    /** 价格记录时间 */
    private LocalDateTime recordedAt;
}
