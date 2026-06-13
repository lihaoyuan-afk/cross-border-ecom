package com.dashboard.service.impl;

import com.dashboard.mapper.DailySalesMapper;
import com.dashboard.service.SalesService;
import com.dashboard.vo.SalesTrendVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
@RequiredArgsConstructor
public class SalesServiceImpl implements SalesService {

    private final DailySalesMapper salesMapper;

    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    @Override
    public List<SalesTrendVO> getTrend(String period, String startDate, String endDate) {
        // 默认时间范围：最近 30 天
        if (startDate == null || endDate == null) {
            endDate   = LocalDate.now().format(FMT);
            startDate = LocalDate.now().minusDays(29).format(FMT);
        }

        return switch (period) {
            case "week"  -> salesMapper.selectWeeklyTrend(startDate, endDate);
            case "month" -> salesMapper.selectMonthlyTrend(startDate, endDate);
            default      -> salesMapper.selectDailyTrend(startDate, endDate);
        };
    }
}
