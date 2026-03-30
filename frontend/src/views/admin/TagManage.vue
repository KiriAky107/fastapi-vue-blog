<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import type { Tag } from '@/types'

const message = useMessage()
const dialog = useDialog()

const tags = ref<Tag[]>([])
const loading = ref(false)
const showModal = ref(false)
const isEditing = ref(false)
const currentId = ref<string | null>(null)

const formData = ref({
  name: '',
  slug: '',
})

async function fetchTags() {
  loading.value = true
  try {
    // 模拟数据 - 实际应该调用API
    tags.value = []
  } catch (error) {
    message.error('获取标签失败')
  } finally {
    loading.value = false
  }
}

function openModal(tag?: Tag) {
  if (tag) {
    isEditing.value = true
    currentId.value = tag.id
    formData.value = {
      name: tag.name,
      slug: tag.slug || '',
    }
  } else {
    isEditing.value = false
    currentId.value = null
    formData.value = { name: '', slug: '' }
  }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  isEditing.value = false
  currentId.value = null
  formData.value = { name: '', slug: '' }
}

async function saveTag() {
  if (!formData.value.name || !formData.value.slug) {
    message.warning('请填写名称和别名')
    return
  }

  try {
    if (isEditing.value && currentId.value) {
      message.success('标签更新成功')
    } else {
      message.success('标签创建成功')
    }
    closeModal()
    fetchTags()
  } catch (error) {
    message.error('保存失败')
  }
}

async function deleteTag(_id: string) {
  try {
    await dialog.warning({
      title: '确认删除',
      content: '确定要删除这个标签吗？',
      positiveText: '删除',
      negativeText: '取消',
    })
    message.success('删除成功')
    fetchTags()
  } catch {
    // 取消
  }
}

function generateSlug() {
  formData.value.slug = formData.value.name
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

onMounted(() => {
  fetchTags()
})
</script>

<template>
  <div class="tag-manage">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">标签管理</h1>
      <button @click="openModal()" class="btn-acg">
        新建标签
      </button>
    </div>

    <div class="glass rounded-xl p-6">
      <div v-if="loading" class="text-center text-gray-500 py-4">加载中...</div>
      <div v-else-if="tags.length === 0" class="text-center text-gray-500 py-8">
        <p class="mb-2">暂无标签</p>
        <button @click="openModal()" class="text-acg-pink hover:underline">点击创建第一个标签</button>
      </div>
      <div v-else class="flex flex-wrap gap-3">
        <div
          v-for="tag in tags"
          :key="tag.id"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-acg-pink/10 text-acg-pink"
        >
          <span>{{ tag.name }}</span>
          <button @click="openModal(tag)" class="hover:text-white">✏️</button>
          <button @click="deleteTag(tag.id)" class="hover:text-white">✕</button>
        </div>
      </div>
    </div>

    <!-- 弹窗 -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div class="glass rounded-xl w-full max-w-md">
        <div class="p-6">
          <h2 class="text-xl font-bold mb-6">{{ isEditing ? '编辑标签' : '新建标签' }}</h2>

          <form @submit.prevent="saveTag" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">名称</label>
              <input
                v-model="formData.name"
                type="text"
                placeholder="标签名称"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800"
                @blur="generateSlug"
              />
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">别名</label>
              <input
                v-model="formData.slug"
                type="text"
                placeholder="url-slug"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800"
              />
            </div>

            <div class="flex justify-end gap-4 pt-4">
              <button type="button" @click="closeModal" class="px-6 py-2 rounded-lg border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800">
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
  </div>
</template>
