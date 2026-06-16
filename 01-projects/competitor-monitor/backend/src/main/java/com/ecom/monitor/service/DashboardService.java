package com.ecom.monitor.service;

import com.ecom.monitor.dto.DashboardOverviewDTO;

public interface DashboardService {
    /** 返回首页看板所需的汇总指标 */
    DashboardOverviewDTO getOverview();
}
