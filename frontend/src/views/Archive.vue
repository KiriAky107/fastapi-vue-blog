<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { postApi } from '@/api/post'
import type { Post } from '@/types'

const posts = ref<Post[]>([])
const loading = ref(false)

// 按年月分组文章
const groupedPosts = computed(() => {
  const groups: Record<string, Post[]> = {}

  posts.value.forEach(post => {
    if (post.status !== 'published') return

    const date = new Date(post.created_at)
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const key = `${year}-${month.toString().padStart(2, '0')}`

    if (!groups[key]) {
      groups[key] = []
    }
    groups[key].push(post)
  })

  return groups
})

// 获取排序后的年份列表
const sortedYears = computed(() => {
  return Object.keys(groupedPosts.value).sort((a, b) => b.localeCompare(a))
})

async function fetchPosts() {
  loading.value = true
  try {
    const response = await postApi.getList({ page: 1, page_size: 1000 })
    posts.value = response.data.items
  } catch (error) {
    console.error('Failed to fetch posts:', error)
  } finally {
    loading.value = false
  }
}

function formatMonth(monthStr: string): string {
  const [year, month] = monthStr.split('-')
  const date = new Date(parseInt(year), parseInt(month) - 1)
  return `${year}年${date.toLocaleDateString('zh-CN', { month: 'long' })}`
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <div class="archive min-h-screen">
    <Navbar />

    <!-- Hero Section -->
    <section class="relative py-16 px-4 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-pink-500/10 via-purple-500/10 to-blue-500/10"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-acg-pink/20 rounded-full blur-3xl"></div>
      <div class="relative max-w-4xl mx-auto text-center">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm mb-6">
          <span class="text-lg">📁</span>
          <span class="text-sm font-medium">归档</span>
        </div>
        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          文章归档
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          共 {{ posts.filter(p => p.status === 'published').length }} 篇文章
        </p>
      </div>
    </section>

    <!-- Archive List -->
    <main class="px-4 pb-12 max-w-4xl mx-auto">
      <div v-if="loading" class="glass rounded-xl p-12 text-center">
        <div class="animate-pulse space-y-4">
          <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mx-auto"></div>
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mx-auto"></div>
        </div>
      </div>

      <div v-else-if="sortedYears.length === 0" class="glass rounded-xl p-12 text-center">
        <div class="text-6xl mb-4">📭</div>
        <h3 class="text-xl font-bold mb-2">暂无文章</h3>
        <p class="text-gray-500">还没有发布的文章</p>
        <RouterLink to="/" class="inline-block mt-4 text-acg-pink hover:underline">
          返回首页
        </RouterLink>
      </div>

      <div v-else class="space-y-8">
        <div v-for="yearMonth in sortedYears" :key="yearMonth" class="archive-group">
          <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
            <span class="text-acg-pink">{{ formatMonth(yearMonth) }}</span>
            <span class="text-gray-400 text-sm font-normal">
              ({{ groupedPosts[yearMonth].length }} 篇)
            </span>
          </h2>

          <div class="space-y-2">
            <RouterLink
              v-for="post in groupedPosts[yearMonth]"
              :key="post.id"
              :to="`/post/${post.id}`"
              class="glass rounded-lg p-4 flex items-center justify-between hover:shadow-md transition-all group"
            >
              <div class="flex items-center gap-4">
                <span class="text-acg-pink text-sm">
                  {{ new Date(post.created_at).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }) }}
                </span>
                <span class="font-medium group-hover:text-acg-pink transition-colors">
                  {{ post.title }}
                </span>
              </div>
              <span
                v-if="post.category"
                class="text-sm px-2 py-1 rounded-full bg-acg-pink/10 text-acg-pink"
              >
                {{ post.category.name }}
              </span>
            </RouterLink>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<style scoped>
.archive {
  min-height: 100vh;
}
</style>
