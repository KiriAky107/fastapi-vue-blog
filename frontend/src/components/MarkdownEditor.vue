<script setup lang="ts">
import { ref, watch } from 'vue'
import VMdEditor from '@kangc/v-md-editor'
import '@kangc/v-md-editor/lib/style/style.css'
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js'
import '@kangc/v-md-editor/lib/theme/style/github.css'
import hljs from 'highlight.js'

// 配置主题
VMdEditor.use(githubTheme, {
  hljs,
})

const props = defineProps<{
  modelValue: string
  placeholder?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const content = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  content.value = newVal
})

watch(content, (newVal) => {
  emit('update:modelValue', newVal)
})

function handleInput(value: string) {
  content.value = value
}
</script>

<template>
  <div class="markdown-editor">
    <VMdEditor
      v-model="content"
      :placeholder="placeholder || '开始撰写...'"
      height="400px"
      mode="edit"
      @change="handleInput"
    />
  </div>
</template>

<style scoped>
.markdown-editor :deep(.v-md-editor) {
  border: 1px solid var(--gray-300, #d1d5db);
  border-radius: 0.5rem;
}

.markdown-editor :deep(.v-md-editor--fullscreen) {
  z-index: 1000;
}
</style>
