<script setup lang="ts">
import { ref } from 'vue'
import type { TreeNode } from '../types'

defineOptions({ name: 'ImpTreeNode' })

const props = defineProps<{
  node: TreeNode
  selectedId?: string | null
  level?: number
}>()

const emit = defineEmits<{
  select: [node: TreeNode]
}>()

const expanded = ref((props.level ?? 0) < 2)

function select(node: TreeNode) {
  emit('select', node)
}
</script>

<template>
  <div class="tree-node">
    <button
      class="tree-row"
      :class="{ selected: selectedId === node.id }"
      :style="{ paddingLeft: `${(level ?? 0) * 0.9 + 0.4}rem` }"
      type="button"
      @click="select(node)"
    >
      <span class="tree-toggle" @click.stop="node.children.length && (expanded = !expanded)">
        <i
          v-if="node.children.length"
          class="bi"
          :class="expanded ? 'bi-chevron-down' : 'bi-chevron-right'"
        />
      </span>
      <span class="text-truncate">{{ node.text }}</span>
      <span class="badge rounded-pill text-bg-light ms-auto">{{ node.count }}</span>
    </button>

    <div v-if="expanded">
      <ImpTreeNode
        v-for="child in node.children"
        :key="child.id"
        :node="child"
        :selected-id="selectedId"
        :level="(level ?? 0) + 1"
        @select="select"
      />
    </div>
  </div>
</template>
