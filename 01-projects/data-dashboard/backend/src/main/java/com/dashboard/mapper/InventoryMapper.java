package com.dashboard.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.dashboard.entity.Inventory;

public interface InventoryMapper extends BaseMapper<Inventory> {
    // 全量查询使用 MyBatis-Plus 内置的 selectList，无需额外定义
}
