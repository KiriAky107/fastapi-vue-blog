import { defineStore } from 'pinia'
import { ref } from 'vue'

type Theme = 'light' | 'dark' | 'auto'

export const useThemeStore = defineStore('theme', () => {
  // 状态
  const theme = ref<Theme>((localStorage.getItem('theme') as Theme) || 'light')

  // Actions
  function setTheme(newTheme: Theme) {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    applyTheme(newTheme)
  }

  function applyTheme(t: Theme) {
    const html = document.documentElement

    if (t === 'auto') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      html.classList.toggle('dark', prefersDark)
    } else {
      html.classList.toggle('dark', t === 'dark')
    }
  }

  function toggleTheme() {
    const themes: Theme[] = ['light', 'dark', 'auto']
    const currentIndex = themes.indexOf(theme.value)
    const nextTheme = themes[(currentIndex + 1) % themes.length]
    setTheme(nextTheme)
  }

  // 初始化主题
  applyTheme(theme.value)

  return {
    theme,
    setTheme,
    toggleTheme,
  }
})
