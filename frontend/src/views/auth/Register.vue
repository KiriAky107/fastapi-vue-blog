<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/auth'
import { useMessage } from 'naive-ui'

const router = useRouter()
const message = useMessage()
const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)

async function handleRegister() {
  if (!username.value || !email.value || !password.value) {
    message.warning('请填写所有字段')
    return
  }

  if (password.value.length < 6) {
    message.warning('密码长度至少为6位')
    return
  }

  loading.value = true
  try {
    await authApi.register({
      username: username.value,
      email: email.value,
      password: password.value,
    })
    message.success('注册成功，请登录')
    router.push('/login')
  } catch (error: any) {
    message.error(error.response?.data?.message || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register min-h-screen flex items-center justify-center px-4">
    <div class="glass rounded-xl p-8 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">注册</h1>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">用户名</label>
          <input
            v-model="username"
            type="text"
            placeholder="请输入用户名"
            class="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-acg-pink"
            required
          />
        </div>

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
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <p class="text-center mt-4 text-sm">
        已有账号？
        <RouterLink to="/login" class="text-acg-pink hover:underline">立即登录</RouterLink>
      </p>
    </div>
  </div>
</template>
