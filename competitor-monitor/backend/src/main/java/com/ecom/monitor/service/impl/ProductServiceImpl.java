package com.ecom.monitor.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ecom.monitor.entity.BsrHistory;
import com.ecom.monitor.entity.PriceHistory;
import com.ecom.monitor.entity.Product;
import com.ecom.monitor.mapper.BsrHistoryMapper;
import com.ecom.monitor.mapper.PriceHistoryMapper;
import com.ecom.monitor.mapper.ProductMapper;
import com.ecom.monitor.service.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductServiceImpl implements ProductService {

    private final ProductMapper productMapper;
    private final PriceHistoryMapper priceHistoryMapper;
    private final BsrHistoryMapper bsrHistoryMapper;

    @Override
    public Page<Product> listProducts(int pageNum, int pageSize, String keyword) {
        Page<Product> page = new Page<>(pageNum, pageSize);
        QueryWrapper<Product> wrapper = new QueryWrapper<>();
        if (StringUtils.hasText(keyword)) {
            // 支持标题、品牌、ASIN 三字段模糊搜索
            wrapper.like("title", keyword)
                   .or().like("brand", keyword)
                   .or().like("asin", keyword);
        }
        wrapper.orderByDesc("created_at");
        return productMapper.selectPage(page, wrapper);
    }

    @Override
    public List<PriceHistory> getPriceHistory(String asin, int days) {
        QueryWrapper<PriceHistory> wrapper = new QueryWrapper<>();
        wrapper.eq("asin", asin)
               .ge("recorded_at", LocalDateTime.now().minusDays(days))
               .orderByAsc("recorded_at");
        return priceHistoryMapper.selectList(wrapper);
    }

    @Override
    public List<BsrHistory> getBsrHistory(String asin, int days) {
        QueryWrapper<BsrHistory> wrapper = new QueryWrapper<>();
        wrapper.eq("asin", asin)
               .ge("recorded_at", LocalDateTime.now().minusDays(days))
               .orderByAsc("recorded_at");
        return bsrHistoryMapper.selectList(wrapper);
    }
}
