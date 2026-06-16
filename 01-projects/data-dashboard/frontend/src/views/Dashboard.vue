<template>
  <div class="dashboard" ref="dashRef">
    <!-- ══════════════════════════════════════════════
         顶部标题栏 + 日期筛选
    ══════════════════════════════════════════════ -->
    <div class="header">
      <div class="header-left">
        <span class="logo">📊</span>
        <div>
          <h1 class="title">跨境电商数据看板</h1>
          <p class="subtitle">数据范围：2024-01-01 ~ 2024-06-30（模拟数据）</p>
        </div>
      </div>
      <div class="header-right">
        <!-- 快捷日期选项 -->
        <el-button-group class="quick-btns">
          <el-button
            v-for="opt in quickOptions"
            :key="opt.label"
            :type="activeQuick === opt.label ? 'primary' : 'default'"
            size="small"
            @click="applyQuick(opt)"
          >{{ opt.label }}</el-button>
        </el-button-group>

        <!-- 自定义日期区间 -->
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          :disabled-date="disabledDate"
          size="small"
          style="width: 240px"
          @change="onDateChange"
        />

        <!-- 导出报表 -->
        <el-button type="success" size="small" :icon="Download" @click="exportReport">
          导出报表
        </el-button>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════
         第一行：4 个核心指标卡片
    ══════════════════════════════════════════════ -->
    <div class="card-row" v-loading="loadingSummary">
      <MetricCard
        title="总销售额"
        :value="fmt.money(summary.totalRevenue)"
        :change="fmt.changeText(summary.revenueChange)"
        icon="💰"
        color="#FF7A1A"
      />
      <MetricCard
        title="总订单量"
        :value="fmt.number(summary.totalOrders) + ' 单'"
        :change="fmt.changeText(summary.ordersChange)"
        icon="🛒"
        color="#4ADE80"
      />
      <MetricCard
        title="平均 ACoS"
        :value="fmt.percent(summary.avgAcos)"
        :change="fmt.acosChangeText(summary.acosChange)"
        icon="📢"
        color="#E8B14B"
        tooltip="广告销售成本比 = 广告花费 / 广告销售额，越低越好"
      />
      <MetricCard
        title="整体转化率"
        :value="fmt.percent(summary.conversionRate)"
        :change="fmt.changeText(summary.conversionRateChange)"
        icon="🎯"
        color="#FB5F5F"
        tooltip="会话 → 成单转化率"
      />
    </div>

    <!-- ══════════════════════════════════════════════
         第二行：销售趋势图 + ACoS 趋势图
    ══════════════════════════════════════════════ -->
    <div class="chart-row">
      <!-- 销售趋势折线图 -->
      <el-card class="chart-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span>📈 销售额趋势</span>
            <el-radio-group v-model="trendPeriod" size="small" @change="loadSalesTrend">
              <el-radio-button value="day">按天</el-radio-button>
              <el-radio-button value="week">按周</el-radio-button>
              <el-radio-button value="month">按月</el-radio-button>
            </el-radio-group>
          </div>
        </template>
        <div ref="salesChartRef" class="echarts-box" v-loading="loadingSales"></div>
      </el-card>

      <!-- ACoS 趋势折线图 -->
      <el-card class="chart-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span>📢 广告 ACoS 趋势</span>
            <el-tooltip content="ACoS = 广告花费 / 广告销售额，合理区间 20%~35%">
              <el-icon><InfoFilled /></el-icon>
            </el-tooltip>
          </div>
        </template>
        <div ref="acosChartRef" class="echarts-box" v-loading="loadingAds"></div>
      </el-card>
    </div>

    <!-- ══════════════════════════════════════════════
         第三行：流量漏斗图 + 库存状态表格
    ══════════════════════════════════════════════ -->
    <div class="chart-row">
      <!-- 流量漏斗图 -->
      <el-card class="chart-card" shadow="never">
        <template #header>
          <span>🌊 流量转化漏斗</span>
        </template>
        <div ref="funnelChartRef" class="echarts-box" v-loading="loadingTraffic"></div>
      </el-card>

      <!-- 库存状态表格 -->
      <el-card class="chart-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span>📦 库存状态</span>
            <el-tag v-if="outOfStockCount > 0" type="danger" size="small">
              {{ outOfStockCount }} 款断货
            </el-tag>
            <el-tag v-if="warningCount > 0" type="warning" size="small" style="margin-left:4px">
              {{ warningCount }} 款预警
            </el-tag>
          </div>
        </template>
        <el-table
          :data="inventoryList"
          size="small"
          :row-class-name="getRowClass"
          v-loading="loadingInventory"
        >
          <el-table-column prop="sku" label="SKU" width="90" />
          <el-table-column prop="productName" label="商品名称" min-width="140" />
          <el-table-column prop="stockQty" label="库存" width="70" align="right" />
          <el-table-column prop="dailySalesAvg" label="日均销量" width="80" align="right">
            <template #default="{ row }">{{ row.dailySalesAvg }}/天</template>
          </el-table-column>
          <el-table-column prop="daysRemaining" label="可销天数" width="80" align="right">
            <template #default="{ row }">
              <span :class="getDaysClass(row)">{{ row.daysRemaining }}天</span>
            </template>
          </el-table-column>
          <el-table-column prop="statusLabel" label="状态" width="72" align="center">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ row.statusLabel }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- ══════════════════════════════════════════════
         底部信息栏
    ══════════════════════════════════════════════ -->
    <div class="footer">
      <span>当前查询周期：{{ currentStart }} ~ {{ currentEnd }}</span>
      <span style="margin: 0 12px">|</span>
      <span>技术栈：Spring Boot 3 + MyBatis-Plus + Vue 3 + ECharts</span>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import { Download, InfoFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { api } from '../api/index.js'
import { fmt } from '../utils/format.js'
import MetricCard from '../components/MetricCard.vue'
import { gsap, ScrollTrigger } from '../animation/gsap.js'

// ── 日期状态 ──────────────────────────────────────────────────
const DATA_MIN = '2024-01-01'
const DATA_MAX = '2024-06-30'
const currentStart = ref('2024-06-01')
const currentEnd   = ref('2024-06-30')
const dateRange    = ref([currentStart.value, currentEnd.value])
const activeQuick  = ref('30天')

const quickOptions = [
  { label: '7天',  days: 7 },
  { label: '30天', days: 30 },
  { label: '90天', days: 90 },
  { label: '全部', days: 181 }
]

function applyQuick(opt) {
  activeQuick.value = opt.label
  const end = new Date('2024-06-30')
  const start = new Date(end)
  start.setDate(end.getDate() - opt.days + 1)
  const fmt2 = (d) => d.toISOString().slice(0, 10)
  currentStart.value = fmt2(start) < DATA_MIN ? DATA_MIN : fmt2(start)
  currentEnd.value   = DATA_MAX
  dateRange.value    = [currentStart.value, currentEnd.value]
  loadAll()
}

function onDateChange(val) {
  if (!val) return
  activeQuick.value  = ''
  currentStart.value = val[0]
  currentEnd.value   = val[1]
  loadAll()
}

function disabledDate(d) {
  const s = d.toISOString().slice(0, 10)
  return s < DATA_MIN || s > DATA_MAX
}

// ── Loading 状态 ──────────────────────────────────────────────
const loadingSummary   = ref(false)
const loadingSales     = ref(false)
const loadingAds       = ref(false)
const loadingTraffic   = ref(false)
const loadingInventory = ref(false)

// ── 数据状态 ──────────────────────────────────────────────────
const summary       = reactive({})
const trendPeriod   = ref('day')
const inventoryList = ref([])

const outOfStockCount = computed(
  () => inventoryList.value.filter(i => i.status === 'OUT_OF_STOCK').length)
const warningCount = computed(
  () => inventoryList.value.filter(i => i.status === 'WARNING').length)

// ── ECharts 引用 ──────────────────────────────────────────────
const salesChartRef  = ref(null)
const acosChartRef   = ref(null)
const funnelChartRef = ref(null)
let salesChart, acosChart, funnelChart

// ── GSAP refs ──────────────────────────────────────────────────
const dashRef = ref(null)
let gsapCtx

// Shared dark-mode ECharts style
const darkAxis = {
  axisLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } },
  axisLabel: { color: '#9097A6' },
  splitLine: { lineStyle: { color: 'rgba(255,255,255,0.06)' } },
  nameTextStyle: { color: '#9097A6' }
}
const darkTooltip = {
  backgroundColor: '#16181E',
  borderColor: '#2A2D36',
  textStyle: { color: '#E6E8EE' }
}
const darkLegend = { textStyle: { color: '#9097A6' } }

