package com.ecom.monitor.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.ecom.monitor.dto.AlertConfigDTO;
import com.ecom.monitor.entity.Alert;
import com.ecom.monitor.entity.AlertConfig;
import com.ecom.monitor.mapper.AlertConfigMapper;
import com.ecom.monitor.mapper.AlertMapper;
import com.ecom.monitor.service.AlertService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

@Service
@RequiredArgsConstructor
public class AlertServiceImpl implements AlertService {

    private final AlertMapper alertMapper;
    private final AlertConfigMapper alertConfigMapper;

    @Override
    public Page<Alert> listAlerts(int pageNum, int pageSize, String asin, Integer isRead) {
        Page<Alert> page = new Page<>(pageNum, pageSize);
        QueryWrapper<Alert> wrapper = new QueryWrapper<>();
        if (StringUtils.hasText(asin))  wrapper.eq("asin", asin);
        if (isRead != null)             wrapper.eq("is_read", isRead);
        wrapper.orderByDesc("triggered_at");
        return alertMapper.selectPage(page, wrapper);
    }

    @Override
    public AlertConfig getConfig(String asin) {
        // 优先查 ASIN 级别配置
        if (StringUtils.hasText(asin)) {
            AlertConfig specific = alertConfigMapper.selectOne(
                new QueryWrapper<AlertConfig>().eq("asin", asin));
            if (specific != null) return specific;
        }
        // 回退到全局配置（asin IS NULL）
        return alertConfigMapper.selectOne(
            new QueryWrapper<AlertConfig>().isNull("asin"));
    }

    @Override
    public void saveConfig(AlertConfigDTO dto) {
        AlertConfig config = new AlertConfig();
        config.setAsin(dto.getAsin());
        config.setPriceDropPct(dto.getPriceDropPct());
        config.setPriceRisePct(dto.getPriceRisePct());
        config.setBsrChangePct(dto.getBsrChangePct());

        // 查询是否已有配置，有则更新，没有则插入
        QueryWrapper<AlertConfig> wrapper = new QueryWrapper<>();
        if (StringUtils.hasText(dto.getAsin()))
            wrapper.eq("asin", dto.getAsin());
        else
            wrapper.isNull("asin");

        AlertConfig existing = alertConfigMapper.selectOne(wrapper);
        if (existing != null) {
            config.setId(existing.getId());
            alertConfigMapper.updateById(config);
        } else {
            alertConfigMapper.insert(config);
        }
    }

    @Override
    public void markAsRead(Long id) {
        alertMapper.update(null,
            new UpdateWrapper<Alert>().eq("id", id).set("is_read", 1));
    }

    @Override
    public long countUnread() {
        return alertMapper.selectCount(
            new QueryWrapper<Alert>().eq("is_read", 0));
    }
}
