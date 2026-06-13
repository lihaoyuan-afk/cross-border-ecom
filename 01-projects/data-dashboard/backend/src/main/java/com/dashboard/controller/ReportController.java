package com.dashboard.controller;

import com.dashboard.service.ReportService;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/report")
@RequiredArgsConstructor
public class ReportController {

    private final ReportService reportService;

    /**
     * 导出 Excel 报表（销售数据 + 广告数据两个 Sheet）
     * GET /api/report/export?start=2024-01-01&end=2024-06-30
     */
    @GetMapping("/export")
    public void exportExcel(
            @RequestParam(defaultValue = "2024-01-01") String start,
            @RequestParam(defaultValue = "2024-06-30") String end,
            HttpServletResponse response) throws Exception {

        reportService.exportExcel(start, end, response);
    }
}
