package com.ecom.monitor.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ecom.monitor.dto.AlertConfigDTO;
import com.ecom.monitor.entity.Alert;
import com.ecom.monitor.entity.AlertConfig;

public interface AlertService {

    /** 分页查询预警列表；asin/isRead 为可选过滤条件 */
    Page<Alert> listAlerts(int pageNum, int pageSize, String asin, Integer isRead);

    /** 获取预警配置：优先返回 ASIN 级别配置，否则返回全局配置 */
    AlertConfig getConfig(String asin);

    /** 保存或更新预警阈值配置 */
    void saveConfig(AlertConfigDTO dto);

    /** 将单条预警标记为已读 */
    void markAsRead(Long id);

    /** 查询未读预警总数（用于导航栏徽标） */
    long countUnread();
}
