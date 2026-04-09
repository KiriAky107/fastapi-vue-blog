<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMessage } from 'naive-ui'
import { commentApi, type CommentCreateRequest } from '@/api/comment'
import type { Comment } from '@/types'
import { useUserStore } from '@/store/user'

const props = defineProps<{
  postId: string
  comments: Comment[]
  loading: boolean
}>()

const emit = defineEmits<{
  (e: 'refresh'): void
}>()

const message = useMessage()
const userStore = useUserStore()

const newComment = ref('')
const submitting = ref(false)
const replyingTo = ref<string | null>(null)
const replyContent = ref('')

// 扁平化评论（包含回复）
const flatComments = computed(() => {
  const result: (Comment & { isReply?: boolean; parentId?: string })[] = []

  for (const comment of props.comments) {
    result.push(comment)
    if (comment.replies?.length) {
      for (const reply of comment.replies) {
        result.push({ ...reply, isReply: true, parentId: comment.id })
      }
    }
  }

  return result
})

function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)} 分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)} 小时前`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)} 天前`

  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

async function submitComment() {
  if (!newComment.value.trim()) {
    message.warning('请输入评论内容')
    return
  }

  if (!userStore.isLoggedIn) {
    message.warning('请先登录')
    return
  }

  submitting.value = true
  try {
    const data: CommentCreateRequest = {
      post_id: props.postId,
      content: newComment.value.trim(),
    }
    await commentApi.create(data)
    message.success('评论成功')
    newComment.value = ''
    emit('refresh')
  } catch (error: any) {
    message.error(error?.message || '评论失败')
  } finally {
    submitting.value = false
  }
}

async function submitReply(parentId: string) {
  if (!replyContent.value.trim()) {
    message.warning('请输入回复内容')
    return
  }

  if (!userStore.isLoggedIn) {
    message.warning('请先登录')
    return
  }

  submitting.value = true
  try {
    const data: CommentCreateRequest = {
      post_id: props.postId,
      content: replyContent.value.trim(),
      parent_id: parentId,
    }
    await commentApi.create(data)
    message.success('回复成功')
    replyContent.value = ''
    replyingTo.value = null
    emit('refresh')
  } catch (error: any) {
    message.error(error?.message || '回复失败')
  } finally {
    submitting.value = false
  }
}

async function deleteComment(commentId: string) {
  if (!confirm('确定要删除这条评论吗？')) return

  try {
    await commentApi.delete(commentId)
    message.success('删除成功')
    emit('refresh')
  } catch (error: any) {
    message.error(error?.message || '删除失败')
  }
}
</script>

<template>
  <div class="comment-section mt-8">
    <h3 class="text-xl font-bold mb-6">评论</h3>

    <!-- 评论输入框 -->
    <div v-if="userStore.isLoggedIn" class="mb-8">
      <textarea
        v-model="newComment"
        placeholder="写下你的评论..."
        rows="3"
        class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 resize-none focus:outline-none focus:ring-2 focus:ring-acg-pink"
      ></textarea>
      <div class="flex justify-end mt-3">
        <button
          @click="submitComment"
          :disabled="submitting"
          class="btn-acg"
        >
          {{ submitting ? '提交中...' : '发表评论' }}
        </button>
      </div>
    </div>
    <div v-else class="mb-8 text-center py-6 glass rounded-lg">
      <p class="text-gray-500">
        <RouterLink to="/login" class="text-acg-pink hover:underline">登录</RouterLink>
        后即可发表评论
      </p>
    </div>

    <!-- 评论列表 -->
    <div v-if="loading" class="text-center py-8 text-gray-500">加载中...</div>
    <div v-else-if="flatComments.length === 0" class="text-center py-8 text-gray-500">
      暂无评论，来发表第一篇评论吧
    </div>
    <div v-else class="space-y-4">
      <div
        v-for="comment in flatComments"
        :key="comment.id"
        :class="['glass rounded-lg p-4', comment.isReply ? 'ml-8 border-l-2 border-acg-pink/30' : '']"
      >
        <div class="flex items-start gap-3">
          <img
            v-if="comment.author?.avatar"
            :src="comment.author.avatar"
            :alt="comment.author.username"
            class="w-8 h-8 rounded-full"
          />
          <div v-else class="w-8 h-8 rounded-full bg-acg-pink/20 flex items-center justify-center">
            <span class="text-acg-pink text-sm">{{ comment.author?.username?.[0] || 'U' }}</span>
          </div>

          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="font-medium text-acg-pink">{{ comment.author?.username || '匿名用户' }}</span>
              <span class="text-xs text-gray-400">{{ formatDate(comment.created_at) }}</span>
            </div>

            <p class="mt-2 text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{{ comment.content }}</p>

            <div class="flex items-center gap-4 mt-2">
              <button
                v-if="!comment.isReply && userStore.isLoggedIn"
                @click="replyingTo = replyingTo === comment.id ? null : comment.id"
                class="text-sm text-gray-500 hover:text-acg-pink"
              >
                回复
              </button>
              <button
                v-if="userStore.user?.id === comment.author?.id || userStore.isAdmin"
                @click="deleteComment(comment.id)"
                class="text-sm text-gray-500 hover:text-red-500"
              >
                删除
              </button>
            </div>

            <!-- 回复输入框 -->
            <div v-if="replyingTo === comment.id" class="mt-3">
              <textarea
                v-model="replyContent"
                :placeholder="`回复 @${comment.author?.username}...`"
                rows="2"
                class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-acg-pink"
              ></textarea>
              <div class="flex justify-end gap-2 mt-2">
                <button
                  @click="replyingTo = null"
                  class="px-3 py-1 text-sm rounded-lg border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  取消
                </button>
                <button
                  @click="submitReply(comment.id)"
                  :disabled="submitting"
                  class="px-3 py-1 text-sm btn-acg rounded-lg"
                >
                  {{ submitting ? '提交中...' : '回复' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
