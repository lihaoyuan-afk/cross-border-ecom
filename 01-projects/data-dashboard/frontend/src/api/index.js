import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 10000
})

http.interceptors.response.use(
  res => res.data,
  err => Promise.reject(err)
)

export const api = {
  // 核心指标汇总（含环比）
  getSummary: (start, end) =>
    http.get('/dashboard/summary', { params: { start, end } }),

  // 销售趋势（折线图）
  getSalesTrend: (period, start, end) =>
    http.get('/sales/trend', { params: { period, start, end } }),

  // 广告表现（ACoS / ROAS / CTR）
  getAdsPerformance: (start, end) =>
    http.get('/ads/performance', { params: { start, end } }),

  // 流量漏斗
  getTrafficFunnel: (start, end) =>
    http.get('/traffic/funnel', { params: { start, end } }),

  // 库存状态
  getInventoryStatus: () =>
    http.get('/inventory/status'),

  // 导出 Excel 报表（直接跳转下载）
  exportReport: (start, end) => {
    const url = `/api/report/export?start=${start}&end=${end}`
    window.open(url, '_blank')
  }
}
