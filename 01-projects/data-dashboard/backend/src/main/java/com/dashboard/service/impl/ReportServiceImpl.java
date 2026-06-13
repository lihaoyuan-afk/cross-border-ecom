package com.dashboard.service.impl;

import com.alibaba.excel.EasyExcel;
import com.alibaba.excel.annotation.ExcelProperty;
import com.alibaba.excel.annotation.format.NumberFormat;
import com.dashboard.mapper.AdPerformanceMapper;
import com.dashboard.mapper.DailySalesMapper;
import com.dashboard.service.ReportService;
import com.dashboard.vo.AdsPerformanceVO;
import com.dashboard.vo.SalesTrendVO;
import jakarta.servlet.http.HttpServletResponse;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class ReportServiceImpl implements ReportService {

    private final DailySalesMapper salesMapper;
    private final AdPerformanceMapper adMapper;

    @Override
    public void exportExcel(String startDate, String endDate, HttpServletResponse response) throws Exception {
        String fileName = URLEncoder.encode(
                "经营数据报表_" + startDate + "_" + endDate + ".xlsx",
                StandardCharsets.UTF_8);

        response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        response.setCharacterEncoding("utf-8");
        response.setHeader("Content-Disposition", "attachment;filename*=utf-8''" + fileName);

        // Sheet1: 每日销售数据
        List<SalesTrendVO> salesList = salesMapper.selectDailyTrend(startDate, endDate);
        List<SalesExcelRow> salesRows = salesList.stream().map(s -> {
            SalesExcelRow row = new SalesExcelRow();
            row.date           = s.getPeriod();
            row.revenue        = s.getRevenue();
            row.orders         = s.getOrders();
            row.avgOrderValue  = s.getAvgOrderValue();
            return row;
        }).toList();

        // Sheet2: 广告表现数据
        List<Map<String, Object>> adRaw = adMapper.selectDailyPerformance(startDate, endDate);
        List<AdsExcelRow> adRows = new ArrayList<>();
        for (Map<String, Object> row : adRaw) {
            AdsExcelRow ar = new AdsExcelRow();
            ar.date        = row.get("date").toString();
            ar.adSpend     = toBD(row.get("ad_spend"));
            ar.impressions = toBD(row.get("impressions")).intValue();
            ar.clicks      = toBD(row.get("clicks")).intValue();
            ar.adRevenue   = toBD(row.get("ad_revenue"));
            BigDecimal rev = ar.adRevenue;
            BigDecimal spd = ar.adSpend;
            ar.acos = rev.compareTo(BigDecimal.ZERO) > 0
                    ? spd.divide(rev, 4, RoundingMode.HALF_UP).multiply(BigDecimal.valueOf(100))
                    : BigDecimal.ZERO;
            ar.roas = spd.compareTo(BigDecimal.ZERO) > 0
                    ? rev.divide(spd, 2, RoundingMode.HALF_UP)
                    : BigDecimal.ZERO;
            adRows.add(ar);
        }

        EasyExcel.write(response.getOutputStream())
                .sheet("销售数据").head(SalesExcelRow.class).doWrite(salesRows)
                .sheet("广告数据").head(AdsExcelRow.class).doWrite(adRows);
    }

    private BigDecimal toBD(Object val) {
        if (val == null) return BigDecimal.ZERO;
        if (val instanceof BigDecimal bd) return bd;
        return new BigDecimal(val.toString());
    }

    @Data
    public static class SalesExcelRow {
        @ExcelProperty("日期")
        private String date;
        @ExcelProperty("销售额（元）")
        private BigDecimal revenue;
        @ExcelProperty("订单量")
        private Integer orders;
        @ExcelProperty("客单价（元）")
        private BigDecimal avgOrderValue;
    }

    @Data
    public static class AdsExcelRow {
        @ExcelProperty("日期")
        private String date;
        @ExcelProperty("广告花费（元）")
        private BigDecimal adSpend;
        @ExcelProperty("曝光量")
        private Integer impressions;
        @ExcelProperty("点击量")
        private Integer clicks;
        @ExcelProperty("广告销售额（元）")
        private BigDecimal adRevenue;
        @ExcelProperty("ACoS（%）")
        private BigDecimal acos;
        @ExcelProperty("ROAS")
        private BigDecimal roas;
    }
}
