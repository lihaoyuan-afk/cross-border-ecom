package com.dashboard.service.impl;

import com.dashboard.mapper.TrafficStatsMapper;
import com.dashboard.service.TrafficService;
import com.dashboard.vo.TrafficFunnelVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class TrafficServiceImpl implements TrafficService {

    private final TrafficStatsMapper trafficMapper;

    @Override
    public TrafficFunnelVO getFunnel(String startDate, String endDate) {
        Map<String, Object> data = trafficMapper.selectFunnelData(startDate, endDate);

        BigDecimal sessions    = toBD(data.get("totalSessions"));
        BigDecimal pageViews   = toBD(data.get("totalPageViews"));
        BigDecimal conversions = toBD(data.get("totalConversions"));

        TrafficFunnelVO vo = new TrafficFunnelVO();
        vo.setTotalSessions(sessions.intValue());
        vo.setTotalPageViews(pageViews.intValue());
        vo.setTotalConversions(conversions.intValue());

        // 会话 → 页面浏览率
        vo.setSessionToPageViewRate(sessions.compareTo(BigDecimal.ZERO) > 0
                ? pageViews.divide(sessions, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO);

        // 页面浏览 → 成单转化率
        vo.setPageViewToConversionRate(pageViews.compareTo(BigDecimal.ZERO) > 0
                ? conversions.divide(pageViews, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO);

        // 整体转化率（会话 → 成单）
        vo.setOverallConversionRate(sessions.compareTo(BigDecimal.ZERO) > 0
                ? conversions.divide(sessions, 4, RoundingMode.HALF_UP)
                : BigDecimal.ZERO);

        return vo;
    }

    private BigDecimal toBD(Object val) {
        if (val == null) return BigDecimal.ZERO;
        if (val instanceof BigDecimal bd) return bd;
        return new BigDecimal(val.toString());
    }
}
