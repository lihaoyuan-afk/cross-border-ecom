package com.dashboard.controller;

import com.dashboard.service.DashboardService;
import com.dashboard.vo.DashboardSummaryVO;
import com.dashboard.vo.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {

    private final DashboardService dashboardService;
    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    /**
     * 获取时间段内核心指标汇总（含环比）
     * GET /api/dashboard/summary?start=2024-05-01&end=2024-05-31
     */
    @GetMapping("/summary")
    public Result<DashboardSummaryVO> getSummary(
            @RequestParam(required = false) String start,
            @RequestParam(required = false) String end) {

        if (end == null)   end   = LocalDate.now().format(FMT);
        if (start == null) start = LocalDate.now().minusDays(29).format(FMT);

        return Result.success(dashboardService.getSummary(start, end));
    }
}
