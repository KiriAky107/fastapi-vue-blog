<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<template>
  <div class="about min-h-screen">
    <Navbar />

    <main class="pt-24 px-4 pb-12 max-w-4xl mx-auto">
      <div class="glass rounded-xl p-8">
        <h1 class="text-3xl font-bold mb-6">关于 ACG Blog</h1>
        <div class="space-y-4 text-gray-600 dark:text-gray-400 leading-relaxed">
          <p>
            ACG Blog 是一个专注于二次元文化的博客平台，使用 Vue 3 + TypeScript + Naive UI 构建。
            在这里，你可以分享你的二次元生活、动漫评论、游戏攻略等内容。
          </p>
          <p>
            本博客系统采用前后端分离架构，前端使用 Vue 3 + Vite，后端使用 FastAPI，
            数据存储使用 PostgreSQL，缓存使用 Redis，为你提供流畅的使用体验。
          </p>
          <p>
            如果你有任何问题或建议，欢迎联系我们！
          </p>
        </div>

        <div class="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-bold mb-4">技术栈</h2>
          <div class="flex flex-wrap gap-2">
            <span class="px-3 py-1 rounded-full bg-acg-pink/20 text-acg-pink text-sm">Vue 3</span>
            <span class="px-3 py-1 rounded-full bg-acg-purple/20 text-acg-purple text-sm">FastAPI</span>
            <span class="px-3 py-1 rounded-full bg-acg-pink/20 text-acg-pink text-sm">TypeScript</span>
            <span class="px-3 py-1 rounded-full bg-acg-purple/20 text-acg-purple text-sm">Naive UI</span>
            <span class="px-3 py-1 rounded-full bg-acg-pink/20 text-acg-pink text-sm">Tailwind CSS</span>
            <span class="px-3 py-1 rounded-full bg-acg-purple/20 text-acg-purple text-sm">PostgreSQL</span>
          </div>
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>
