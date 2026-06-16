import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { title: '监控看板' },
  },
  {
    path: '/products',
    name: 'ProductList',
    component: () => import('../views/ProductList.vue'),
    meta: { title: '商品列表' },
  },
  {
    path: '/products/:asin',
    name: 'ProductDetail',
    component: () => import('../views/ProductDetail.vue'),
    meta: { title: '商品详情' },
  },
  {
    path: '/alerts/config',
    name: 'AlertConfig',
    component: () => import('../views/AlertConfig.vue'),
    meta: { title: '预警配置' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由切换时更新浏览器标签页标题
router.beforeEach((to) => {
  document.title = `${to.meta.title} - 竞品监控系统`
})

export default router
