<script setup lang="ts">
import { RouterLink } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <div class="not-found min-h-screen">
    <Navbar />
    <main class="pt-24 px-4 pb-12 flex items-center justify-center">
      <div class="text-center">
        <h1 class="text-6xl font-bold text-acg-pink mb-4">404</h1>
        <p class="text-xl mb-6 text-gray-600 dark:text-gray-400">页面不存在</p>
        <RouterLink to="/" class="btn-acg">返回首页</RouterLink>
      </div>
    </main>
  </div>
</template>
