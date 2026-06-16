<template>
  <div ref="appRef">
    <!-- Header -->
    <header class="app-header">
      <span style="font-size:22px">📊</span>
      <h1>Amazon Listing 质量评分引擎</h1>
      <span class="subtitle">基于 A9 算法 · 8 维评分模型 · AI 优化建议</span>
    </header>

    <main class="app-body">
      <!-- ── LEFT: 输入区 ── -->
      <section class="panel">
        <div class="panel-title">Listing 数据输入</div>

        <div class="field">
          <label>产品标题 <span>英文</span></label>
          <textarea
            v-model="form.title"
            rows="3"
            placeholder="粘贴 Amazon 产品标题..."
          />
          <div class="char-count" :class="titleLenClass">
            {{ form.title.length }} 字符
            <span v-if="form.title.length < 80"> · 建议 80-200</span>
            <span v-else-if="form.title.length > 200"> · 已超出推荐长度</span>
            <span v-else> · ✓ 长度合适</span>
          </div>
        </div>

        <div class="field">
          <label>Bullet Points <span>每行一条，最多5条</span></label>
          <textarea
            v-model="bulletsText"
            rows="7"
            placeholder="BULLET 1: 粘贴第一条卖点&#10;BULLET 2: 粘贴第二条卖点&#10;..."
          />
          <div class="char-count">{{ bulletCount }} / 5 条</div>
        </div>

        <div class="field">
          <label>产品描述 <span>建议 1000+ 字符</span></label>
          <textarea
            v-model="form.description"
            rows="5"
            placeholder="粘贴产品 Description..."
          />
          <div class="char-count" :class="descLenClass">
            {{ form.description.length }} 字符
          </div>
        </div>

        <div class="input-row">
          <div class="field">
            <label>图片数量</label>
            <input type="number" v-model.number="form.image_count" min="0" max="9" placeholder="7" />
          </div>
          <div class="field">
            <label>评论数量</label>
            <input type="number" v-model.number="form.review_count" min="0" placeholder="50" />
          </div>
        </div>

        <div class="input-row">
          <div class="field">
            <label>当前定价 ($)</label>
            <input type="number" v-model.number="form.price" min="0" step="0.01" placeholder="29.99" />
          </div>
          <div class="field">
            <label>类目均价 ($)</label>
            <input type="number" v-model.number="form.avg_category_price" min="0" step="0.01" placeholder="25.00" />
          </div>
        </div>

        <div class="field">
          <label>目标关键词 <span>用于 AI 重写</span></label>
          <input type="text" v-model="form.target_keyword" placeholder="e.g. stainless steel water bottle" />
        </div>

        <button class="btn btn-primary" @click="handleScore" :disabled="loading.score || !form.title">
          <span v-if="loading.score"><span class="loading-spinner"></span>评分中...</span>
          <span v-else>🔍 开始评分</span>
        </button>

        <button class="btn btn-secondary" @click="loadDemo">
          📋 加载演示数据
        </button>
      </section>

      <!-- ── CENTER: 雷达图 + 维度详情 ── -->
      <section class="panel" style="border-right: 1px solid var(--border)">
        <div class="panel-title">评分结果</div>

        <template v-if="scoreResult">
          <!-- 总分 -->
          <div class="total-score-wrap">
            <div class="total-score-number" :class="`grade-${scoreResult.grade.toLowerCase()}`">
              {{ displayScore }}
            </div>
            <div style="margin-top:4px">
              <span class="grade-badge" :class="`grade-${scoreResult.grade.toLowerCase()}`">
                等级 {{ scoreResult.grade }}
              </span>
            </div>
            <div class="summary-text">{{ scoreResult.summary }}</div>
          </div>

          <!-- 雷达图 -->
          <div id="radar-chart" ref="radarRef"></div>

          <!-- 维度详情列表 -->
          <div class="dim-list">
            <div
              v-for="d in scoreResult.dimensions"
              :key="d.name"
              class="dim-item"
              :class="dimClass(d.score)"
            >
              <div class="dim-header">
                <span class="dim-name">{{ d.name }}</span>
                <span class="dim-score" :class="dimClass(d.score)">{{ d.score }} / 10</span>
              </div>
              <div class="score-bar-bg">
                <div
                  class="score-bar-fill"
                  :style="{ background: dimColor(d.score) }"
                />
              </div>
              <div class="dim-issue">{{ d.issue }}</div>
            </div>
          </div>
        </template>

        <div v-else class="empty-state">
          <div class="icon">📈</div>
          <p>填写左侧 Listing 数据<br/>点击「开始评分」获取 8 维分析</p>
        </div>
      </section>

      <!-- ── RIGHT: 优化建议 + AI 重写 ── -->
      <section class="panel">
        <div class="panel-title">优化建议</div>

        <!-- 优化建议区 -->
        <template v-if="suggestions">
          <div class="seo-summary">{{ suggestions.seo_summary }}</div>

          <div class="suggestions-panel">
            <div v-if="suggestions.priority_actions?.length">
              <div class="suggest-section-title priority">⚠ 紧急修复（{{ suggestions.priority_actions.length }}项）</div>
              <div v-for="item in suggestions.priority_actions" :key="item.dimension" class="suggest-item">
                <div class="suggest-item-dim">{{ item.dimension }} · {{ item.current_score }}/10</div>
                <div class="suggest-item-action">{{ item.action }}</div>
              </div>
            </div>

            <div v-if="suggestions.improvements?.length">
              <div class="suggest-section-title improve">↑ 重点提升（{{ suggestions.improvements.length }}项）</div>
              <div v-for="item in suggestions.improvements" :key="item.dimension" class="suggest-item">
                <div class="suggest-item-dim">{{ item.dimension }} · {{ item.current_score }}/10</div>
                <div class="suggest-item-action">{{ item.action }}</div>
              </div>
            </div>

            <div v-if="suggestions.quick_wins?.length">
              <div class="suggest-section-title quick">✓ 速效优化（{{ suggestions.quick_wins.length }}项）</div>
              <div v-for="item in suggestions.quick_wins" :key="item.dimension" class="suggest-item">
                <div class="suggest-item-dim">{{ item.dimension }} · {{ item.current_score }}/10</div>
                <div class="suggest-item-action">{{ item.action }}</div>
              </div>
            </div>
          </div>

          <button class="btn btn-secondary" @click="handleOptimize" :disabled="loading.optimize" style="margin-top:8px">
            <span v-if="loading.optimize"><span class="loading-spinner"></span>分析中...</span>
            <span v-else>🔄 刷新建议</span>
          </button>
        </template>

        <template v-else-if="scoreResult">
          <button class="btn btn-secondary" @click="handleOptimize" :disabled="loading.optimize">
            <span v-if="loading.optimize"><span class="loading-spinner"></span>分析中...</span>
            <span v-else>💡 获取优化建议</span>
          </button>
        </template>

        <!-- 分割线 -->
        <div v-if="scoreResult" style="border-top: 1px solid var(--border); margin: 16px 0;"></div>

        <!-- AI 重写区 -->
        <template v-if="scoreResult">
          <div class="panel-title" style="margin-bottom:10px">AI 重写对比</div>

          <button class="btn btn-ai" @click="handleRewrite" :disabled="loading.rewrite">
            <span v-if="loading.rewrite"><span class="loading-spinner"></span>AI 重写中...</span>
            <span v-else>✨ AI 重写 Listing</span>
          </button>

          <template v-if="rewriteResult">
            <!-- 对比 tabs -->
            <div class="rewrite-tabs" ref="tabsRef" style="margin-top:12px">
              <button class="tab-btn" :class="{active: rewriteTab==='original'}" @click="rewriteTab='original'">原始</button>
              <button class="tab-btn" :class="{active: rewriteTab==='title'}" @click="rewriteTab='title'">标题</button>
              <button class="tab-btn" :class="{active: rewriteTab==='bullets'}" @click="rewriteTab='bullets'">Bullets</button>
              <button class="tab-btn" :class="{active: rewriteTab==='desc'}" @click="rewriteTab='desc'">描述</button>
              <div class="tab-ink" ref="tabInkRef"></div>
            </div>

            <div class="rewrite-content">
              <template v-if="rewriteTab==='original'">
                <strong style="color:var(--text-muted);font-size:11px">原始标题：</strong>
                <div style="margin-bottom:12px">{{ form.title || '（未填写）' }}</div>
                <strong style="color:var(--text-muted);font-size:11px">原始 Bullets（{{ bulletLines.length }} 条）：</strong>
                <div v-for="(b,i) in bulletLines" :key="i" style="margin-top:4px">{{ i+1 }}. {{ b }}</div>
              </template>

              <template v-else-if="rewriteTab==='title'">
                <strong style="color:var(--text-muted);font-size:11px">优化后标题：</strong>
                <div style="margin-top:6px">{{ rewriteResult.optimized_title }}</div>
                <div style="margin-top:8px;font-size:11px;color:var(--text-muted)">
                  字符数：{{ rewriteResult.optimized_title?.length ?? 0 }}
                </div>
              </template>

              <template v-else-if="rewriteTab==='bullets'">
                <strong style="color:var(--text-muted);font-size:11px">优化后 Bullets：</strong>
                <div v-for="(b,i) in rewriteResult.optimized_bullets" :key="i" style="margin-top:10px">
                  <span style="color:var(--accent2);font-size:11px">{{ i+1 }}</span>
                  {{ b }}
                </div>
              </template>

              <template v-else-if="rewriteTab==='desc'">
                <strong style="color:var(--text-muted);font-size:11px">优化后描述：</strong>
                <div style="margin-top:6px;white-space:pre-wrap">{{ rewriteResult.optimized_description }}</div>
              </template>
            </div>

            <!-- 优化说明 -->
            <div class="notes-list" v-if="rewriteResult.optimization_notes?.length">
              <div style="font-size:11px;color:var(--text-muted);margin-bottom:6px;font-weight:600">优化逻辑说明：</div>
              <div v-for="note in rewriteResult.optimization_notes" :key="note" class="note-item">
                {{ note }}
              </div>
            </div>

            <!-- Mock 提示 -->
            <div v-if="rewriteResult.is_mock" class="mock-notice">
              ℹ {{ rewriteResult.mock_notice }}
            </div>
          </template>
        </template>

        <div v-if="!scoreResult" class="empty-state" style="padding-top:20px">
          <div class="icon">🤖</div>
          <p>评分后可获取 AI<br/>驱动的优化建议</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
