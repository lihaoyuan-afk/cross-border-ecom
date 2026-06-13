package com.ecom.monitor.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.time.LocalDateTime;

/** BSR 排名历史快照 */
@Data
@TableName("bsr_history")
public class BsrHistory {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String asin;

    /** BSR 排名值（越小越好，1 = 类目第一） */
    private Integer bsrRank;

    /** 排名所在类目 */
    private String category;

    /** 排名记录时间 */
    private LocalDateTime recordedAt;
}
