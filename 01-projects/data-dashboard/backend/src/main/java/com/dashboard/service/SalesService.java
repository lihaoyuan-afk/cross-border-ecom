package com.dashboard.service;

import com.dashboard.vo.SalesTrendVO;

import java.util.List;

public interface SalesService {
    List<SalesTrendVO> getTrend(String period, String startDate, String endDate);
}
