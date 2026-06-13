<template>
  <div>
    <div class="page-hd">
      <el-button text @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>&nbsp;返回
      </el-button>
      <h2 class="page-title">商品详情 &nbsp;<el-text type="primary">{{ asin }}</el-text></h2>
    </div>

    <!-- 时间范围切换 -->
    <el-radio-group v-model="days" style="margin-bottom: 16px" @change="loadCharts">
      <el-radio-button :value="7">近 7 天</el-radio-button>
      <el-radio-button :value="30">近 30 天</el-radio-button>
      <el-radio-button :value="90">近 90 天</el-radio-button>
    </el-radio-group>

    <!-- 价格折线图 -->
    <el-card shadow="never" style="margin-bottom: 16px">
      <template #header><b>价格走势（USD）</b></template>
      <div v-if="priceData.length === 0 && !priceLoading" class="empty-tip">
        暂无价格数据
      </div>
      <v-chart v-else :option="priceOption" style="height:300px" autoresize v-loading="priceLoading" />
    </el-card>

    <!-- BSR 折线图 -->
    <el-card shadow="never">
      <template #header><b>BSR 排名走势（排名越低越好）</b></template>
      <div v-if="bsrData.length === 0 && !bsrLoading" class="empty-tip">
        暂无 BSR 数据
      </div>
      <v-chart v-else :option="bsrOption" style="height:300px" autoresize v-loading="bsrLoading" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPriceHistory, getBsrHistory } from '../api/index.js'

const route      = useRoute()
const asin       = route.params.asin
const days       = ref(30)
const priceData  = ref([])
const bsrData    = ref([])
const priceLoading = ref(false)
const bsrLoading   = ref(false)

// ECharts 价格折线图配置
const priceOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    formatter: (p) => `${p[0].axisValue}<br/>价格：<b>$${p[0].value}</b>`,
  },
  grid: { left: 60, right: 20, top: 30, bottom: 55 },
  xAxis: {
    type: 'category',
    data: priceData.value.map(r => r.recordedAt?.slice(0, 10)),
    axisLabel: { rotate: 30, fontSize: 11 },
  },
  yAxis: {
    type: 'value',
    name: 'USD',
    axisLabel: { formatter: '${value}' },
  },
  series: [{
    name: '价格',
    type: 'line',
    data: priceData.value.map(r => r.price),
    smooth: true,
    symbol: 'none',
    lineStyle: { color: '#409eff', width: 2 },
    areaStyle: {
      color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(64,158,255,0.25)' },
          { offset: 1, color: 'rgba(64,158,255,0)' },
        ],
      },
    },
    markPoint: {
      data: [{ type: 'min', name: '最低价' }, { type: 'max', name: '最高价' }],
      symbolSize: 40,
    },
  }],
}))

// ECharts BSR 排名折线图配置
const bsrOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    formatter: (p) => `${p[0].axisValue}<br/>排名：<b>#${p[0].value}</b>`,
  },
  grid: { left: 75, right: 20, top: 30, bottom: 55 },
  xAxis: {
    type: 'category',
    data: bsrData.value.map(r => r.recordedAt?.slice(0, 10)),
    axisLabel: { rotate: 30, fontSize: 11 },
  },
  yAxis: {
    type: 'value',
    name: '排名',
    inverse: true,   // 排名越小越好，Y 轴反转使"好"在上方
    axisLabel: { formatter: '#{value}' },
  },
  series: [{
    name: 'BSR 排名',
    type: 'line',
    data: bsrData.value.map(r => r.bsrRank),
    smooth: true,
    symbol: 'none',
    lineStyle: { color: '#67c23a', width: 2 },
    areaStyle: {
      color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(103,194,58,0.25)' },
          { offset: 1, color: 'rgba(103,194,58,0)' },
        ],
      },
    },
    markPoint: {
      data: [{ type: 'min', name: '最佳排名' }],
      symbolSize: 40,
    },
  }],
}))

const loadCharts = async () => {
  priceLoading.value = true
  bsrLoading.value   = true
  try {
    const [pr, br] = await Promise.all([
      getPriceHistory(asin, days.value),
      getBsrHistory(asin, days.value),
    ])
    priceData.value = pr.data || []
    bsrData.value   = br.data || []
  } finally {
    priceLoading.value = false
    bsrLoading.value   = false
  }
}

onMounted(loadCharts)
</script>

<style scoped>
.page-hd { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.page-title { font-size: 18px; font-weight: 600; color: #303133; }
.empty-tip { text-align: center; color: #909399; padding: 60px 0; }
</style>
