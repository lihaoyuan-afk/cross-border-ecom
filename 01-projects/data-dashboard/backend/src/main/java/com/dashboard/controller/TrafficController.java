package com.dashboard.controller;

import com.dashboard.service.TrafficService;
import com.dashboard.vo.Result;
import com.dashboard.vo.TrafficFunnelVO;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/traffic")
@RequiredArgsConstructor
public class TrafficController {

    private final TrafficService trafficService;

    /**
     * 流量漏斗数据：会话 → 浏览 → 购买 三层转化率
     * GET /api/traffic/funnel?start=2024-01-01&end=2024-06-30
     */
    @GetMapping("/funnel")
    public Result<TrafficFunnelVO> getFunnel(
            @RequestParam(defaultValue = "2024-01-01") String start,
            @RequestParam(defaultValue = "2024-06-30") String end) {

        return Result.success(trafficService.getFunnel(start, end));
    }
}
