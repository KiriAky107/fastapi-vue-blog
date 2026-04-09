<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import { postApi } from '@/api/post'
import type { Post, PostCreateRequest } from '@/types'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import MarkdownEditor from '@/components/MarkdownEditor.vue'

const message = useMessage()
const posts = ref<Post[]>([])
const loading = ref(false)
const showEditor = ref(false)
const isEditing = ref(false)
const currentPostId = ref<string | null>(null)

// 表单数据
const formData = ref<PostCreateRequest>({
  title: '',
  content: '',
  summary: '',
  cover_image: '',
  category_id: '',
  tags: [],
  status: 'draft',
})

const searchParams = ref({
  page: 1,
  page_size: 20,
})

async function fetchPosts() {
  loading.value = true
  try {
    const response = await postApi.getList(searchParams.value)
    posts.value = response.data.items
  } catch (error) {
    message.error('获取文章列表失败')
  } finally {
    loading.value = false
  }
}

function openEditor(post?: Post) {
  if (post) {
    isEditing.value = true
    currentPostId.value = post.id
    formData.value = {
      title: post.title,
      content: post.content,
      summary: post.summary || '',
      cover_image: post.cover_image || '',
      category_id: post.category?.id || '',
      tags: [],
      status: post.status === 'archived' ? 'draft' : post.status,
    }
  } else {
    isEditing.value = false
    currentPostId.value = null
    formData.value = {
      title: '',
      content: '',
      summary: '',
      cover_image: '',
      category_id: '',
      tags: [],
      status: 'draft',
    }
  }
  showEditor.value = true
}

function closeEditor() {
  showEditor.value = false
  isEditing.value = false
  currentPostId.value = null
}

async function savePost() {
  if (!formData.value.title || !formData.value.content) {
    message.warning('请填写标题和内容')
    return
  }

  try {
    if (isEditing.value && currentPostId.value) {
      await postApi.update(currentPostId.value, formData.value)
      message.success('文章更新成功')
    } else {
      await postApi.create(formData.value)
      message.success('文章创建成功')
    }
    closeEditor()
    fetchPosts()
  } catch (error: any) {
    message.error(error?.message || '保存失败')
  }
}

async function deletePost(id: string) {
  try {
    await postApi.delete(id)
    message.success('删除成功')
    fetchPosts()
  } catch (error) {
    message.error('删除失败')
  }
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <div class="post-manage min-h-screen">
    <Navbar />

    <main class="pt-24 px-4 pb-12 max-w-6xl mx-auto">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">文章管理</h1>
        <button @click="openEditor()" class="btn-acg">
          新建文章
        </button>
      </div>

      <div class="glass rounded-xl overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-100 dark:bg-gray-800">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-medium">标题</th>
              <th class="px-4 py-3 text-left text-sm font-medium">分类</th>
              <th class="px-4 py-3 text-left text-sm font-medium">状态</th>
              <th class="px-4 py-3 text-left text-sm font-medium">发布时间</th>
              <th class="px-4 py-3 text-right text-sm font-medium">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="post in posts" :key="post.id" class="hover:bg-gray-50 dark:hover:bg-gray-800">
              <td class="px-4 py-3">
                <RouterLink :to="`/post/${post.id}`" class="text-acg-pink hover:underline">
                  {{ post.title }}
                </RouterLink>
              </td>
              <td class="px-4 py-3 text-sm text-gray-500">{{ post.category?.name || '-' }}</td>
              <td class="px-4 py-3">
                <span
                  :class="{
                    'bg-green-500/20 text-green-500': post.status === 'published',
                    'bg-yellow-500/20 text-yellow-500': post.status === 'draft',
                    'bg-gray-500/20 text-gray-500': post.status === 'archived',
                  }"
                  class="px-2 py-1 text-xs rounded-full"
                >
                  {{ post.status === 'published' ? '已发布' : post.status === 'draft' ? '草稿' : '归档' }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(post.created_at) }}</td>
              <td class="px-4 py-3 text-right">
                <button @click="openEditor(post)" class="text-acg-pink hover:underline mr-4">编辑</button>
                <button @click="deletePost(post.id)" class="text-red-500 hover:underline">删除</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="loading" class="p-8 text-center text-gray-500">加载中...</div>
        <div v-if="!loading && posts.length === 0" class="p-8 text-center text-gray-500">暂无文章</div>
      </div>
    </main>

    <!-- 编辑器弹窗 -->
    <div v-if="showEditor" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div class="glass rounded-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h2 class="text-xl font-bold mb-6">{{ isEditing ? '编辑文章' : '新建文章' }}</h2>

          <form @submit.prevent="savePost" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">标题</label>
              <input
                v-model="formData.title"
                type="text"
                placeholder="文章标题"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">摘要</label>
              <textarea
                v-model="formData.summary"
                placeholder="文章摘要（可选）"
                rows="2"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800"
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">封面图 URL</label>
              <input
                v-model="formData.cover_image"
                type="url"
                placeholder="https://..."
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800"
              />
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">内容 (Markdown)</label>
              <MarkdownEditor
                v-model="formData.content"
                placeholder="使用 Markdown 编写文章内容..."
              />
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">状态</label>
              <select
                v-model="formData.status"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800"
              >
                <option value="draft">草稿</option>
                <option value="published">发布</option>
              </select>
            </div>

            <div class="flex justify-end gap-4 pt-4">
              <button type="button" @click="closeEditor" class="px-6 py-2 rounded-lg border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800">
                取消
              </button>
              <button type="submit" class="btn-acg">
                保存
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>
