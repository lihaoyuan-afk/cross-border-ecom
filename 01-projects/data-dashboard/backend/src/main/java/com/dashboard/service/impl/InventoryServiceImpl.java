package com.dashboard.service.impl;

import com.dashboard.entity.Inventory;
import com.dashboard.mapper.InventoryMapper;
import com.dashboard.service.InventoryService;
import com.dashboard.vo.InventoryStatusVO;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;

@Service
@RequiredArgsConstructor
public class InventoryServiceImpl implements InventoryService {

    private final InventoryMapper inventoryMapper;

    @Override
    public List<InventoryStatusVO> getStatus() {
        List<Inventory> list = inventoryMapper.selectList(null);

        return list.stream().map(inv -> {
            InventoryStatusVO vo = new InventoryStatusVO();
            vo.setSku(inv.getSku());
            vo.setProductName(inv.getProductName());
            vo.setStockQty(inv.getStockQty());
            vo.setDailySalesAvg(inv.getDailySalesAvg());
            vo.setAlertThreshold(inv.getAlertThreshold());

            // 可销天数 = 库存 / 日均销量
            BigDecimal stock       = BigDecimal.valueOf(inv.getStockQty());
            BigDecimal dailySales  = inv.getDailySalesAvg();
            BigDecimal daysRemaining = BigDecimal.ZERO;

            if (dailySales.compareTo(BigDecimal.ZERO) > 0) {
                daysRemaining = stock.divide(dailySales, 1, RoundingMode.FLOOR);
            }
            vo.setDaysRemaining(daysRemaining);

            // 判断库存状态
            if (inv.getStockQty() == 0) {
                vo.setStatus("OUT_OF_STOCK");
                vo.setStatusLabel("断货");
            } else if (daysRemaining.intValue() < inv.getAlertThreshold()) {
                vo.setStatus("WARNING");
                vo.setStatusLabel("预警");
            } else {
                vo.setStatus("NORMAL");
                vo.setStatusLabel("正常");
            }

            return vo;
        }).toList();
    }
}