import { gsap, Flip } from './animation/gsap.js'

// ── Animation refs ──
const appRef = ref(null)
const tabsRef = ref(null)
const tabInkRef = ref(null)
const displayScore = ref(0)
const scoreProxy = { val: 0 }
let gsapCtx

// ── State ──
const form = ref({
  title: '',
  description: '',
  image_count: 0,
  price: 0,
  avg_category_price: 0,
  review_count: 0,
  target_keyword: '',
  category: 'General',
})

const bulletsText = ref('')
const scoreResult = ref(null)
const suggestions = ref(null)
const rewriteResult = ref(null)
const rewriteTab = ref('title')
const radarRef = ref(null)
let radarChart = null

const loading = ref({ score: false, optimize: false, rewrite: false })

// ── Computed ──
const bulletLines = computed(() =>
  bulletsText.value.split('\n').map(l => l.trim()).filter(Boolean)
)

const bulletCount = computed(() => bulletLines.value.length)

const titleLenClass = computed(() => {
  const l = form.value.title.length
  if (l >= 80 && l <= 200) return 'good'
  if (l > 60) return 'warn'
  return ''
})

const descLenClass = computed(() => {
  const l = form.value.description.length
  if (l >= 1000) return 'good'
  if (l >= 500) return 'warn'
  return ''
})

