package com.dashboard.controller;

import com.dashboard.service.InventoryService;
import com.dashboard.vo.InventoryStatusVO;
import com.dashboard.vo.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/inventory")
@RequiredArgsConstructor
public class InventoryController {

    private final InventoryService inventoryService;

    /**
     * 库存状态列表（含断货预警标记）
     * GET /api/inventory/status
     */
    @GetMapping("/status")
    public Result<List<InventoryStatusVO>> getStatus() {
        return Result.success(inventoryService.getStatus());
    }
}
