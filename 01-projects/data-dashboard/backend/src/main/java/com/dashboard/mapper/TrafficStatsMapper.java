package com.dashboard.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.dashboard.entity.TrafficStats;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.Map;

public interface TrafficStatsMapper extends BaseMapper<TrafficStats> {

    /** 聚合指定日期段流量漏斗核心数据 */
    @Select("""
        SELECT SUM(sessions)    AS totalSessions,
               SUM(page_views)  AS totalPageViews,
               SUM(conversions) AS totalConversions
        FROM traffic_stats
        WHERE date BETWEEN #{startDate} AND #{endDate}
        """)
    Map<String, Object> selectFunnelData(
            @Param("startDate") String startDate,
            @Param("endDate") String endDate);
}
