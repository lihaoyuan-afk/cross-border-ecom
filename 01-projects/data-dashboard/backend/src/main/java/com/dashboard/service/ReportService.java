package com.dashboard.service;

import jakarta.servlet.http.HttpServletResponse;

public interface ReportService {
    void exportExcel(String startDate, String endDate, HttpServletResponse response) throws Exception;
}
