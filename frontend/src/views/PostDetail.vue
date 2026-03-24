<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()
const postId = route.params.id as string
</script>

<template>
  <div class="post-detail">
    <nav class="glass fixed top-0 left-0 right-0 z-50">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <RouterLink to="/" class="text-acg-pink hover:underline">← 返回首页</RouterLink>
      </div>
    </nav>

    <main class="pt-20 px-4 max-w-4xl mx-auto">
      <div class="glass rounded-xl p-8">
        <h1 class="text-3xl font-bold mb-4">文章详情 - {{ postId }}</h1>
        <div class="text-gray-600 dark:text-gray-400">
          文章内容加载中...
        </div>
      </div>
    </main>
  </div>
</template>
