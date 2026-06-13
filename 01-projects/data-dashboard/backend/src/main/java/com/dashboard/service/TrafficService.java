package com.dashboard.service;

import com.dashboard.vo.TrafficFunnelVO;

public interface TrafficService {
    TrafficFunnelVO getFunnel(String startDate, String endDate);
}
