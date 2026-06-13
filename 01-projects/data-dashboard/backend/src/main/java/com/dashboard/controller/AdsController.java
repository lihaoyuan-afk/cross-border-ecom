package com.dashboard.controller;

import com.dashboard.service.AdsService;
import com.dashboard.vo.AdsPerformanceVO;
import com.dashboard.vo.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/ads")
@RequiredArgsConstructor
public class AdsController {

    private final AdsService adsService;

    /**
     * 广告表现数据（含 ACoS / ROAS / CTR 计算值）
     * GET /api/ads/performance?start=2024-01-01&end=2024-03-31
     */
    @GetMapping("/performance")
    public Result<List<AdsPerformanceVO>> getPerformance(
            @RequestParam(required = false) String start,
            @RequestParam(required = false) String end) {

        if (end == null)   end   = "2024-06-30";
        if (start == null) start = "2024-01-01";

        return Result.success(adsService.getPerformance(start, end));
    }
}
