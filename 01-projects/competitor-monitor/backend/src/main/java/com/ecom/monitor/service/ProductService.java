package com.ecom.monitor.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ecom.monitor.entity.BsrHistory;
import com.ecom.monitor.entity.PriceHistory;
import com.ecom.monitor.entity.Product;

import java.util.List;

public interface ProductService {

    /** 分页查询商品列表，keyword 支持标题/品牌/ASIN 模糊搜索 */
    Page<Product> listProducts(int pageNum, int pageSize, String keyword);

    /** 获取某商品近 N 天的价格历史（用于折线图） */
    List<PriceHistory> getPriceHistory(String asin, int days);

    /** 获取某商品近 N 天的 BSR 排名历史（用于折线图） */
    List<BsrHistory> getBsrHistory(String asin, int days);
}
