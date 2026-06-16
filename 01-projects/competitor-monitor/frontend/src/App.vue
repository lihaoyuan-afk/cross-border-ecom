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
        background-color="#16181E"
        text-color="#9097A6"
        active-text-color="#FF7A1A"
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

    <!-- 右侧内容区（路由切换过渡） -->
    <el-main class="main">
      <router-view v-slot="{ Component }">
        <transition :css="false" @leave="onLeave" @enter="onEnter">
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { getUnreadCount } from './api/index.js'
import { gsap } from './animation/gsap.js'

const route = useRoute()
const unreadCount = ref(0)
let badgeTween

// Route transitions
function onLeave(el, done) {
  gsap.to(el, { y: -8, autoAlpha: 0, duration: 0.2, ease: 'power2.in', onComplete: done })
}
function onEnter(el, done) {
  gsap.from(el, { y: 8, autoAlpha: 0, duration: 0.28, ease: 'power3.out', onComplete: done })
}

onMounted(async () => {
  // Logo slide in
  gsap.from('.logo', { x: -10, duration: 0.45 })
  gsap.from('.el-menu-item', { x: -6, stagger: 0.07, duration: 0.38, delay: 0.2 })

  try {
    const res = await getUnreadCount()
    unreadCount.value = res.data || 0
  } catch { /* 静默处理，不影响主流程 */ }

  // Badge pulse for unread alerts
  if (unreadCount.value > 0) {
    badgeTween = gsap.to('.nav-badge .el-badge__content', {
      scale: 1.1, duration: 0.9, yoyo: true, repeat: -1, ease: 'sine.inOut'
    })
  }
})

onUnmounted(() => {
  badgeTween?.kill()
})
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #0E0F12;
  font-family: 'Inter', 'PingFang SC', -apple-system, BlinkMacSystemFont, sans-serif;
}

.app-wrap { min-height: 100vh; }

.sidebar {
  background: #16181E;
  border-right: 1px solid #2A2D36;
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
  color: #E6E8EE;
  font-size: 15px;
  font-weight: 600;
  border-bottom: 1px solid #2A2D36;
}

.logo .el-icon { color: #FF7A1A; }

.el-menu { border-right: none !important; background-color: #16181E !important; }

.el-menu-item {
  height: 48px;
  line-height: 48px;
  border-left: 2px solid transparent;
  transition: border-color 0.2s;
}
.el-menu-item.is-active { border-left-color: #FF7A1A !important; }

.nav-badge { margin-left: auto; }
.nav-badge .el-badge__content { transform: translateY(-2px); }

.main { padding: 24px; overflow-y: auto; min-height: 100vh; background: #0E0F12; }

/* Page title */
.page-title {
  font-size: 18px;
  font-weight: 700;
  color: #E6E8EE;
  margin-bottom: 20px;
}
</style>
