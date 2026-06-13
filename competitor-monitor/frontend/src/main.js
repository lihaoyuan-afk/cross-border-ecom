import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import VueECharts from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart } from 'echarts/charts'
import {
  GridComponent, TooltipComponent,
  LegendComponent, TitleComponent, MarkPointComponent,
} from 'echarts/components'

// 按需注册 ECharts 组件（减小打包体积）
use([
  CanvasRenderer, LineChart, BarChart,
  GridComponent, TooltipComponent, LegendComponent, TitleComponent, MarkPointComponent,
])

const app = createApp(App)

// 注册所有 Element Plus 图标（面试展示用，生产项目应按需引入）
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)
app.use(ElementPlus)
app.component('VChart', VueECharts)
app.mount('#app')
