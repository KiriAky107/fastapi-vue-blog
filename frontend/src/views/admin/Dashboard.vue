<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { postApi } from '@/api/post'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const stats = ref({
  postCount: 0,
  userCount: 0,
  viewCount: 0,
})
const recentPosts = ref<any[]>([])
const loading = ref(false)

async function fetchDashboardData() {
  loading.value = true
  try {
    const response = await postApi.getList({ page: 1, page_size: 5 })
    recentPosts.value = response.data.items
    stats.value.postCount = response.data.total
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<template>
  <div class="dashboard">
    <div class="mb-6">
      <h1 class="text-2xl font-bold">仪表盘</h1>
      <p class="text-gray-500 text-sm mt-1">欢迎回来，{{ userStore.user?.username || '管理员' }}</p>
    </div>

    <!-- 统计卡片 -->
    <div class="grid gap-4 md:grid-cols-3 mb-8">
      <div class="glass rounded-xl p-6 relative overflow-hidden">
        <div class="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-pink-500/20 to-transparent rounded-bl-full"></div>
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-pink-500/20 flex items-center justify-center">
            <span class="text-2xl">📝</span>
          </div>
          <div>
            <p class="text-gray-500 text-sm">文章总数</p>
            <p class="text-3xl font-bold text-pink-500">{{ stats.postCount }}</p>
          </div>
        </div>
      </div>

      <div class="glass rounded-xl p-6 relative overflow-hidden">
        <div class="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-blue-500/20 to-transparent rounded-bl-full"></div>
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center">
            <span class="text-2xl">👤</span>
          </div>
          <div>
            <p class="text-gray-500 text-sm">用户总数</p>
            <p class="text-3xl font-bold text-blue-500">{{ stats.userCount }}</p>
          </div>
        </div>
      </div>

      <div class="glass rounded-xl p-6 relative overflow-hidden">
        <div class="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-purple-500/20 to-transparent rounded-bl-full"></div>
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center">
            <span class="text-2xl">👁️</span>
          </div>
          <div>
            <p class="text-gray-500 text-sm">总访问量</p>
            <p class="text-3xl font-bold text-purple-500">{{ stats.viewCount.toLocaleString() }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 最近文章 -->
    <div class="glass rounded-xl p-6">
      <h2 class="text-lg font-bold mb-4">最近文章</h2>
      <div v-if="loading" class="text-center text-gray-500 py-4">加载中...</div>
      <div v-else-if="recentPosts.length === 0" class="text-center text-gray-500 py-4">暂无文章</div>
      <div v-else class="space-y-3">
        <div
          v-for="post in recentPosts"
          :key="post.id"
          class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-acg-pink/10 flex items-center justify-center text-acg-pink">
              📄
            </div>
            <div>
              <RouterLink :to="`/post/${post.id}`" class="font-medium hover:text-acg-pink">
                {{ post.title }}
              </RouterLink>
              <p class="text-sm text-gray-500">{{ formatDate(post.created_at) }}</p>
            </div>
          </div>
          <span
            :class="{
              'bg-green-500/20 text-green-500': post.status === 'published',
              'bg-yellow-500/20 text-yellow-500': post.status === 'draft',
            }"
            class="px-2 py-1 text-xs rounded-full"
          >
            {{ post.status === 'published' ? '已发布' : '草稿' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