// ── 数据加载 ──────────────────────────────────────────────────
async function loadAll() {
  loadSummary()
  loadSalesTrend()
  loadAdsChart()
  loadFunnel()
  loadInventory()
}

async function loadSummary() {
  loadingSummary.value = true
  try {
    const res = await api.getSummary(currentStart.value, currentEnd.value)
    Object.assign(summary, res.data || {})
  } catch (e) {
    ElMessage.error('加载指标数据失败')
  } finally {
    loadingSummary.value = false
  }
}

async function loadSalesTrend() {
  loadingSales.value = true
  try {
    const res = await api.getSalesTrend(
      trendPeriod.value, currentStart.value, currentEnd.value)
    const data = res.data || []
    renderSalesChart(data)
  } catch (e) {
    ElMessage.error('加载销售趋势失败')
  } finally {
    loadingSales.value = false
  }
}

async function loadAdsChart() {
  loadingAds.value = true
  try {
    const res = await api.getAdsPerformance(currentStart.value, currentEnd.value)
    const data = res.data || []
    renderAcosChart(data)
  } catch (e) {
    ElMessage.error('加载广告数据失败')
  } finally {
    loadingAds.value = false
  }
}

async function loadFunnel() {
  loadingTraffic.value = true
  try {
    const res = await api.getTrafficFunnel(currentStart.value, currentEnd.value)
    renderFunnelChart(res.data || {})
  } catch (e) {
    ElMessage.error('加载流量漏斗失败')
  } finally {
    loadingTraffic.value = false
  }
}

