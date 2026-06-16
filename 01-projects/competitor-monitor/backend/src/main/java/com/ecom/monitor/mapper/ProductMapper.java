package com.ecom.monitor.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.ecom.monitor.entity.Product;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface ProductMapper extends BaseMapper<Product> {
}