// ── Helpers ──
const buildPayload = () => ({
  ...form.value,
  bullets: bulletLines.value,
})

const dimClass = (score) => {
  if (score >= 8) return 'score-high'
  if (score >= 5) return 'score-mid'
  return 'score-low'
}

const dimColor = (score) => {
  if (score >= 8) return 'var(--green)'
  if (score >= 5) return 'var(--yellow)'
  return 'var(--red)'
}

// ── Radar chart ──
const initRadar = async (dimensions) => {
  await nextTick()
  if (!radarRef.value) return

  if (!radarChart) {
    radarChart = echarts.init(radarRef.value, 'dark')
  }

  const indicators = dimensions.map(d => ({ name: d.name, max: 10 }))
  const values = dimensions.map(d => d.score)

  radarChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'item' },
    radar: {
      indicator: indicators,
      radius: '65%',
      center: ['50%', '50%'],
      shape: 'polygon',
      splitNumber: 5,
      axisName: { color: '#7a7f9a', fontSize: 11 },
      splitArea: {
        areaStyle: {
          color: ['rgba(255,122,26,0.03)', 'rgba(255,122,26,0.05)',
                  'rgba(255,122,26,0.08)', 'rgba(255,122,26,0.11)',
                  'rgba(255,122,26,0.14)']
        }
      },
      axisLine: { lineStyle: { color: 'rgba(255,122,26,0.2)' } },
      splitLine: { lineStyle: { color: 'rgba(255,122,26,0.15)' } },
    },
    series: [{
      type: 'radar',
      data: [{
        value: values,
        name: 'Listing 评分',
        symbol: 'circle',
        symbolSize: 5,
        areaStyle: { color: 'rgba(255,149,0,0.15)' },
        lineStyle: { color: '#ff9500', width: 2 },
        itemStyle: { color: '#ff9500' },
        label: {
          show: true,
          formatter: (p) => p.value,
          fontSize: 11,
          color: '#e8eaf0',
        }
      }]
    }]
  })
}

// ── GSAP: tab ink helper ──
function moveTabInk(activeBtn) {
  if (!tabInkRef.value || !activeBtn) return
  gsap.to(tabInkRef.value, {
    x: activeBtn.offsetLeft,
    width: activeBtn.offsetWidth,
    duration: 0.25,
    ease: 'power2.out',
  })
}

