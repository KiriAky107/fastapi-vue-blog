<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Hero from '@/components/Hero.vue'
import PostCard from '@/components/PostCard.vue'
import Sidebar from '@/components/Sidebar.vue'
import Footer from '@/components/Footer.vue'
import { postApi } from '@/api/post'
import { categoryApi } from '@/api/category'
import type { Post, Category } from '@/types'

const posts = ref<Post[]>([])
const categories = ref<Category[]>([{ id: '', name: '全部', slug: '', created_at: '' }])
const selectedCategory = ref('')
const loading = ref(false)

async function fetchPosts(categoryId?: string) {
  loading.value = true
  try {
    const params: any = { page: 1, page_size: 20 }
    if (categoryId) {
      params.category_id = categoryId
    }
    const response = await postApi.getList(params)
    posts.value = response.data.items.filter(p => p.status === 'published')
  } catch (error) {
    console.error('Failed to fetch posts:', error)
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    const response = await categoryApi.getAll()
    categories.value = [{ id: '', name: '全部', slug: '', created_at: '' }, ...response.data]
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  }
}

function handleCategoryChange(slug: string) {
  selectedCategory.value = slug
  const catId = slug ? categories.value.find(c => c.slug === slug)?.id : ''
  fetchPosts(catId)
}

onMounted(() => {
  fetchCategories()
  fetchPosts()
})
</script>

<template>
  <div class="home">
    <Navbar />
    <Hero />

    <main class="main-container">
      <!-- 分类筛选 -->
      <section class="category-section">
        <div class="category-buttons">
          <button
            v-for="cat in categories"
            :key="cat.id"
            @click="handleCategoryChange(cat.slug)"
            class="category-btn"
            :class="{ active: selectedCategory === cat.slug }"
          >
            {{ cat.name }}
          </button>
        </div>
      </section>

      <!-- 文章列表 + 侧边栏 -->
      <div class="content-layout">
        <!-- 文章列表 -->
        <section class="posts-section">
          <h2 class="section-title">最新文章</h2>
          <div v-if="loading" class="text-center py-8 text-gray-500">加载中...</div>
          <div v-else-if="posts.length === 0" class="text-center py-8 text-gray-500">暂无文章</div>
          <div v-else class="posts-grid">
            <PostCard v-for="post in posts" :key="post.id" :post="post" />
          </div>
        </section>

        <!-- 侧边栏 -->
        <Sidebar />
      </div>
    </main>

    <Footer />
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
}

.main-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 3rem 1rem;
}

.category-section {
  margin-bottom: 2rem;
}

.category-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.75rem;
}

.category-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6B7280;
  background: #F3F4F6;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}
:global(.dark) .category-btn {
  background: #374151;
  color: #9CA3AF;
}
.category-btn:hover {
  background: rgba(255, 183, 197, 0.3);
  color: #FFB7C5;
}
.category-btn.active {
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  color: white;
}

.content-layout {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
@media (min-width: 1024px) {
  .content-layout {
    flex-direction: row;
    align-items: flex-start;
  }
}

.posts-section {
  flex: 1;
  min-width: 0;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.posts-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}
@media (min-width: 640px) {
  .posts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1024px) {
  .posts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
