<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi } from '@/api/post'
import { commentApi } from '@/api/comment'
import type { Post, Comment } from '@/types'
import { useMessage } from 'naive-ui'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import CommentSection from '@/components/Comment.vue'

const message = useMessage()

const route = useRoute()
const router = useRouter()
const postId = route.params.id as string
const post = ref<Post | null>(null)
const loading = ref(true)
const comments = ref<Comment[]>([])
const commentsLoading = ref(true)

async function fetchPost() {
  loading.value = true
  try {
    const response = await postApi.getDetail(postId)
    post.value = response.data
    // 增加浏览量
    postApi.incrementView(postId).catch(() => {})
  } catch (error) {
    message.error('文章不存在或已被删除')
    router.push('/')
  } finally {
    loading.value = false
  }
}

async function fetchComments() {
  commentsLoading.value = true
  try {
    const response = await commentApi.getByPost(postId)
    comments.value = response.data.items
  } catch (error) {
    console.error('Failed to fetch comments:', error)
  } finally {
    commentsLoading.value = false
  }
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

onMounted(() => {
  fetchPost()
  fetchComments()
})
</script>

<template>
  <div class="post-detail min-h-screen">
    <Navbar />

    <main class="pt-24 px-4 pb-12 max-w-4xl mx-auto">
      <div v-if="loading" class="glass rounded-xl p-8 text-center">
        <div class="text-gray-500">加载中...</div>
      </div>

      <article v-else-if="post" class="glass rounded-xl overflow-hidden">
        <!-- 封面图 -->
        <div v-if="post.cover_image" class="w-full h-64 md:h-80 overflow-hidden">
          <img :src="post.cover_image" :alt="post.title" class="w-full h-full object-cover" />
        </div>

        <div class="p-6 md:p-8">
          <!-- 标题 -->
          <h1 class="text-3xl md:text-4xl font-bold mb-4">{{ post.title }}</h1>

          <!-- 元信息 -->
          <div class="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-6 pb-6 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center gap-2">
              <img
                v-if="post.author.avatar"
                :src="post.author.avatar"
                :alt="post.author.username"
                class="w-8 h-8 rounded-full"
              />
              <span class="text-acg-pink">{{ post.author.username }}</span>
            </div>
            <span>发布于 {{ formatDate(post.created_at) }}</span>
            <span v-if="post.category">{{ post.category.name }}</span>
            <span>阅读 {{ post.view_count }}</span>
            <span>点赞 {{ post.like_count || 0 }}</span>
          </div>

          <!-- 标签 -->
          <div v-if="post.tags?.length" class="flex flex-wrap gap-2 mb-6">
            <span
              v-for="tag in post.tags"
              :key="tag.id"
              class="px-3 py-1 text-sm rounded-full bg-acg-pink/20 text-acg-pink"
            >
              {{ tag.name }}
            </span>
          </div>

          <!-- 文章内容 -->
          <div class="prose prose-lg max-w-none dark:prose-invert" v-html="post.content"></div>
        </div>
      </article>

      <!-- 评论区域 -->
      <CommentSection
        v-if="post"
        :postId="postId"
        :comments="comments"
        :loading="commentsLoading"
        @refresh="fetchComments"
      />
    </main>

    <Footer />
  </div>
</template>
