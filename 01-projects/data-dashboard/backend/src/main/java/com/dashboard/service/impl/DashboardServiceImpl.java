package com.dashboard.service.impl;

import com.dashboard.mapper.AdPerformanceMapper;
import com.dashboard.mapper.DailySalesMapper;
import com.dashboard.mapper.TrafficStatsMapper;
import com.dashboard.service.DashboardService;
import com.dashboard.vo.DashboardSummaryVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class DashboardServiceImpl implements DashboardService {

    private final DailySalesMapper salesMapper;
    private final AdPerformanceMapper adMapper;
    private final TrafficStatsMapper trafficMapper;

    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    @Override
    public DashboardSummaryVO getSummary(String startDate, String endDate) {
        // 查询当前周期数据
        Map<String, Object> sales   = nullSafe(salesMapper.selectSummary(startDate, endDate));
        Map<String, Object> ads     = nullSafe(adMapper.selectSummary(startDate, endDate));
        Map<String, Object> traffic = nullSafe(trafficMapper.selectFunnelData(startDate, endDate));

        // 计算上一个同等时长周期（用于环比）
        LocalDate start  = LocalDate.parse(startDate, FMT);
        LocalDate end    = LocalDate.parse(endDate, FMT);
        long periodDays  = end.toEpochDay() - start.toEpochDay() + 1;
        String prevStart = start.minusDays(periodDays).format(FMT);
        String prevEnd   = start.minusDays(1).format(FMT);

        Map<String, Object> prevSales   = nullSafe(salesMapper.selectSummary(prevStart, prevEnd));
        Map<String, Object> prevAds     = nullSafe(adMapper.selectSummary(prevStart, prevEnd));
        Map<String, Object> prevTraffic = nullSafe(trafficMapper.selectFunnelData(prevStart, prevEnd));

        DashboardSummaryVO vo = new DashboardSummaryVO();

        // ── 销售模块 ──
        BigDecimal totalRevenue = toBD(sales.get("totalRevenue"));
        BigDecimal totalOrders  = toBD(sales.get("totalOrders"));
        BigDecimal totalRefunds = toBD(sales.get("totalRefunds"));

        vo.setTotalRevenue(totalRevenue);
        vo.setTotalOrders(totalOrders.intValue());
        vo.setAvgOrderValue(toBD(sales.get("avgOrderValue")).setScale(2, RoundingMode.HALF_UP));
        vo.setRefundRate(totalOrders.compareTo(BigDecimal.ZERO) > 0
                ? totalRefunds.divide(totalOrders, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO);

        // ── 广告模块 ──
        BigDecimal totalAdSpend   = toBD(ads.get("totalAdSpend"));
        BigDecimal totalAdRevenue = toBD(ads.get("totalAdRevenue"));

        vo.setTotalAdSpend(totalAdSpend);
        vo.setAvgAcos(totalAdRevenue.compareTo(BigDecimal.ZERO) > 0
                ? totalAdSpend.divide(totalAdRevenue, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO);
        vo.setAvgRoas(totalAdSpend.compareTo(BigDecimal.ZERO) > 0
                ? totalAdRevenue.divide(totalAdSpend, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO);

        BigDecimal totalImpressions = toBD(ads.get("totalImpressions"));
        BigDecimal totalClicks      = toBD(ads.get("totalClicks"));
        vo.setAvgCtr(totalImpressions.compareTo(BigDecimal.ZERO) > 0
                ? totalClicks.divide(totalImpressions, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO);

        // ── 流量模块 ──
        BigDecimal totalSessions     = toBD(traffic.get("totalSessions"));
        BigDecimal totalConversions  = toBD(traffic.get("totalConversions"));

        vo.setTotalSessions(totalSessions.intValue());
        vo.setTotalPageViews(toBD(traffic.get("totalPageViews")).intValue());
        vo.setConversionRate(totalSessions.compareTo(BigDecimal.ZERO) > 0
                ? totalConversions.divide(totalSessions, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO);

        // ── 环比变化 ──
        vo.setRevenueChange(calcChange(totalRevenue, toBD(prevSales.get("totalRevenue"))));
        vo.setOrdersChange(calcChange(totalOrders, toBD(prevSales.get("totalOrders"))));

        BigDecimal prevAdSpend   = toBD(prevAds.get("totalAdSpend"));
        BigDecimal prevAdRevenue = toBD(prevAds.get("totalAdRevenue"));
        BigDecimal prevAcos = prevAdRevenue.compareTo(BigDecimal.ZERO) > 0
                ? prevAdSpend.divide(prevAdRevenue, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO;
        vo.setAcosChange(calcChange(vo.getAvgAcos(), prevAcos));

        BigDecimal prevSessions    = toBD(prevTraffic.get("totalSessions"));
        BigDecimal prevConversions = toBD(prevTraffic.get("totalConversions"));
        BigDecimal prevConvRate    = prevSessions.compareTo(BigDecimal.ZERO) > 0
                ? prevConversions.divide(prevSessions, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO;
        vo.setConversionRateChange(calcChange(vo.getConversionRate(), prevConvRate));

        return vo;
    }

    private Map<String, Object> nullSafe(Map<String, Object> map) {
        return map != null ? map : java.util.Collections.emptyMap();
    }

    private BigDecimal toBD(Object val) {
        if (val == null) return BigDecimal.ZERO;
        if (val instanceof BigDecimal bd) return bd;
        return new BigDecimal(val.toString());
    }

    private BigDecimal calcChange(BigDecimal current, BigDecimal previous) {
        if (previous == null || previous.compareTo(BigDecimal.ZERO) == 0) return BigDecimal.ZERO;
        return current.subtract(previous)
                .divide(previous, 4, RoundingMode.HALF_UP);
    }
}
