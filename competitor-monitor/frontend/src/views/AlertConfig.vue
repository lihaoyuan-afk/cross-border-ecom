<template>
  <div>
    <h2 class="page-title">预警配置</h2>

    <el-row :gutter="20">
      <!-- 左侧：阈值配置表单 -->
      <el-col :span="10">
        <el-card shadow="never">
          <template #header><b>预警阈值设置</b></template>

          <el-form :model="form" label-width="170px" label-position="left" style="max-width: 420px">
            <el-form-item label="目标 ASIN">
              <el-input
                v-model="form.asin"
                placeholder="留空则修改全局默认配置"
                clearable
                @change="loadConfig"
              />
              <div class="tip">留空时修改对所有商品生效的默认配置</div>
            </el-form-item>

            <el-form-item label="价格下跌预警 (%)">
              <el-input-number
                v-model="form.priceDropPct"
                :min="1" :max="50" :precision="1" style="width: 100%"
              />
            </el-form-item>

            <el-form-item label="价格上涨预警 (%)">
              <el-input-number
                v-model="form.priceRisePct"
                :min="1" :max="50" :precision="1" style="width: 100%"
              />
            </el-form-item>

            <el-form-item label="BSR 变动预警 (%)">
              <el-input-number
                v-model="form.bsrChangePct"
                :min="1" :max="100" :precision="1" style="width: 100%"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" :loading="saving" @click="handleSave">保存配置</el-button>
              <el-button @click="loadConfig">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 右侧：预警历史 -->
      <el-col :span="14">
        <el-card shadow="never">
          <template #header>
            <div class="card-hd">
              <b>预警记录</b>
              <el-radio-group v-model="readFilter" size="small" @change="() => { alertPage = 1; loadAlerts() }">
                <el-radio-button :value="null">全部</el-radio-button>
                <el-radio-button :value="0">未读</el-radio-button>
                <el-radio-button :value="1">已读</el-radio-button>
              </el-radio-group>
            </div>
          </template>

          <el-table :data="alerts" v-loading="alertLoading" stripe size="small" style="width:100%">
            <el-table-column prop="asin" label="ASIN" width="145" />
            <el-table-column label="类型" width="110">
              <template #default="{ row }">
                <el-tag :type="typeTagMap[row.alertType]" size="small">
                  {{ typeLabelMap[row.alertType] || row.alertType }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="变化" width="85" align="right">
              <template #default="{ row }">
                <span :class="row.changePct < 0 ? 'c-red' : 'c-orange'">
                  {{ row.changePct > 0 ? '+' : '' }}{{ row.changePct }}%
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="triggeredAt" label="时间" min-width="155" show-overflow-tooltip />
            <el-table-column width="75" align="center">
              <template #default="{ row }">
                <el-button
                  v-if="!row.isRead" text type="primary" size="small"
                  @click="handleMarkRead(row)"
                >已读</el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="pager">
            <el-pagination
              v-model:current-page="alertPage"
              :total="alertTotal"
              :page-size="15"
              layout="prev, pager, next, total"
              small
              @current-change="loadAlerts"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getAlertConfig, saveAlertConfig, getAlertList, markAlertRead } from '../api/index.js'
import { ElMessage } from 'element-plus'

const form = reactive({ asin: '', priceDropPct: 10, priceRisePct: 15, bsrChangePct: 20 })
const saving = ref(false)

const alerts     = ref([])
const alertLoading = ref(false)
const alertPage  = ref(1)
const alertTotal = ref(0)
const readFilter = ref(null)

const typeLabelMap = {
  PRICE_DROP: '价格下跌', PRICE_RISE: '价格上涨',
  BSR_IMPROVE: 'BSR 改善', BSR_DROP: 'BSR 下滑',
}
const typeTagMap = {
  PRICE_DROP: 'danger', PRICE_RISE: 'warning',
  BSR_IMPROVE: 'success', BSR_DROP: 'info',
}

const loadConfig = async () => {
  const res = await getAlertConfig(form.asin || undefined)
  if (res.data) {
    form.priceDropPct = Number(res.data.priceDropPct)
    form.priceRisePct = Number(res.data.priceRisePct)
    form.bsrChangePct = Number(res.data.bsrChangePct)
  }
}

const handleSave = async () => {
  saving.value = true
  try {
    await saveAlertConfig({
      asin: form.asin || null,
      priceDropPct: form.priceDropPct,
      priceRisePct: form.priceRisePct,
      bsrChangePct: form.bsrChangePct,
    })
    ElMessage.success('配置已保存')
  } finally {
    saving.value = false
  }
}

const loadAlerts = async () => {
  alertLoading.value = true
  try {
    const res = await getAlertList({
      pageNum: alertPage.value, pageSize: 15,
      isRead: readFilter.value,
    })
    alerts.value    = res.data?.records || []
    alertTotal.value = res.data?.total   || 0
  } finally {
    alertLoading.value = false
  }
}

const handleMarkRead = async (row) => {
  await markAlertRead(row.id)
  row.isRead = 1
}

onMounted(() => { loadConfig(); loadAlerts() })
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: 600; margin-bottom: 20px; color: #303133; }
.card-hd { display: flex; justify-content: space-between; align-items: center; }
.tip { font-size: 12px; color: #909399; margin-top: 4px; line-height: 1.4; }
.pager { margin-top: 12px; display: flex; justify-content: flex-end; }
.c-red { color: #f56c6c; font-weight: 600; }
.c-orange { color: #e6a23c; font-weight: 600; }
</style>
