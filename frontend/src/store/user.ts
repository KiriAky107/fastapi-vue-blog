import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { authApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_active === true)

  // Actions
  function setToken(newToken: string | null) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('access_token', newToken)
    } else {
      localStorage.removeItem('access_token')
    }
  }

  function setUser(newUser: User | null) {
    user.value = newUser
  }

  async function fetchUser() {
    if (!token.value) return

    try {
      const response = await authApi.getCurrentUser()
      setUser(response.data)
    } catch (error) {
      console.error('Failed to fetch user:', error)
      setToken(null)
      setUser(null)
    }
  }

  async function login(email: string, password: string) {
    const response = await authApi.login({ email, password })
    setToken(response.data.access_token)
    await fetchUser()
  }

  function logout() {
    setToken(null)
    setUser(null)
  }

  return {
    user,
    token,
    isLoggedIn,
    isAdmin,
    setToken,
    setUser,
    fetchUser,
    login,
    logout,
  }
})
