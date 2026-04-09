<script setup lang="ts">
import { computed, watch, onMounted } from 'vue'

const props = defineProps<{
  title?: string
  description?: string
  image?: string
  url?: string
}>()

const defaultTitle = 'ACG Blog'
const defaultDescription = '一个 ACG 风格的博客系统'

const finalTitle = computed(() => {
  return props.title ? `${props.title} | ${defaultTitle}` : defaultTitle
})

const finalDescription = computed(() => props.description || defaultDescription)

function updateMeta() {
  // Update title
  document.title = finalTitle.value

  // Update meta tags
  updateMetaTag('description', finalDescription.value)
  updateMetaTag('og:title', finalTitle.value)
  updateMetaTag('og:description', finalDescription.value)
  updateMetaTag('twitter:title', finalTitle.value)
  updateMetaTag('twitter:description', finalDescription.value)

  if (props.image) {
    updateMetaTag('og:image', props.image)
    updateMetaTag('twitter:image', props.image)
  }

  if (props.url) {
    updateMetaTag('og:url', props.url)
  }
}

function updateMetaTag(name: string, content: string) {
  let meta = document.querySelector(`meta[name="${name}"]`) || document.querySelector(`meta[property="${name}"]`)

  if (!meta) {
    meta = document.createElement('meta')
    if (name.startsWith('og:') || name.startsWith('twitter:')) {
      meta.setAttribute('property', name)
    } else {
      meta.setAttribute('name', name)
    }
    document.head.appendChild(meta)
  }

  meta.setAttribute('content', content)
}

watch(() => [props.title, props.description, props.image, props.url], updateMeta)

onMounted(updateMeta)
</script>

<template>
  <!-- No visual output, only meta tags -->
</template>
