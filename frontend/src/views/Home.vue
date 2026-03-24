<script setup lang="ts">
import { ref } from 'vue'
import Navbar from '@/components/Navbar.vue'
import Hero from '@/components/Hero.vue'
import PostCard from '@/components/PostCard.vue'
import Sidebar from '@/components/Sidebar.vue'
import Footer from '@/components/Footer.vue'
import type { Post } from '@/types'

// 模拟文章数据 - 后端完成后替换为真实API调用
const posts = ref<Post[]>([
  {
    id: '1',
    title: '《原神》4.2版本前瞻：芙宁娜技能演示与剧情预测',
    slug: 'genshin-4-2-preview',
    content: '',
    summary: '4.2版本即将到来，让我们提前了解水神芙宁娜的技能机制以及可能的剧情发展...',
    cover_image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=800',
    author: { id: '1', username: 'Miyako', email: '', is_active: true, created_at: '', updated_at: '' },
    category: { id: '1', name: '游戏攻略', slug: 'game', created_at: '' },
    tags: [{ id: '1', name: '原神', created_at: '' }, { id: '2', name: '攻略', created_at: '' }],
    view_count: 5200,
    status: 'published',
    created_at: '2024-03-15T10:00:00Z',
    updated_at: '2024-03-15T10:00:00Z'
  },
  {
    id: '2',
    title: '2024年必追的10部春季新番推荐',
    slug: 'spring-2024-anime',
    content: '',
    summary: '春天到了，又到了补番的季节！本期为大家带来2024年春季最值得期待的新番动画...',
    cover_image: 'https://images.unsplash.com/photo-1535016120720-40c6874c3b1c?w=800',
    author: { id: '2', username: 'Akari', email: '', is_active: true, created_at: '', updated_at: '' },
    category: { id: '2', name: '动漫资讯', slug: 'anime', created_at: '' },
    tags: [{ id: '3', name: '新番', created_at: '' }, { id: '4', name: '推荐', created_at: '' }],
    view_count: 3800,
    status: 'published',
    created_at: '2024-03-14T08:00:00Z',
    updated_at: '2024-03-14T08:00:00Z'
  },
  {
    id: '3',
    title: '《崩坏星穹铁道》角色强度榜 - 3月版',
    slug: 'honkai-star-rail-tier-list',
    content: '',
    summary: '版本强势角色有哪些？本期强度榜为你详细分析当前版本的T0、T1角色...',
    cover_image: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800',
    author: { id: '1', username: 'Miyako', email: '', is_active: true, created_at: '', updated_at: '' },
    category: { id: '1', name: '游戏攻略', slug: 'game', created_at: '' },
    tags: [{ id: '2', name: '崩坏星穹铁道', created_at: '' }, { id: '5', name: '强度榜', created_at: '' }],
    view_count: 2900,
    status: 'published',
    created_at: '2024-03-13T15:30:00Z',
    updated_at: '2024-03-13T15:30:00Z'
  },
  {
    id: '4',
    title: '手办入坑指南：从萌新到进阶的全方位攻略',
    slug: 'figure-beginner-guide',
    content: '',
    summary: '想入手第一只手办但不知道如何选择？这篇指南将带你了解手办的各种分类、选购渠道...',
    cover_image: 'https://images.unsplash.com/photo-1608889175123-8ee362201f81?w=800',
    author: { id: '3', username: 'Sakura', email: '', is_active: true, created_at: '', updated_at: '' },
    category: { id: '3', name: '二次元美图', slug: 'pictures', created_at: '' },
    tags: [{ id: '6', name: '手办', created_at: '' }, { id: '7', name: '教程', created_at: '' }],
    view_count: 2100,
    status: 'published',
    created_at: '2024-03-12T12:00:00Z',
    updated_at: '2024-03-12T12:00:00Z'
  },
  {
    id: '5',
    title: '同人创作分享：用画笔描绘心中的二次元世界',
    slug: 'fanart-sharing',
    content: '',
    summary: '本期收录了多位优秀画师的作品，让我们一起欣赏这些充满想象力的同人创作...',
    cover_image: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800',
    author: { id: '2', username: 'Akari', email: '', is_active: true, created_at: '', updated_at: '' },
    category: { id: '4', name: '同人创作', slug: 'fanwork', created_at: '' },
    tags: [{ id: '8', name: '同人', created_at: '' }, { id: '9', name: '绘画', created_at: '' }],
    view_count: 1800,
    status: 'published',
    created_at: '2024-03-11T09:00:00Z',
    updated_at: '2024-03-11T09:00:00Z'
  },
  {
    id: '6',
    title: '《约定的梦幻岛》最新话解析：剧情走向深度分析',
    slug: 'neverland-analysis',
    content: '',
    summary: '最新一话的剧情信息量巨大，让我们来深度分析一下剧情走向和角色心理...',
    cover_image: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800',
    author: { id: '4', username: 'Ken', email: '', is_active: true, created_at: '', updated_at: '' },
    category: { id: '2', name: '动漫资讯', slug: 'anime', created_at: '' },
    tags: [{ id: '10', name: '约定的梦幻岛', created_at: '' }, { id: '11', name: '分析', created_at: '' }],
    view_count: 1500,
    status: 'published',
    created_at: '2024-03-10T20:00:00Z',
    updated_at: '2024-03-10T20:00:00Z'
  }
])

const categories = [
  { name: '全部', slug: '' },
  { name: '动漫资讯', slug: 'anime' },
  { name: '游戏攻略', slug: 'game' },
  { name: '二次元美图', slug: 'pictures' },
  { name: '同人创作', slug: 'fanwork' },
]

const selectedCategory = ref('')
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
            :key="cat.slug"
            @click="selectedCategory = cat.slug"
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
          <div class="posts-grid">
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
