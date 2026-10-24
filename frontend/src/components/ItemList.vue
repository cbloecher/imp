<script setup lang="ts">
import type { Item } from '../types'

defineProps<{
  items: Item[]
  selectedId?: string | null
}>()

const emit = defineEmits<{
  select: [item: Item]
}>()

function typeLabel(type: Item['type']) {
  return {
    idea: 'Idee',
    action: 'Aktion',
    commitment: 'Verbindlich',
    process: 'Vorgang',
    waiting: 'Warten',
    reference: 'Referenz',
  }[type]
}
</script>

<template>
  <div class="item-list">
    <button
      v-for="item in items"
      :key="item.id"
      type="button"
      class="item-row"
      :class="{ selected: selectedId === item.id }"
      @click="emit('select', item)"
    >
      <div class="d-flex gap-2 align-items-start">
        <i class="bi bi-circle mt-1 text-secondary" />
        <div class="min-w-0 flex-grow-1">
          <div class="fw-semibold text-truncate">{{ item.title }}</div>
          <div class="d-flex flex-wrap gap-1 mt-1">
            <span class="badge text-bg-secondary">{{ typeLabel(item.type) }}</span>
            <span v-if="item.in_current_sprint" class="badge text-bg-primary">Sprint</span>
            <span v-if="item.delegated_to" class="badge text-bg-info">delegiert</span>
            <span v-if="item.waiting_for" class="badge text-bg-warning">wartet</span>
            <span v-if="item.review_after" class="badge border text-body">WV {{ item.review_after }}</span>
          </div>
        </div>
      </div>
    </button>

    <div v-if="!items.length" class="p-4 text-secondary text-center">
      Keine Einträge in dieser Ansicht.
    </div>
  </div>
</template>
