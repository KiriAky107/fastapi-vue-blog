<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { Post } from '@/types'

interface Props {
  post: Post
}

defineProps<Props>()
</script>

<template>
  <article class="post-card">
    <RouterLink :to="`/post/${post.id}`" class="post-link">
      <!-- 封面图 -->
      <div class="post-cover">
        <img v-if="post.cover_image" :src="post.cover_image" :alt="post.title" class="cover-img" />
        <div v-else class="cover-placeholder">
          <span>📖</span>
        </div>
        <span class="status-badge" :class="post.status">{{ post.status === 'published' ? '已发布' : post.status === 'draft' ? '草稿' : '归档' }}</span>
      </div>

      <!-- 内容区 -->
      <div class="post-content">
        <!-- 分类 -->
        <div class="post-tags" v-if="post.category || (post.tags && post.tags.length)">
          <RouterLink v-if="post.category" :to="`/category/${post.category.id}`" class="category-tag">
            {{ post.category.name }}
          </RouterLink>
          <RouterLink v-for="tag in (post.tags || []).slice(0, 2)" :key="tag.id" :to="`/tag/${tag.id}`" class="tag">
            #{{ tag.name }}
          </RouterLink>
        </div>

        <!-- 标题 -->
        <h3 class="post-title">{{ post.title }}</h3>

        <!-- 摘要 -->
        <p v-if="post.summary" class="post-summary">{{ post.summary }}</p>

        <!-- 底部信息 -->
        <div class="post-meta">
          <div class="author">
            <div class="author-avatar">{{ post.author.username?.[0]?.toUpperCase() || 'U' }}</div>
            <span class="author-name">{{ post.author.username }}</span>
          </div>
          <div class="meta-right">
            <span class="views">👁 {{ post.view_count }}</span>
            <span class="date">{{ new Date(post.created_at).toLocaleDateString('zh-CN') }}</span>
          </div>
        </div>
      </div>
    </RouterLink>
  </article>
</template>

<style scoped>
.post-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border-radius: 1rem;
  overflow: hidden;
  transition: all 0.3s;
}
:global(.dark) .post-card {
  background: rgba(17, 24, 39, 0.8);
}
.post-card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.post-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.post-cover {
  position: relative;
  height: 12rem;
  overflow: hidden;
}

.cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}
.post-card:hover .cover-img {
  transform: scale(1.1);
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #FFE4E9, #A8D8EA);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
}

.status-badge {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.9);
  color: #6B7280;
}
:global(.dark) .status-badge {
  background: rgba(17, 24, 39, 0.9);
  color: #9CA3AF;
}
.status-badge.published {
  background: rgba(220, 252, 231, 0.95);
  color: #22C55E;
}
.status-badge.draft {
  background: rgba(254, 215, 170, 0.95);
  color: #F97316;
}

.post-content {
  padding: 1.25rem;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.category-tag {
  padding: 0.125rem 0.625rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  background: linear-gradient(135deg, #FFB7C5, #A8D8EA);
  color: white;
  text-decoration: none;
  transition: transform 0.2s;
}
.category-tag:hover {
  transform: scale(1.05);
}

.tag {
  padding: 0.125rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  background: #F3F4F6;
  color: #6B7280;
  text-decoration: none;
  transition: all 0.2s;
}
:global(.dark) .tag {
  background: #374151;
  color: #9CA3AF;
}
.tag:hover {
  background: #FFB7C5;
  color: white;
}

.post-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1F2937;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s;
}
:global(.dark) .post-title {
  color: #F3F4F6;
}
.post-card:hover .post-title {
  color: #FFB7C5;
}

.post-summary {
  font-size: 0.875rem;
  color: #6B7280;
  line-height: 1.6;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
:global(.dark) .post-summary {
  color: #9CA3AF;
}

.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.author-avatar {
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 9999px;
  background: linear-gradient(135deg, #FFB7C5, #D4B5E6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
}

.author-name {
  font-size: 0.875rem;
  color: #6B7280;
}
:global(.dark) .author-name {
  color: #9CA3AF;
}

.meta-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.75rem;
  color: #9CA3AF;
}

.views {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
</style>
