<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMessage, useDialog } from 'naive-ui'
import type { Category } from '@/types'

const message = useMessage()
const dialog = useDialog()

const categories = ref<Category[]>([])
const loading = ref(false)
const showModal = ref(false)
const isEditing = ref(false)
const currentId = ref<string | null>(null)

const formData = ref({
  name: '',
  slug: '',
  description: '',
})

async function fetchCategories() {
  loading.value = true
  try {
    // 模拟数据 - 实际应该调用API
    categories.value = []
  } catch (error) {
    message.error('获取分类失败')
  } finally {
    loading.value = false
  }
}

function openModal(category?: Category) {
  if (category) {
    isEditing.value = true
    currentId.value = category.id
    formData.value = {
      name: category.name,
      slug: category.slug,
      description: category.description || '',
    }
  } else {
    isEditing.value = false
    currentId.value = null
    formData.value = { name: '', slug: '', description: '' }
  }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  isEditing.value = false
  currentId.value = null
  formData.value = { name: '', slug: '', description: '' }
}

async function saveCategory() {
  if (!formData.value.name || !formData.value.slug) {
    message.warning('请填写名称和别名')
    return
  }

  try {
    if (isEditing.value && currentId.value) {
      message.success('分类更新成功')
    } else {
      message.success('分类创建成功')
    }
    closeModal()
    fetchCategories()
  } catch (error) {
    message.error('保存失败')
  }
}

async function deleteCategory(_id: string) {
  try {
    await dialog.warning({
      title: '确认删除',
      content: '确定要删除这个分类吗？',
      positiveText: '删除',
      negativeText: '取消',
    })
    message.success('删除成功')
    fetchCategories()
  } catch {
    // 取消
  }
}

function generateSlug() {
  // 简单的 slug 生成
  formData.value.slug = formData.value.name
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}

onMounted(() => {
  fetchCategories()
})
</script>

<template>
  <div class="category-manage">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">分类管理</h1>
      <button @click="openModal()" class="btn-acg">
        新建分类
      </button>
    </div>

    <div class="glass rounded-xl overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-100 dark:bg-gray-800">
          <tr>
            <th class="px-4 py-3 text-left text-sm font-medium">名称</th>
            <th class="px-4 py-3 text-left text-sm font-medium">别名</th>
            <th class="px-4 py-3 text-left text-sm font-medium">描述</th>
            <th class="px-4 py-3 text-left text-sm font-medium">创建时间</th>
            <th class="px-4 py-3 text-right text-sm font-medium">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="cat in categories" :key="cat.id" class="hover:bg-gray-50 dark:hover:bg-gray-800">
            <td class="px-4 py-3 font-medium">{{ cat.name }}</td>
            <td class="px-4 py-3 text-gray-500 text-sm">{{ cat.slug }}</td>
            <td class="px-4 py-3 text-gray-500 text-sm">{{ cat.description || '-' }}</td>
            <td class="px-4 py-3 text-gray-500 text-sm">{{ new Date(cat.created_at).toLocaleDateString() }}</td>
            <td class="px-4 py-3 text-right">
              <button @click="openModal(cat)" class="text-acg-pink hover:underline mr-4">编辑</button>
              <button @click="deleteCategory(cat.id)" class="text-red-500 hover:underline">删除</button>
            </td>
          </tr>
          <tr v-if="loading">
            <td colspan="5" class="px-4 py-8 text-center text-gray-500">加载中...</td>
          </tr>
          <tr v-if="!loading && categories.length === 0">
            <td colspan="5" class="px-4 py-8 text-center text-gray-500">暂无分类，点击上方按钮创建</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 弹窗 -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
      <div class="glass rounded-xl w-full max-w-md">
        <div class="p-6">
          <h2 class="text-xl font-bold mb-6">{{ isEditing ? '编辑分类' : '新建分类' }}</h2>

          <form @submit.prevent="saveCategory" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">名称</label>
              <input
                v-model="formData.name"
                type="text"
                placeholder="分类名称"
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

            <div>
              <label class="block text-sm font-medium mb-2">描述</label>
              <textarea
                v-model="formData.description"
                placeholder="分类描述（可选）"
                rows="3"
                class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800"
              ></textarea>
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
