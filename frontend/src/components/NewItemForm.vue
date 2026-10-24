<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  create: [title: string]
}>()

const title = ref('')

function submit() {
  const value = title.value.trim()
  if (!value) return
  emit('create', value)
  title.value = ''
}
</script>

<template>
  <form class="quick-capture" @submit.prevent="submit">
    <div class="input-group">
      <span class="input-group-text"><i class="bi bi-plus-lg" /></span>
      <input
        v-model="title"
        class="form-control"
        placeholder="Was liegt auf dem Zettel?"
        aria-label="Neues Item"
      />
      <button class="btn btn-primary" type="submit">Erfassen</button>
    </div>
  </form>
</template>
