package com.dashboard.controller;

import com.dashboard.service.SalesService;
import com.dashboard.vo.Result;
import com.dashboard.vo.SalesTrendVO;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/sales")
@RequiredArgsConstructor
public class SalesController {

    private final SalesService salesService;

    /**
     * 销售趋势数据
     * GET /api/sales/trend?period=day&start=2024-01-01&end=2024-06-30
     * period 可选值：day（按天）/ week（按周）/ month（按月）
     */
    @GetMapping("/trend")
    public Result<List<SalesTrendVO>> getTrend(
            @RequestParam(defaultValue = "day") String period,
            @RequestParam(required = false) String start,
            @RequestParam(required = false) String end) {

        return Result.success(salesService.getTrend(period, start, end));
    }
}
