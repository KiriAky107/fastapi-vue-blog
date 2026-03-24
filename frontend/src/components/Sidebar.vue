<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const categories = ref([
  { id: '1', name: '动漫资讯', slug: 'anime', post_count: 12 },
  { id: '2', name: '游戏攻略', slug: 'game', post_count: 8 },
  { id: '3', name: '二次元美图', slug: 'pictures', post_count: 25 },
  { id: '4', name: '同人创作', slug: 'fanwork', post_count: 15 },
])

const tags = ref([
  '原神', '崩坏星穹铁道', '我的世界', 'EVA',
  '约定的梦幻岛', '咒术回战', 'Cosplay', '手办'
])

const hotPosts = ref([
  { id: '1', title: '《原神》4.2版本前瞻：芙宁娜技能演示', view_count: 5200 },
  { id: '2', title: '2024年必追的10部春季新番', view_count: 3800 },
  { id: '3', title: '《崩坏星穹铁道》角色强度榜更新', view_count: 2900 },
  { id: '4', title: '二次元手游开服大横评', view_count: 2100 },
  { id: '5', title: '手办入坑指南：从萌新到进阶', view_count: 1800 },
])
</script>

<template>
  <aside class="sidebar">
    <!-- 关于卡片 -->
    <div class="sidebar-card">
      <div class="about-header">
        <div class="about-avatar">🎌</div>
        <h3 class="about-title">ACG Blog</h3>
      </div>
      <p class="about-desc">专注于二次元文化的博客平台，分享动漫、游戏、同人创作等内容。</p>
      <div class="about-stats">
        <div class="about-stat">
          <span class="stat-value pink">66</span>
          <span class="stat-name">文章</span>
        </div>
        <div class="about-stat">
          <span class="stat-value blue">8</span>
          <span class="stat-name">分类</span>
        </div>
        <div class="about-stat">
          <span class="stat-value purple">42</span>
          <span class="stat-name">标签</span>
        </div>
      </div>
    </div>

    <!-- 分类列表 -->
    <div class="sidebar-card">
      <h3 class="sidebar-title">分类</h3>
      <ul class="category-list">
        <li v-for="cat in categories" :key="cat.id">
          <RouterLink :to="`/category/${cat.slug}`" class="category-item">
            <span>{{ cat.name }}</span>
            <span class="category-count">{{ cat.post_count }}</span>
          </RouterLink>
        </li>
      </ul>
    </div>

    <!-- 标签云 -->
    <div class="sidebar-card">
      <h3 class="sidebar-title">标签</h3>
      <div class="tag-cloud">
        <RouterLink v-for="tag in tags" :key="tag" :to="`/tag/${tag}`" class="tag">
          {{ tag }}
        </RouterLink>
      </div>
    </div>

    <!-- 热门文章 -->
    <div class="sidebar-card">
      <h3 class="sidebar-title">热门文章</h3>
      <ul class="hot-list">
        <li v-for="(post, index) in hotPosts" :key="post.id">
          <RouterLink :to="`/post/${post.id}`" class="hot-item">
            <span class="hot-rank" :class="`rank-${index + 1}`">{{ index + 1 }}</span>
            <div class="hot-content">
              <div class="hot-title">{{ post.title }}</div>
              <div class="hot-views">{{ post.view_count }} 阅读</div>
            </div>
          </RouterLink>
        </li>
      </ul>
    </div>

    <!-- 备案信息 -->
    <div class="copyright">
      <p>© 2024 ACG Blog. All rights reserved.</p>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 100%;
}

@media (min-width: 1024px) {
  .sidebar {
    width: 320px;
    flex-shrink: 0;
  }
}

.sidebar-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}
:global(.dark) .sidebar-card {
  background: rgba(17, 24, 39, 0.8);
}

.about-header {
  text-align: center;
  margin-bottom: 1rem;
}

.about-avatar {
  width: 5rem;
  height: 5rem;
  margin: 0 auto 0.75rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

.about-title {
  font-size: 1.125rem;
  font-weight: bold;
}

.about-desc {
  font-size: 0.875rem;
  color: #6B7280;
  text-align: center;
  margin-bottom: 1rem;
  line-height: 1.6;
}
:global(.dark) .about-desc {
  color: #9CA3AF;
}

.about-stats {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

.about-stat {
  text-align: center;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: bold;
  display: block;
}
.stat-value.pink { color: #FFB7C5; }
.stat-value.blue { color: #A8D8EA; }
.stat-value.purple { color: #D4B5E6; }

.stat-name {
  font-size: 0.75rem;
  color: #6B7280;
}
:global(.dark) .stat-name {
  color: #9CA3AF;
}

.sidebar-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #FFB7C5;
  color: #FFB7C5;
}

.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  color: #6B7280;
  text-decoration: none;
  transition: all 0.2s;
}
:global(.dark) .category-item {
  color: #9CA3AF;
}
.category-item:hover {
  background: rgba(255, 183, 197, 0.2);
  color: #FFB7C5;
  transform: translateX(4px);
}

.category-count {
  font-size: 0.75rem;
  background: #F3F4F6;
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
}
:global(.dark) .category-count {
  background: #374151;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  background: rgba(255, 183, 197, 0.3);
  color: #6B7280;
  text-decoration: none;
  transition: all 0.2s;
}
:global(.dark) .tag {
  background: rgba(212, 181, 230, 0.2);
  color: #9CA3AF;
}
.tag:hover {
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  color: white;
  transform: scale(1.05);
}

.hot-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.hot-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.5rem 0;
  text-decoration: none;
  transition: transform 0.2s;
}
.hot-item:hover {
  transform: translateX(4px);
}

.hot-rank {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  flex-shrink: 0;
  background: #F3F4F6;
  color: #6B7280;
}
:global(.dark) .hot-rank {
  background: #374151;
  color: #9CA3AF;
}
.rank-1 { background: linear-gradient(135deg, #FFD700, #FFA500); color: white; }
.rank-2 { background: linear-gradient(135deg, #C0C0C0, #A8A8A8); color: white; }
.rank-3 { background: linear-gradient(135deg, #CD7F32, #B87333); color: white; }

.hot-content {
  flex: 1;
  min-width: 0;
}

.hot-title {
  font-size: 0.875rem;
  color: #374151;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s;
}
:global(.dark) .hot-title {
  color: #D1D5DB;
}
.hot-item:hover .hot-title {
  color: #FFB7C5;
}

.hot-views {
  font-size: 0.75rem;
  color: #9CA3AF;
  margin-top: 0.25rem;
}

.copyright {
  text-align: center;
  font-size: 0.75rem;
  color: #9CA3AF;
  padding: 1rem 0;
}
</style>
