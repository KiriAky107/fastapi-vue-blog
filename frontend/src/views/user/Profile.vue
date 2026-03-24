<script setup lang="ts">
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
</script>

<template>
  <div class="profile">
    <nav class="glass fixed top-0 left-0 right-0 z-50">
      <div class="max-w-4xl mx-auto px-4 py-4">
        <RouterLink to="/" class="text-acg-pink hover:underline">← 返回首页</RouterLink>
      </div>
    </nav>

    <main class="pt-20 px-4 max-w-4xl mx-auto">
      <div class="glass rounded-xl p-8">
        <h1 class="text-2xl font-bold mb-4">个人中心</h1>
        <div v-if="userStore.user">
          <p>用户名: {{ userStore.user.username }}</p>
          <p>邮箱: {{ userStore.user.email }}</p>
        </div>
        <div v-else>
          加载中...
        </div>
      </div>
    </main>
  </div>
</template>