// ── GSAP: lifecycle ──
onMounted(() => {
  gsapCtx = gsap.context(() => {
    gsap.from('.app-header', { x: -10, duration: 0.5 })
    gsap.from('.field', { y: 8, stagger: 0.05, duration: 0.4, delay: 0.25 })
    gsap.from('.btn', { y: 6, stagger: 0.07, duration: 0.35, delay: 0.45 })
  }, appRef.value)
})

onUnmounted(() => {
  gsapCtx?.revert()
})

// ── GSAP: score result ──
watch(scoreResult, async (result) => {
  if (!result) { displayScore.value = 0; return }
  await nextTick()

  // Count-up total score
  scoreProxy.val = 0
  gsap.to(scoreProxy, {
    val: result.total_score,
    duration: 1.0,
    ease: 'power3.out',
    onUpdate() { displayScore.value = Math.round(scoreProxy.val) },
  })

  // Grade badge pop in after count finishes
  gsap.from('.grade-badge', { scale: 0.82, autoAlpha: 0, duration: 0.35, delay: 0.65 })

  // Radar chart scale entrance
  gsap.from('#radar-chart', { scale: 0.92, autoAlpha: 0, duration: 0.6, delay: 0.15 })

  // Dim-items stagger
  gsap.from('.dim-item', { y: 10, autoAlpha: 0, stagger: 0.07, duration: 0.45, delay: 0.3, overwrite: 'auto' })

  // Score bars: tween from 0 to actual percentage
  const bars = appRef.value?.querySelectorAll('.score-bar-fill') ?? []
  result.dimensions.forEach((d, i) => {
    gsap.to(bars[i], { width: (d.score * 10) + '%', duration: 0.7, delay: 0.35 + i * 0.06, ease: 'power2.out', overwrite: true })
  })
})

// ── GSAP: suggestions stagger ──
watch(suggestions, async (val) => {
  if (!val) return
  await nextTick()
  gsap.from('.suggest-item', { y: 8, autoAlpha: 0, stagger: 0.05, duration: 0.4, delay: 0.1, overwrite: 'auto' })
})

// ── GSAP: rewrite result ──
watch(rewriteResult, async (val) => {
  if (!val) return
  await nextTick()
  gsap.from('.rewrite-content', { y: 6, autoAlpha: 0, duration: 0.35 })
  // Init tab ink on first appear
  const activeBtn = tabsRef.value?.querySelector('.tab-btn.active')
  moveTabInk(activeBtn)
})

// ── GSAP: tab ink slide ──
watch(rewriteTab, async () => {
  await nextTick()
  const activeBtn = tabsRef.value?.querySelector('.tab-btn.active')
  moveTabInk(activeBtn)
  gsap.from('.rewrite-content', { autoAlpha: 0, duration: 0.2 })
})

// ── API calls ──
const handleScore = async () => {
  loading.value.score = true
  suggestions.value = null
  rewriteResult.value = null
  try {
    const res = await axios.post('/api/score', buildPayload())
    scoreResult.value = res.data
    initRadar(res.data.dimensions)
  } catch (e) {
    alert('评分失败：' + (e.response?.data?.error || e.message))
  } finally {
    loading.value.score = false
  }
}

const handleOptimize = async () => {
  loading.value.optimize = true
  try {
    const res = await axios.post('/api/optimize', buildPayload())
    suggestions.value = res.data
  } catch (e) {
    alert('获取建议失败：' + (e.response?.data?.error || e.message))
  } finally {
    loading.value.optimize = false
  }
}

const handleRewrite = async () => {
  loading.value.rewrite = true
  rewriteTab.value = 'title'
  try {
    const res = await axios.post('/api/rewrite', buildPayload())
    rewriteResult.value = res.data
  } catch (e) {
    alert('AI 重写失败：' + (e.response?.data?.error || e.message))
  } finally {
    loading.value.rewrite = false
  }
}

// ── Demo data ──
const loadDemo = () => {
  form.value = {
    title: 'Water Bottle Stainless Steel 32oz Vacuum Insulated Water Bottle BPA Free Leak Proof Lid for Gym Sports Travel Hiking Office',
    description: 'This water bottle is made of stainless steel. It keeps drinks cold. It has a lid. Good for travel.',
    image_count: 4,
    price: 34.99,
    avg_category_price: 25.00,
    review_count: 12,
    target_keyword: 'stainless steel water bottle',
    category: 'Sports & Outdoors',
  }
  bulletsText.value = [
    'Keeps drinks cold',
    'Made of stainless steel',
    'Has a leak proof lid',
  ].join('\n')

  scoreResult.value = null
  suggestions.value = null
  rewriteResult.value = null
}

// Resize chart with window
window.addEventListener('resize', () => radarChart?.resize())
</script>
