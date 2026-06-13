package com.ecom.monitor.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ecom.monitor.common.Result;
import com.ecom.monitor.entity.BsrHistory;
import com.ecom.monitor.entity.PriceHistory;
import com.ecom.monitor.entity.Product;
import com.ecom.monitor.service.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;

    /** 商品列表（分页 + 关键词搜索） */
    @GetMapping("/list")
    public Result<Page<Product>> listProducts(
            @RequestParam(defaultValue = "1")  int pageNum,
            @RequestParam(defaultValue = "20") int pageSize,
            @RequestParam(required = false)    String keyword) {
        return Result.success(productService.listProducts(pageNum, pageSize, keyword));
    }

    /** 获取指定商品的价格历史（默认最近 30 天） */
    @GetMapping("/{asin}/price-history")
    public Result<List<PriceHistory>> getPriceHistory(
            @PathVariable String asin,
            @RequestParam(defaultValue = "30") int days) {
        return Result.success(productService.getPriceHistory(asin, days));
    }

    /** 获取指定商品的 BSR 排名历史（默认最近 30 天） */
    @GetMapping("/{asin}/bsr-history")
    public Result<List<BsrHistory>> getBsrHistory(
            @PathVariable String asin,
            @RequestParam(defaultValue = "30") int days) {
        return Result.success(productService.getBsrHistory(asin, days));
    }
}