async function loadInventory() {
  loadingInventory.value = true
  try {
    const res = await api.getInventoryStatus()
    inventoryList.value = res.data || []
  } catch (e) {
    ElMessage.error('加载库存数据失败')
  } finally {
    loadingInventory.value = false
  }
}

// ── ECharts 渲染 ──────────────────────────────────────────────
function renderSalesChart(data) {
  if (!salesChart) return
  const dates    = data.map(d => d.period)
  const revenues = data.map(d => Number(d.revenue).toFixed(0))
  const orders   = data.map(d => d.orders)

  salesChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      ...darkTooltip,
      trigger: 'axis',
      formatter(params) {
        const d = params[0]
        const o = params[1]
        return `${d.axisValue}<br/>
          ${d.marker}销售额：¥${Number(d.value).toLocaleString()}<br/>
          ${o.marker}订单量：${o.value} 单`
      }
    },
    legend: { ...darkLegend, data: ['销售额', '订单量'], bottom: 4 },
    grid: { top: 20, bottom: 52, left: 80, right: 50, containLabel: true },
    xAxis: {
      ...darkAxis,
      type: 'category',
      data: dates,
      axisLabel: { ...darkAxis.axisLabel, rotate: dates.length > 20 ? 45 : 0, fontSize: 11 }
    },
    yAxis: [
      {
        ...darkAxis,
        type: 'value',
        name: '销售额（元）',
        axisLabel: { ...darkAxis.axisLabel, formatter: v => (v >= 1000 ? (v / 1000).toFixed(0) + 'k' : v) }
      },
      {
        ...darkAxis,
        type: 'value',
        name: '订单量',
        splitLine: { show: false }
      }
    ],
    series: [
      {
        name: '销售额',
        type: 'line',
        data: revenues,
        smooth: true,
        yAxisIndex: 0,
        itemStyle: { color: '#FF7A1A' },
        lineStyle: { color: '#FF7A1A', width: 2 },
        areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: 'rgba(255,122,26,0.28)' }, { offset: 1, color: 'rgba(255,122,26,0)' }] } }
      },
      {
        name: '订单量',
        type: 'bar',
        data: orders,
        yAxisIndex: 1,
        itemStyle: { color: 'rgba(74,222,128,0.5)' },
        barMaxWidth: 12
      }
    ]
  }, true)
}

