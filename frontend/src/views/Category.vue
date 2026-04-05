<script setup lang="ts">
import { useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { postApi } from '@/api/post'
import { categoryApi } from '@/api/category'
import type { Post, Category } from '@/types'
import { ref, onMounted, computed } from 'vue'
import PostCard from '@/components/PostCard.vue'

const route = useRoute()
const categoryId = computed(() => route.params.id as string | undefined)
const category = ref<Category | null>(null)
const posts = ref<Post[]>([])
const loading = ref(false)

async function fetchCategoryAndPosts() {
  loading.value = true
  try {
    const id = categoryId.value

    if (!id) {
      // 全部分类页
      category.value = null
      const response = await postApi.getList({ page: 1, page_size: 20 })
      posts.value = response.data.items.filter((p: Post) => p.status === 'published')
    } else {
      // 特定分类
      const [catResponse, postsResponse] = await Promise.all([
        categoryApi.getDetail(id),
        postApi.getList({ category_id: id, page: 1, page_size: 20 }),
      ])
      category.value = catResponse.data
      posts.value = postsResponse.data.items.filter((p: Post) => p.status === 'published')
    }
  } catch (error) {
    console.error('Failed to fetch category:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategoryAndPosts()
})
</script>

<template>
  <div class="category min-h-screen">
    <Navbar />

    <!-- Hero Section -->
    <section class="relative py-16 px-4 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-pink-500/10 via-purple-500/10 to-blue-500/10"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-acg-pink/20 rounded-full blur-3xl"></div>
      <div class="relative max-w-6xl mx-auto text-center">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm mb-6">
          <span class="text-lg">📁</span>
          <span class="text-sm font-medium">分类</span>
        </div>
        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          {{ category?.name || '全部分类' }}
        </h1>
        <p v-if="category?.description" class="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          {{ category.description }}
        </p>
        <p v-else class="text-gray-500">
          浏览所有文章
        </p>
      </div>
    </section>

    <!-- Content -->
    <main class="px-4 pb-12 max-w-6xl mx-auto">
      <div v-if="loading" class="glass rounded-xl p-12 text-center">
        <div class="animate-pulse space-y-4">
          <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mx-auto"></div>
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mx-auto"></div>
        </div>
      </div>

      <div v-else-if="posts.length === 0" class="glass rounded-xl p-12 text-center">
        <div class="text-6xl mb-4">📭</div>
        <h3 class="text-xl font-bold mb-2">暂无文章</h3>
        <p class="text-gray-500">该分类下还没有发布的文章</p>
        <RouterLink to="/" class="inline-block mt-4 text-acg-pink hover:underline">
          返回首页
        </RouterLink>
      </div>

      <div v-else>
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-medium">
            共 {{ posts.length }} 篇文章
          </h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <PostCard v-for="post in posts" :key="post.id" :post="post" />
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>
