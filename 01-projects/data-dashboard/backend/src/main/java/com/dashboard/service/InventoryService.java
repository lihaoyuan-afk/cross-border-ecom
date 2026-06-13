package com.dashboard.service;

import com.dashboard.vo.InventoryStatusVO;

import java.util.List;

public interface InventoryService {
    List<InventoryStatusVO> getStatus();
}
