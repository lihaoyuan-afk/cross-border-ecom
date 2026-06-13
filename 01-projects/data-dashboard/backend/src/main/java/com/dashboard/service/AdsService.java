package com.dashboard.service;

import com.dashboard.vo.AdsPerformanceVO;

import java.util.List;

public interface AdsService {
    List<AdsPerformanceVO> getPerformance(String startDate, String endDate);
}
