package com.ecom.monitor.controller;

import com.ecom.monitor.common.Result;
import com.ecom.monitor.dto.DashboardOverviewDTO;
import com.ecom.monitor.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {

    private final DashboardService dashboardService;

    /** 首页看板概览数据 */
    @GetMapping("/overview")
    public Result<DashboardOverviewDTO> getOverview() {
        return Result.success(dashboardService.getOverview());
    }
}
