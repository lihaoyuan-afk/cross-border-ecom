package com.ecom.monitor.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.time.LocalDateTime;

/** 监控商品基础信息 */
@Data
@TableName("products")
public class Product {

    @TableId(type = IdType.AUTO)
    private Long id;

    /** Amazon 商品唯一标识符 */
    private String asin;

    /** 商品标题 */
    private String title;

    /** 一级类目（如 Electronics） */
    private String category;

    /** 二级类目（如 Wireless Earbuds） */
    private String subCategory;

    /** 品牌名称 */
    private String brand;

    /** 添加监控时间 */
    private LocalDateTime createdAt;
}
