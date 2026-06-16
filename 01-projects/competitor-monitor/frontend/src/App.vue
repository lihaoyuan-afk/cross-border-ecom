<template>
  <el-container class="app-wrap">
    <!-- 左侧导航栏 -->
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <el-icon size="22"><DataAnalysis /></el-icon>
        <span>竞品监控系统</span>
      </div>

      <el-menu
        :default-active="route.path"
        router
        background-color="#1a1a2e"
        text-color="#a0a8b8"
        active-text-color="#409eff"
      >
        <el-menu-item index="/">
          <el-icon><Monitor /></el-icon>
          <span>监控看板</span>
        </el-menu-item>
        <el-menu-item index="/products">
          <el-icon><Goods /></el-icon>
          <span>商品列表</span>
        </el-menu-item>
        <el-menu-item index="/alerts/config">
          <el-icon><Bell /></el-icon>
          <span>预警配置</span>
          <el-badge v-if="unreadCount > 0" :value="unreadCount" class="nav-badge" />
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 右侧内容区 -->
    <el-main class="main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getUnreadCount } from './api/index.js'

const route = useRoute()
const unreadCount = ref(0)

onMounted(async () => {
  try {
    const res = await getUnreadCount()
    unreadCount.value = res.data || 0
  } catch { /* 静默处理，不影响主流程 */ }
})
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #f0f2f5; font-family: 'PingFang SC', -apple-system, BlinkMacSystemFont, sans-serif; }

.app-wrap { min-height: 100vh; }

.sidebar {
  background: #1a1a2e;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  border-bottom: 1px solid #2d2d44;
}

.el-menu { border-right: none !important; }

.el-menu-item { height: 48px; line-height: 48px; }

.nav-badge { margin-left: auto; }
.nav-badge .el-badge__content { transform: translateY(-2px); }

.main { padding: 24px; overflow-y: auto; min-height: 100vh; }
</style>
