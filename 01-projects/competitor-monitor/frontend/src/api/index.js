import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例：基础路径 /api 会被 vite 代理到后端 :8080
const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// 响应拦截器：统一提取 data，统一弹出错误提示
request.interceptors.response.use(
  (res) => res.data,
  (err) => {
    ElMessage.error(err.message || '网络请求失败，请检查后端服务')
    return Promise.reject(err)
  }
)

// ---- 商品接口 ----
export const getProductList  = (params) => request.get('/products/list', { params })
export const getPriceHistory = (asin, days = 30) =>
  request.get(`/products/${asin}/price-history`, { params: { days } })
export const getBsrHistory   = (asin, days = 30) =>
  request.get(`/products/${asin}/bsr-history`, { params: { days } })

// ---- 看板接口 ----
export const getDashboardOverview = () => request.get('/dashboard/overview')

// ---- 预警接口 ----
export const getAlertList   = (params) => request.get('/alerts/list', { params })
export const getAlertConfig = (asin)   => request.get('/alerts/config', { params: { asin } })
export const saveAlertConfig = (data)  => request.post('/alerts/config', data)
export const markAlertRead  = (id)     => request.put(`/alerts/${id}/read`)
export const getUnreadCount = ()       => request.get('/alerts/unread-count')
