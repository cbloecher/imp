<script setup lang="ts">
import { ref } from 'vue'
import { api } from './api'
import type { Item, Lookups, TreeNode } from './types'
import ImpTreeNode from './components/TreeNode.vue'
import NewItemForm from './components/NewItemForm.vue'
import ItemList from './components/ItemList.vue'
import ItemDetail from './components/ItemDetail.vue'

const tree = ref<TreeNode[]>([])
const items = ref<Item[]>([])
const lookups = ref<Lookups>({ organisations: [], functions: [], topics: [], tags: [] })
const selectedNode = ref<TreeNode | null>(null)
const selectedItem = ref<Item | null>(null)
const loading = ref(false)
const error = ref('')

async function refreshTree() {
  tree.value = await api.tree()
}

async function refreshLookups() {
  lookups.value = await api.lookups()
}

async function loadItems(filters: Record<string, string | boolean> = selectedNode.value?.filters || {}) {
  loading.value = true
  try {
    items.value = await api.items(filters)
    if (selectedItem.value) {
      selectedItem.value = items.value.find(item => item.id === selectedItem.value?.id) || null
    }
  } finally {
    loading.value = false
  }
}

async function init() {
  error.value = ''
  try {
    await Promise.all([refreshTree(), refreshLookups()])
    const root = tree.value[0]
    const inbox = root?.children.find(node => node.id === 'view:inbox')
    selectedNode.value = inbox || root || null
    await loadItems()
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  }
}

async function selectNode(node: TreeNode) {
  selectedNode.value = node
  selectedItem.value = null
  await loadItems(node.filters)
}

async function createItem(title: string) {
  const item = await api.createItem(title)
  await Promise.all([refreshTree(), loadItems()])
  selectedItem.value = item
}

async function saveItem(payload: Record<string, unknown>) {
  if (!selectedItem.value) return
  selectedItem.value = await api.updateItem(selectedItem.value.id, payload)
  await Promise.all([refreshTree(), loadItems()])
}

async function setSprint(included: boolean, kind: string) {
  if (!selectedItem.value) return
  selectedItem.value = await api.setSprint(selectedItem.value.id, included, kind)
  await Promise.all([refreshTree(), loadItems()])
}

async function createLookup(kind: keyof Lookups, name: string) {
  const value = name.trim()
  if (!value) return
  await api.createLookup(kind, value)
  await refreshLookups()
}

async function renameTag(id: string, name: string) {
  await api.renameLookup('tags', id, name)
  await Promise.all([refreshLookups(), refreshTree(), loadItems()])
}

init()
</script>

<template>
  <div class="app-shell">
    <header class="topbar border-bottom">
      <div>
        <span class="brand">IMP</span>
        <span class="text-secondary ms-2">Integrated Management Plane</span>
      </div>
      <span class="badge text-bg-light border">PoC</span>
    </header>

    <div class="capture-row border-bottom">
      <NewItemForm @create="createItem" />
    </div>

    <div v-if="error" class="alert alert-danger m-3">{{ error }}</div>

    <main class="workspace">
      <aside class="tree-pane border-end">
        <div class="pane-heading">Navigation</div>
        <ImpTreeNode
          v-for="node in tree"
          :key="node.id"
          :node="node"
          :selected-id="selectedNode?.id"
          :level="0"
          @select="selectNode"
        />
      </aside>

      <section class="list-pane border-end">
        <div class="pane-heading d-flex justify-content-between">
          <span>{{ selectedNode?.text || 'Alle' }}</span>
          <span class="text-secondary">{{ items.length }}</span>
        </div>
        <div v-if="loading" class="p-3 text-secondary">Lade …</div>
        <ItemList
          v-else
          :items="items"
          :selected-id="selectedItem?.id"
          @select="selectedItem = $event"
        />
      </section>

      <section class="detail-pane">
        <ItemDetail
          v-if="selectedItem"
          :item="selectedItem"
          :lookups="lookups"
          @save="saveItem"
          @sprint="setSprint"
          @create-lookup="createLookup"
          @rename-tag="renameTag"
        />
        <div v-else class="empty-detail">
          <i class="bi bi-card-text fs-1 text-secondary" />
          <div>Item auswählen, um Details zu bearbeiten.</div>
        </div>
      </section>
    </main>
  </div>
</template>
