<template>
  <div>
    <div class="page-hd">
      <h2 class="page-title">商品列表</h2>
      <el-input
        v-model="keyword"
        placeholder="搜索 ASIN、品牌或商品名..."
        style="width: 300px"
        clearable
        @input="onSearch"
      >
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>
    </div>

    <el-card shadow="never">
      <el-table
        :data="products"
        v-loading="loading"
        stripe
        highlight-current-row
        style="width: 100%; cursor: pointer"
        @row-click="(row) => goDetail(row.asin)"
      >
        <el-table-column prop="asin" label="ASIN" width="150" />
        <el-table-column prop="brand" label="品牌" width="120" />
        <el-table-column prop="subCategory" label="子类目" width="150" />
        <el-table-column prop="title" label="商品标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" width="110" align="center">
          <template #default="{ row }">
            <el-button type="primary" text size="small" @click.stop="goDetail(row.asin)">
              查看详情 →
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pager">
        <el-pagination
          v-model:current-page="pageNum"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @change="loadList"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProductList } from '../api/index.js'

const router  = useRouter()
const products = ref([])
const loading  = ref(false)
const keyword  = ref('')
const pageNum  = ref(1)
const pageSize = ref(20)
const total    = ref(0)
let searchTimer = null

const loadList = async () => {
  loading.value = true
  try {
    const res = await getProductList({
      pageNum: pageNum.value,
      pageSize: pageSize.value,
      keyword: keyword.value || undefined,
    })
    products.value = res.data?.records || []
    total.value    = res.data?.total   || 0
  } finally {
    loading.value = false
  }
}

// 防抖搜索：输入停止 300ms 后再发请求
const onSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { pageNum.value = 1; loadList() }, 300)
}

const goDetail = (asin) => router.push(`/products/${asin}`)

onMounted(loadList)
</script>

<style scoped>
.page-hd { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-title { font-size: 20px; font-weight: 600; color: #303133; }
.pager { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
