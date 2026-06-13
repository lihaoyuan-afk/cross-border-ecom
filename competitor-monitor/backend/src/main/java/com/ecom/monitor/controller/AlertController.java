package com.ecom.monitor.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ecom.monitor.common.Result;
import com.ecom.monitor.dto.AlertConfigDTO;
import com.ecom.monitor.entity.Alert;
import com.ecom.monitor.entity.AlertConfig;
import com.ecom.monitor.service.AlertService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/alerts")
@RequiredArgsConstructor
public class AlertController {

    private final AlertService alertService;

    /** 预警列表（分页，可按 ASIN 和已读状态筛选） */
    @GetMapping("/list")
    public Result<Page<Alert>> listAlerts(
            @RequestParam(defaultValue = "1")  int pageNum,
            @RequestParam(defaultValue = "20") int pageSize,
            @RequestParam(required = false)    String asin,
            @RequestParam(required = false)    Integer isRead) {
        return Result.success(alertService.listAlerts(pageNum, pageSize, asin, isRead));
    }

    /** 获取预警配置（不传 asin 则返回全局配置） */
    @GetMapping("/config")
    public Result<AlertConfig> getConfig(
            @RequestParam(required = false) String asin) {
        return Result.success(alertService.getConfig(asin));
    }

    /** 保存/更新预警阈值配置 */
    @PostMapping("/config")
    public Result<Void> saveConfig(@RequestBody AlertConfigDTO dto) {
        alertService.saveConfig(dto);
        return Result.success();
    }

    /** 标记预警为已读 */
    @PutMapping("/{id}/read")
    public Result<Void> markAsRead(@PathVariable Long id) {
        alertService.markAsRead(id);
        return Result.success();
    }

    /** 未读预警数（导航徽标用） */
    @GetMapping("/unread-count")
    public Result<Long> unreadCount() {
        return Result.success(alertService.countUnread());
    }
}
