<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const categoryId = route.params.id as string
</script>

<template>
  <div class="category">
    <nav class="glass fixed top-0 left-0 right-0 z-50">
      <div class="max-w-6xl mx-auto px-4 py-4">
        <RouterLink to="/" class="text-acg-pink hover:underline">← 返回首页</RouterLink>
      </div>
    </nav>

    <main class="pt-20 px-4 max-w-6xl mx-auto">
      <div class="glass rounded-xl p-8">
        <h1 class="text-2xl font-bold mb-4">分类 - {{ categoryId }}</h1>
        <div class="text-gray-600 dark:text-gray-400">
          分类内容加载中...
        </div>
      </div>
    </main>
  </div>
</template>
