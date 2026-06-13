package com.dashboard.service.impl;

import com.dashboard.mapper.AdPerformanceMapper;
import com.dashboard.service.AdsService;
import com.dashboard.vo.AdsPerformanceVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class AdsServiceImpl implements AdsService {

    private final AdPerformanceMapper adMapper;

    @Override
    public List<AdsPerformanceVO> getPerformance(String startDate, String endDate) {
        List<Map<String, Object>> rawList = adMapper.selectDailyPerformance(startDate, endDate);

        return rawList.stream().map(row -> {
            AdsPerformanceVO vo = new AdsPerformanceVO();
            vo.setDate(row.get("date").toString());

            BigDecimal adSpend   = toBD(row.get("ad_spend"));
            BigDecimal adRevenue = toBD(row.get("ad_revenue"));
            BigDecimal impressions = toBD(row.get("impressions"));
            BigDecimal clicks    = toBD(row.get("clicks"));

            vo.setAdSpend(adSpend);
            vo.setAdRevenue(adRevenue);
            vo.setImpressions(impressions.intValue());
            vo.setClicks(clicks.intValue());

            // ACoS = 广告花费 / 广告销售额
            vo.setAcos(adRevenue.compareTo(BigDecimal.ZERO) > 0
                    ? adSpend.divide(adRevenue, 4, RoundingMode.HALF_UP)
                    : BigDecimal.ZERO);

            // ROAS = 广告销售额 / 广告花费
            vo.setRoas(adSpend.compareTo(BigDecimal.ZERO) > 0
                    ? adRevenue.divide(adSpend, 4, RoundingMode.HALF_UP)
                    : BigDecimal.ZERO);

            // CTR = 点击量 / 曝光量
            vo.setCtr(impressions.compareTo(BigDecimal.ZERO) > 0
                    ? clicks.divide(impressions, 4, RoundingMode.HALF_UP)
                    : BigDecimal.ZERO);

            return vo;
        }).toList();
    }

    private BigDecimal toBD(Object val) {
        if (val == null) return BigDecimal.ZERO;
        if (val instanceof BigDecimal bd) return bd;
        return new BigDecimal(val.toString());
    }
}
