package com.dashboard.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.dashboard.entity.DailySales;
import com.dashboard.vo.SalesTrendVO;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

public interface DailySalesMapper extends BaseMapper<DailySales> {

    /** 按天聚合销售趋势 */
    @Select("""
        SELECT DATE_FORMAT(date, '%Y-%m-%d') AS period,
               SUM(revenue)         AS revenue,
               SUM(orders)          AS orders,
               AVG(avg_order_value) AS avgOrderValue
        FROM daily_sales
        WHERE date BETWEEN #{startDate} AND #{endDate}
        GROUP BY date
        ORDER BY date
        """)
    List<SalesTrendVO> selectDailyTrend(
            @Param("startDate") String startDate,
            @Param("endDate") String endDate);

    /** 按周聚合销售趋势 */
    @Select("""
        SELECT CONCAT(YEAR(date), '-W', LPAD(WEEK(date,1), 2, '0')) AS period,
               SUM(revenue)         AS revenue,
               SUM(orders)          AS orders,
               AVG(avg_order_value) AS avgOrderValue
        FROM daily_sales
        WHERE date BETWEEN #{startDate} AND #{endDate}
        GROUP BY YEARWEEK(date, 1)
        ORDER BY YEARWEEK(date, 1)
        """)
    List<SalesTrendVO> selectWeeklyTrend(
            @Param("startDate") String startDate,
            @Param("endDate") String endDate);

    /** 按月聚合销售趋势 */
    @Select("""
        SELECT DATE_FORMAT(date, '%Y-%m') AS period,
               SUM(revenue)         AS revenue,
               SUM(orders)          AS orders,
               AVG(avg_order_value) AS avgOrderValue
        FROM daily_sales
        WHERE date BETWEEN #{startDate} AND #{endDate}
        GROUP BY DATE_FORMAT(date, '%Y-%m')
        ORDER BY DATE_FORMAT(date, '%Y-%m')
        """)
    List<SalesTrendVO> selectMonthlyTrend(
            @Param("startDate") String startDate,
            @Param("endDate") String endDate);

    /** 聚合指定日期段的销售核心指标 */
    @Select("""
        SELECT SUM(revenue)       AS totalRevenue,
               SUM(orders)        AS totalOrders,
               AVG(avg_order_value) AS avgOrderValue,
               SUM(refund_count)  AS totalRefunds
        FROM daily_sales
        WHERE date BETWEEN #{startDate} AND #{endDate}
        """)
    Map<String, Object> selectSummary(
            @Param("startDate") String startDate,
            @Param("endDate") String endDate);
}
