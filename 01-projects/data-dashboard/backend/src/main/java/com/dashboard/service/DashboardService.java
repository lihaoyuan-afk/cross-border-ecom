package com.dashboard.service;

import com.dashboard.vo.DashboardSummaryVO;

public interface DashboardService {
    DashboardSummaryVO getSummary(String startDate, String endDate);
}
