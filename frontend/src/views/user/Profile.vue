<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { authApi } from '@/api/auth'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'

const router = useRouter()
const userStore = useUserStore()

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

async function handleLogout() {
  if (!confirm('确定要退出登录吗？')) {
    return
  }
  try {
    await authApi.logout()
  } catch (error) {
    // ignore
  }
  userStore.logout()
  router.push('/')
}

onMounted(() => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
  }
})
</script>

<template>
  <div class="profile min-h-screen">
    <Navbar />

    <!-- Hero Background -->
    <section class="relative py-16 px-4 overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-br from-pink-500/10 via-purple-500/10 to-blue-500/10"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-acg-pink/20 rounded-full blur-3xl"></div>
    </section>

    <!-- Profile Content -->
    <main class="px-4 pb-12 max-w-2xl mx-auto -mt-20 relative z-10">
      <div class="glass rounded-xl p-6 md:p-8">
        <h1 class="text-2xl font-bold mb-6">个人中心</h1>

        <div v-if="userStore.user" class="space-y-6">
          <!-- 头像和基本信息 -->
          <div class="flex items-center gap-6">
            <div class="w-20 h-20 rounded-full overflow-hidden bg-acg-pink/20 flex items-center justify-center">
              <img
                v-if="userStore.user.avatar"
                :src="userStore.user.avatar"
                :alt="userStore.user.username"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-3xl text-acg-pink">{{ userStore.user.username?.[0]?.toUpperCase() || 'U' }}</span>
            </div>
            <div>
              <h2 class="text-xl font-bold">{{ userStore.user.username }}</h2>
              <p class="text-gray-500 text-sm">加入于 {{ formatDate(userStore.user.created_at) }}</p>
            </div>
          </div>

          <!-- 详细信息 -->
          <div class="space-y-4 py-4 border-t border-gray-200 dark:border-gray-700">
            <div class="flex justify-between">
              <span class="text-gray-500">邮箱</span>
              <span>{{ userStore.user.email }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">状态</span>
              <span :class="userStore.user.is_active ? 'text-green-500' : 'text-gray-400'">
                {{ userStore.user.is_active ? '已激活' : '未激活' }}
              </span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex gap-4 pt-4">
            <button
              @click="handleLogout"
              class="px-6 py-2 rounded-lg bg-red-500/20 text-red-500 hover:bg-red-500/30 transition-colors"
            >
              退出登录
            </button>
          </div>
        </div>

        <div v-else class="text-center text-gray-500 py-8">
          加载中...
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>
