package com.dashboard.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.dashboard.entity.AdPerformance;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

public interface AdPerformanceMapper extends BaseMapper<AdPerformance> {

    /** 查询指定日期范围内的逐日广告数据（前端折线图用） */
    @Select("""
        SELECT DATE_FORMAT(date, '%Y-%m-%d') AS date,
               ad_spend,
               impressions,
               clicks,
               ad_revenue
        FROM ad_performance
        WHERE date BETWEEN #{startDate} AND #{endDate}
        ORDER BY date
        """)
    List<Map<String, Object>> selectDailyPerformance(
            @Param("startDate") String startDate,
            @Param("endDate") String endDate);

    /** 聚合指定日期段广告核心指标 */
    @Select("""
        SELECT SUM(ad_spend)   AS totalAdSpend,
               SUM(impressions) AS totalImpressions,
               SUM(clicks)     AS totalClicks,
               SUM(ad_revenue) AS totalAdRevenue
        FROM ad_performance
        WHERE date BETWEEN #{startDate} AND #{endDate}
        """)
    Map<String, Object> selectSummary(
            @Param("startDate") String startDate,
            @Param("endDate") String endDate);
}
