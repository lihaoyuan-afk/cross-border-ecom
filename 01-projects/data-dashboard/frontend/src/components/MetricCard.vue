<template>
  <el-card class="metric-card" shadow="never">
    <div class="card-body">
      <div class="left">
        <div class="card-title">
          {{ title }}
          <el-tooltip v-if="tooltip" :content="tooltip" placement="top">
            <el-icon style="color:#C0C4CC;margin-left:4px;cursor:help"><InfoFilled /></el-icon>
          </el-tooltip>
        </div>
        <div class="card-value">{{ value }}</div>
        <div class="card-change" :style="{ color: change.color }">
          {{ change.text }}
          <span class="change-label">环比上期</span>
        </div>
      </div>
      <div class="icon-wrap" :style="{ background: color + '18', color }">
        {{ icon }}
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { InfoFilled } from '@element-plus/icons-vue'

defineProps({
  title:   { type: String,  required: true },
  value:   { type: String,  required: true },
  change:  { type: Object,  default: () => ({ text: '—', color: '#909399' }) },
  icon:    { type: String,  default: '📊' },
  color:   { type: String,  default: '#409EFF' },
  tooltip: { type: String,  default: '' }
})
</script>

<style scoped>
.metric-card {
  border-radius: 8px;
  border: 1px solid var(--el-border-color);
}
.metric-card :deep(.el-card__body) {
  padding: 16px 20px;
}
.card-body {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.left { flex: 1; }
.card-title {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin-bottom: 6px;
}
.card-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  line-height: 1.2;
  letter-spacing: -0.5px;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-variant-numeric: tabular-nums;
}
.card-change {
  font-size: 12px;
  margin-top: 6px;
  font-weight: 500;
}
.change-label {
  font-weight: 400;
  color: var(--el-text-color-placeholder);
  margin-left: 4px;
}
.icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
  margin-left: 12px;
}
</style>
