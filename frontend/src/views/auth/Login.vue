<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useMessage } from 'naive-ui'

const router = useRouter()
const userStore = useUserStore()
const message = useMessage()
const email = ref('')
const password = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!email.value || !password.value) {
    message.warning('请填写邮箱和密码')
    return
  }

  loading.value = true
  try {
    await userStore.login(email.value, password.value)
    message.success('登录成功')
    router.push('/')
  } catch (error: any) {
    message.error(error?.message || '登录失败，请检查邮箱和密码')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login min-h-screen flex items-center justify-center px-4">
    <div class="glass rounded-xl p-8 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">登录</h1>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">邮箱</label>
          <input
            v-model="email"
            type="email"
            placeholder="请输入邮箱"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-acg-pink"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium mb-2">密码</label>
          <input
            v-model="password"
            type="password"
            placeholder="请输入密码"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-acg-pink"
            required
          />
        </div>

        <button type="submit" class="w-full btn-acg" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <p class="text-center mt-4 text-sm">
        还没有账号？
        <RouterLink to="/register" class="text-acg-pink hover:underline">立即注册</RouterLink>
      </p>
    </div>
  </div>
</template>