function renderAcosChart(data) {
  if (!acosChart) return
  const dates = data.map(d => d.date)
  const acos  = data.map(d => (Number(d.acos) * 100).toFixed(1))
  const roas  = data.map(d => Number(d.roas).toFixed(2))

  acosChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      ...darkTooltip,
      trigger: 'axis',
      formatter(params) {
        const a = params[0], r = params[1]
        return `${a.axisValue}<br/>
          ${a.marker}ACoS：${a.value}%<br/>
          ${r.marker}ROAS：${r.value}x`
      }
    },
    legend: { ...darkLegend, data: ['ACoS(%)', 'ROAS(x)'], bottom: 4 },
    grid: { top: 30, bottom: 52, left: 55, right: 55, containLabel: true },
    xAxis: {
      ...darkAxis,
      type: 'category',
      data: dates,
      axisLabel: { ...darkAxis.axisLabel, rotate: dates.length > 20 ? 45 : 0, fontSize: 11 }
    },
    yAxis: [
      {
        ...darkAxis,
        type: 'value',
        name: 'ACoS %',
        min: 0,
        max: 50,
        axisLabel: { ...darkAxis.axisLabel, formatter: v => v + '%' }
      },
      {
        ...darkAxis,
        type: 'value',
        name: 'ROAS',
        min: 0,
        splitLine: { show: false },
        axisLabel: { ...darkAxis.axisLabel, formatter: v => v + 'x' }
      }
    ],
    visualMap: {
      show: false,
      seriesIndex: 0,
      pieces: [
        { gt: 0,  lte: 20, color: '#4ADE80' },
        { gt: 20, lte: 35, color: '#E8B14B' },
        { gt: 35,          color: '#FB5F5F' }
      ]
    },
    series: [
      {
        name: 'ACoS(%)',
        type: 'line',
        data: acos,
        smooth: true,
        yAxisIndex: 0,
        markLine: {
          silent: true,
          lineStyle: { type: 'dashed', color: '#E8B14B' },
          data: [{ yAxis: 35, name: '预警线 35%' }],
          label: { formatter: '预警线 {c}%', color: '#9097A6' }
        }
      },
      {
        name: 'ROAS(x)',
        type: 'line',
        data: roas,
        smooth: true,
        yAxisIndex: 1,
        lineStyle: { type: 'dashed', color: '#76A9D6' },
        itemStyle: { color: '#76A9D6' }
      }
    ]
  }, true)
}

function renderFunnelChart(data) {
  if (!funnelChart) return
  const sessions    = data.totalSessions    || 0
  const pageViews   = data.totalPageViews   || 0
  const conversions = data.totalConversions || 0

  const s2p = sessions   > 0 ? ((pageViews   / sessions)   * 100).toFixed(1) : 0
  const p2c = pageViews  > 0 ? ((conversions / pageViews)  * 100).toFixed(1) : 0
  const s2c = sessions   > 0 ? ((conversions / sessions)   * 100).toFixed(1) : 0

  funnelChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter(p) {
        const map = {
          '访客会话':   `会话数：${sessions.toLocaleString()}`,
          '页面浏览':   `浏览量：${pageViews.toLocaleString()}\n会话→浏览：${s2p}%`,
          '成功下单':   `成单数：${conversions.toLocaleString()}\n浏览→成单：${p2c}%\n整体转化：${s2c}%`
        }
        return map[p.name] || p.name
      }
    },
    series: [
      {
        type: 'funnel',
        left: '10%',
        width: '80%',
        top: 20,
        bottom: 20,
        min: 0,
        max: 100,
        minSize: '30%',
        maxSize: '100%',
        sort: 'descending',
        gap: 6,
        label: {
          show: true,
          position: 'inside',
          formatter(p) {
            const vals = {
              '访客会话': sessions.toLocaleString(),
              '页面浏览': pageViews.toLocaleString(),
              '成功下单': conversions.toLocaleString()
            }
            return `${p.name}\n${vals[p.name]}`
          }
        },
        itemStyle: { borderWidth: 0 },
        data: [
          { value: 100, name: '访客会话',   itemStyle: { color: '#FF7A1A' } },
          { value: Math.round(pageViews / sessions * 100) || 60,
            name: '页面浏览',   itemStyle: { color: '#4ADE80' } },
          { value: Math.round(conversions / sessions * 100) || 10,
            name: '成功下单',   itemStyle: { color: '#E8B14B' } }
        ]
      }
    ]
  }, true)
}

