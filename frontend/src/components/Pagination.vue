<script setup lang="ts">
import { computed } from 'vue'
import { NButton, NSpace } from 'naive-ui'

const props = defineProps<{
  current: number
  total: number
  pageSize: number
  onPageChange: (page: number) => void
}>()

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))

const pages = computed(() => {
  const result: (number | '...')[] = []
  if (totalPages.value <= 7) {
    for (let i = 1; i <= totalPages.value; i++) {
      result.push(i)
    }
  } else {
    if (props.current <= 3) {
      for (let i = 1; i <= 5; i++) result.push(i)
      result.push('...')
      result.push(totalPages.value)
    } else if (props.current >= totalPages.value - 2) {
      result.push(1)
      result.push('...')
      for (let i = totalPages.value - 4; i <= totalPages.value; i++) {
        result.push(i)
      }
    } else {
      result.push(1)
      result.push('...')
      for (let i = props.current - 1; i <= props.current + 1; i++) {
        result.push(i)
      }
      result.push('...')
      result.push(totalPages.value)
    }
  }
  return result
})

function handleClick(page: number | '...') {
  if (page === '...' || page === props.current) return
  props.onPageChange(page as number)
}
</script>

<template>
  <div class="flex justify-center items-center gap-2 py-6">
    <NSpace>
      <NButton
        :disabled="current <= 1"
        @click="handleClick(current - 1)"
        size="small"
      >
        上一页
      </NButton>

      <template v-for="page in pages" :key="page">
        <NButton
          v-if="page !== '...'"
          :type="page === current ? 'primary' : 'default'"
          @click="handleClick(page)"
          size="small"
        >
          {{ page }}
        </NButton>
        <NButton v-else disabled size="small">
          ...
        </NButton>
      </template>

      <NButton
        :disabled="current >= totalPages"
        @click="handleClick(current + 1)"
        size="small"
      >
        下一页
      </NButton>
    </NSpace>
  </div>
</template>
