<template>
  <div ref="dashRef">
    <h2 class="page-title">监控看板</h2>

    <!-- 4 个核心指标卡片 -->
    <el-row :gutter="16" style="margin-bottom: 20px">
      <el-col :span="6" v-for="card in statCards" :key="card.label">
        <el-card class="stat-card" shadow="hover" v-loading="loading">
          <div class="stat-inner">
            <div class="stat-icon" :style="{ background: card.color }">
              <el-icon size="22" color="#fff"><component :is="card.icon" /></el-icon>
            </div>
            <div>
              <div class="stat-val">{{ card.value }}</div>
              <div class="stat-label">{{ card.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最新预警列表 -->
    <el-card shadow="never">
      <template #header>
        <div class="card-hd">
          <span class="card-hd-title">最新预警（最近 10 条）</span>
          <el-button text type="primary" size="small" @click="$router.push('/alerts/config')">
            查看全部
          </el-button>
        </div>
      </template>

      <el-table :data="alerts" stripe v-loading="alertLoading" size="default">
        <el-table-column prop="asin" label="ASIN" width="150" />
        <el-table-column label="预警类型" width="130">
          <template #default="{ row }">
            <el-tag :type="typeTagMap[row.alertType]" size="small">
              {{ typeLabelMap[row.alertType] || row.alertType }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="变化幅度" width="110" align="right">
          <template #default="{ row }">
            <span :class="row.changePct < 0 ? 'c-red' : 'c-orange'">
              {{ row.changePct > 0 ? '+' : '' }}{{ row.changePct }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column label="变化前" width="90" align="right">
          <template #default="{ row }">${{ row.oldValue }}</template>
        </el-table-column>
        <el-table-column label="变化后" width="90" align="right">
          <template #default="{ row }">${{ row.newValue }}</template>
        </el-table-column>
        <el-table-column prop="triggeredAt" label="触发时间" min-width="160" />
        <el-table-column label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.isRead ? 'info' : 'success'" size="small">
              {{ row.isRead ? '已读' : '未读' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="90" align="center">
          <template #default="{ row }">
            <el-button
              v-if="!row.isRead" text type="primary" size="small"
              @click="handleMarkRead(row)"
            >标已读</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getDashboardOverview, getAlertList, markAlertRead } from '../api/index.js'
import { ElMessage } from 'element-plus'
import { gsap, ScrollTrigger } from '../animation/gsap.js'

const overview = ref({})
const alerts = ref([])
const loading = ref(false)
const alertLoading = ref(false)
const dashRef = ref(null)
let gsapCtx

const typeLabelMap = {
  PRICE_DROP: '价格下跌', PRICE_RISE: '价格上涨',
  BSR_IMPROVE: 'BSR 改善', BSR_DROP: 'BSR 下滑',
}
const typeTagMap = {
  PRICE_DROP: 'danger', PRICE_RISE: 'warning',
  BSR_IMPROVE: 'success', BSR_DROP: 'info',
}

const statCards = computed(() => [
  {
    label: '监控商品总数',
    value: overview.value.totalProducts ?? '—',
    icon: 'Goods', color: '#FF7A1A',
  },
  {
    label: '今日预警',
    value: overview.value.todayAlerts ?? '—',
    icon: 'Warning', color: '#FB5F5F',
  },
  {
    label: '未读预警',
    value: overview.value.unreadAlerts ?? '—',
    icon: 'Bell', color: '#E8B14B',
  },
  {
    label: '近24h价格下跌预警',
    value: overview.value.recentPriceDrops ?? '—',
    icon: 'TrendCharts', color: '#4ADE80',
  },
])

const loadData = async () => {
  loading.value = true
  alertLoading.value = true
  try {
    const [ovRes, alRes] = await Promise.all([
      getDashboardOverview(),
      getAlertList({ pageNum: 1, pageSize: 10 }),
    ])
    overview.value = ovRes.data || {}
    alerts.value = alRes.data?.records || []
  } catch {
    ElMessage.error('数据加载失败，请确认后端服务已启动')
  } finally {
    loading.value = false
    alertLoading.value = false
  }
}

const handleMarkRead = async (row) => {
  await markAlertRead(row.id)
  row.isRead = 1
  overview.value.unreadAlerts = Math.max(0, (overview.value.unreadAlerts || 1) - 1)
  ElMessage.success('已标记为已读')
}

onMounted(() => {
  gsapCtx = gsap.context(() => {
    gsap.from('.page-title', { x: -8, duration: 0.45 })

    ScrollTrigger.batch('.stat-card', {
      onEnter: (els) => gsap.from(els, {
        y: 12, autoAlpha: 0, stagger: 0.08, duration: 0.5, ease: 'power3.out'
      }),
      once: true,
      start: 'top 95%',
    })

    ScrollTrigger.batch('.el-table__row', {
      onEnter: (els) => gsap.from(els, {
        x: -5, autoAlpha: 0, stagger: 0.04, duration: 0.35, ease: 'power2.out'
      }),
      once: true,
      start: 'top 92%',
    })
  }, dashRef.value)

  loadData()
})

onUnmounted(() => {
  gsapCtx?.revert()
})
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: 600; margin-bottom: 20px; color: var(--el-text-color-primary); }
.stat-card { border-radius: 8px; }
.stat-inner { display: flex; align-items: center; gap: 16px; }
.stat-icon {
  width: 52px; height: 52px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.stat-val {
  font-size: 26px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  line-height: 1.2;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-variant-numeric: tabular-nums;
}
.stat-label { font-size: 12px; color: var(--el-text-color-secondary); margin-top: 4px; }
.card-hd { display: flex; justify-content: space-between; align-items: center; }
.card-hd-title { font-weight: 600; color: var(--el-text-color-primary); }
.c-red { color: #FB5F5F; font-weight: 600; }
.c-orange { color: #E8B14B; font-weight: 600; }
</style>
