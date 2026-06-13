import dayjs from 'dayjs'

export const fmt = {
  // 金额：¥12,345.67
  money: (val) => {
    if (val == null) return '¥0.00'
    return '¥' + Number(val).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  },

  // 整数：带千位分隔符
  number: (val) => {
    if (val == null) return '0'
    return Number(val).toLocaleString('zh-CN')
  },

  // 百分比：0.2567 → 25.67%
  percent: (val, digits = 2) => {
    if (val == null) return '0%'
    return (Number(val) * 100).toFixed(digits) + '%'
  },

  // 倍数：3.58 → 3.58x
  multiple: (val) => {
    if (val == null) return '0x'
    return Number(val).toFixed(2) + 'x'
  },

  // 日期格式
  date: (val) => dayjs(val).format('YYYY-MM-DD'),

  // 环比变化：正值返回绿色 ↑，负值返回红色 ↓
  // 注意：ACoS 越高越差，调用时传 reverse=true
  changeText: (val) => {
    if (val == null) return { text: '—', color: '#909399' }
    const pct = (Number(val) * 100).toFixed(1)
    const isPositive = Number(val) >= 0
    return {
      text: (isPositive ? '↑ ' : '↓ ') + Math.abs(pct) + '%',
      color: isPositive ? '#67C23A' : '#F56C6C'
    }
  },

  // ACoS 的环比：上升是坏事（红色），下降是好事（绿色）
  acosChangeText: (val) => {
    if (val == null) return { text: '—', color: '#909399' }
    const pct = (Number(val) * 100).toFixed(1)
    const isPositive = Number(val) >= 0
    return {
      text: (isPositive ? '↑ ' : '↓ ') + Math.abs(pct) + '%',
      color: isPositive ? '#F56C6C' : '#67C23A'  // 颜色反转
    }
  }
}