// ── 表格辅助方法 ──────────────────────────────────────────────
function getRowClass({ row }) {
  if (row.status === 'OUT_OF_STOCK') return 'row-danger'
  if (row.status === 'WARNING')      return 'row-warning'
  return ''
}

function getDaysClass(row) {
  if (row.status === 'OUT_OF_STOCK') return 'text-danger'
  if (row.status === 'WARNING')      return 'text-warning'
  return 'text-normal'
}

function getStatusType(status) {
  return { NORMAL: 'success', WARNING: 'warning', OUT_OF_STOCK: 'danger' }[status] || 'info'
}

// ── 导出报表 ──────────────────────────────────────────────────
function exportReport() {
  api.exportReport(currentStart.value, currentEnd.value)
  ElMessage.success('报表导出中，请稍候...')
}

// ── 生命周期 ──────────────────────────────────────────────────
onMounted(async () => {
  await nextTick()
  salesChart  = echarts.init(salesChartRef.value,  null, { renderer: 'svg' })
  acosChart   = echarts.init(acosChartRef.value,   null, { renderer: 'svg' })
  funnelChart = echarts.init(funnelChartRef.value,  null, { renderer: 'svg' })

  window.addEventListener('resize', () => {
    salesChart?.resize()
    acosChart?.resize()
    funnelChart?.resize()
  })

  // GSAP entrance animations
  gsapCtx = gsap.context(() => {
    // Header reveal
    gsap.from('.header', { y: -10, duration: 0.5 })

    // MetricCards stagger entrance
    ScrollTrigger.batch('.metric-card', {
      onEnter: (els) => gsap.from(els, {
        y: 12, stagger: 0.08, duration: 0.5, ease: 'power3.out'
      }),
      once: true,
      start: 'top 95%',
    })

    // Chart boxes scale on scroll
    ScrollTrigger.batch('.echarts-box', {
      onEnter: (els) => gsap.from(els, {
        scale: 0.97, stagger: 0.1, duration: 0.6, ease: 'power2.out'
      }),
      once: true,
      start: 'top 90%',
    })

    // Table rows stagger
    ScrollTrigger.batch('.el-table__row', {
      onEnter: (els) => gsap.from(els, {
        x: -6, stagger: 0.04, duration: 0.35, ease: 'power2.out'
      }),
      once: true,
      start: 'top 92%',
    })
  }, dashRef.value)

  loadAll()
})

onUnmounted(() => {
  gsapCtx?.revert()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding: 16px 24px 32px;
  max-width: 1440px;
  margin: 0 auto;
}

/* ── 顶部 Header ── */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  border-radius: 8px;
  padding: 12px 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.35);
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.logo { font-size: 28px; }
.title {
  font-size: 18px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  line-height: 1.3;
}
.subtitle {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 2px;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.quick-btns { flex-shrink: 0; }

/* ── 指标卡片行 ── */
.card-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

/* ── 图表行 ── */
.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}
.chart-card :deep(.el-card__header) {
  padding: 10px 16px;
  border-bottom: 1px solid var(--el-border-color);
  font-weight: 600;
  font-size: 14px;
  color: var(--el-text-color-primary);
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.echarts-box {
  height: 300px;
  width: 100%;
}

/* ── 库存表格行颜色（dark override in tokens.css） ── */
.text-danger  { color: #FB5F5F; font-weight: 600; }
.text-warning { color: #E8B14B; font-weight: 600; }
.text-normal  { color: #4ADE80; }

/* ── 底部 ── */
.footer {
  text-align: center;
  color: var(--el-text-color-placeholder);
  font-size: 12px;
  padding: 12px 0;
}

/* ── 响应式 ── */
@media (max-width: 1100px) {
  .card-row { grid-template-columns: repeat(2, 1fr); }
  .chart-row { grid-template-columns: 1fr; }
}
@media (max-width: 600px) {
  .card-row { grid-template-columns: 1fr 1fr; }
  .header { flex-direction: column; gap: 10px; align-items: flex-start; }
}
</style>
