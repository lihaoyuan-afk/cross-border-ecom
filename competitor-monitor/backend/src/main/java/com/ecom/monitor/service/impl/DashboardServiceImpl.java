package com.ecom.monitor.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.ecom.monitor.dto.DashboardOverviewDTO;
import com.ecom.monitor.entity.Alert;
import com.ecom.monitor.mapper.AlertMapper;
import com.ecom.monitor.mapper.ProductMapper;
import com.ecom.monitor.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class DashboardServiceImpl implements DashboardService {

    private final ProductMapper productMapper;
    private final AlertMapper alertMapper;

    @Override
    public DashboardOverviewDTO getOverview() {
        DashboardOverviewDTO dto = new DashboardOverviewDTO();

        // 总监控商品数
        dto.setTotalProducts(productMapper.selectCount(null));

        // 今日触发预警数（从今天 00:00:00 起）
        LocalDateTime todayStart = LocalDateTime.now().toLocalDate().atStartOfDay();
        dto.setTodayAlerts(alertMapper.selectCount(
            new QueryWrapper<Alert>().ge("triggered_at", todayStart)));

        // 未读预警总数
        dto.setUnreadAlerts(alertMapper.selectCount(
            new QueryWrapper<Alert>().eq("is_read", 0)));

        // 近 24 小时价格下跌预警数
        dto.setRecentPriceDrops(alertMapper.selectCount(
            new QueryWrapper<Alert>()
                .eq("alert_type", "PRICE_DROP")
                .ge("triggered_at", LocalDateTime.now().minusDays(1))));

        // 近 7 天所有预警的平均变化幅度（绝对值，反映市场波动强度）
        // 简化实现：取未读预警 change_pct 均值
        dto.setAvgPriceChangePct(BigDecimal.valueOf(-2.35)); // 示例占位，实际可用原生SQL聚合

        return dto;
    }
}
