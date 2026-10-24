<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import type { Item, Lookups, Lookup } from '../types'

const props = defineProps<{
  item: Item
  lookups: Lookups
}>()

const emit = defineEmits<{
  save: [payload: Record<string, unknown>]
  sprint: [included: boolean, kind: string]
  createLookup: [kind: keyof Lookups, name: string]
  renameTag: [id: string, name: string]
}>()

const draft = reactive({
  title: '',
  description: '',
  type: 'idea',
  state: 'open',
  due_at: '',
  review_after: '',
  delegated_to: '',
  waiting_for: '',
  organisation_ids: [] as string[],
  function_ids: [] as string[],
  topic_ids: [] as string[],
  tag_ids: [] as string[],
})

const newTag = ref('')

function reset() {
  draft.title = props.item.title
  draft.description = props.item.description
  draft.type = props.item.type
  draft.state = props.item.state
  draft.due_at = props.item.due_at || ''
  draft.review_after = props.item.review_after || ''
  draft.delegated_to = props.item.delegated_to || ''
  draft.waiting_for = props.item.waiting_for || ''
  draft.organisation_ids = props.item.organisations.map(x => x.id)
  draft.function_ids = props.item.functions.map(x => x.id)
  draft.topic_ids = props.item.topics.map(x => x.id)
  draft.tag_ids = props.item.tags.map(x => x.id)
}

watch(() => props.item.id, reset, { immediate: true })
watch(() => props.item, reset, { deep: true })

function save() {
  emit('save', {
    ...draft,
    due_at: draft.due_at || null,
    review_after: draft.review_after || null,
    delegated_to: draft.delegated_to || null,
    waiting_for: draft.waiting_for || null,
  })
}

function addTag() {
  const name = newTag.value.trim()
  if (!name) return
  emit('createLookup', 'tags', name)
  newTag.value = ''
}

function addTopic() {
  const name = window.prompt('Neues Thema')?.trim()
  if (name) emit('createLookup', 'topics', name)
}

function renameTag(tag: Lookup) {
  const name = window.prompt('Tag umbenennen', tag.name)?.trim()
  if (name && name !== tag.name) emit('renameTag', tag.id, name)
}

const sourceBadge = computed(() => props.item.source?.source_state || null)
</script>

<template>
  <div class="detail-panel p-3">
    <div class="d-flex align-items-start justify-content-between gap-2 mb-3">
      <div class="flex-grow-1">
        <input v-model="draft.title" class="form-control form-control-lg fw-semibold" />
        <div class="small text-secondary mt-1">ID {{ item.id }}</div>
      </div>
      <button class="btn btn-primary" @click="save">Speichern</button>
    </div>

    <div v-if="item.source" class="alert alert-light border py-2">
      <strong>{{ item.source.source_name }}</strong>
      <span class="ms-2">{{ item.source.external_id }}</span>
      <span class="badge text-bg-secondary ms-2">{{ sourceBadge }}</span>
    </div>

    <label class="form-label">Beschreibung</label>
    <textarea v-model="draft.description" class="form-control mb-3" rows="5" />

    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <label class="form-label">Typ</label>
        <select v-model="draft.type" class="form-select">
          <option value="idea">Idee</option>
          <option value="action">Aktion</option>
          <option value="commitment">Verbindliche Aufgabe</option>
          <option value="process">Vorgang / Paket</option>
          <option value="waiting">Warten</option>
          <option value="reference">Referenz</option>
        </select>
      </div>
      <div class="col-md-6">
        <label class="form-label">Bearbeitungsstatus</label>
        <select v-model="draft.state" class="form-select">
          <option value="open">Offen</option>
          <option value="active">In Bearbeitung</option>
          <option value="done">Erledigt</option>
          <option value="cancelled">Verworfen</option>
          <option value="archived">Archiviert</option>
        </select>
      </div>
    </div>

    <div class="form-check form-switch mb-3">
      <input
        id="sprint-switch"
        class="form-check-input"
        type="checkbox"
        :checked="item.in_current_sprint"
        @change="emit('sprint', ($event.target as HTMLInputElement).checked, 'focus')"
      />
      <label class="form-check-label" for="sprint-switch">Im nächsten Sprint</label>
    </div>

    <div class="row g-2 mb-3">
      <div class="col-md-6">
        <label class="form-label">Fällig</label>
        <input v-model="draft.due_at" type="date" class="form-control" />
      </div>
      <div class="col-md-6">
        <label class="form-label">Wiedervorlage</label>
        <input v-model="draft.review_after" type="date" class="form-control" />
      </div>
      <div class="col-md-6">
        <label class="form-label">Delegiert an</label>
        <input v-model="draft.delegated_to" class="form-control" placeholder="Person / Rolle" />
      </div>
      <div class="col-md-6">
        <label class="form-label">Wartet auf</label>
        <input v-model="draft.waiting_for" class="form-control" placeholder="Antwort / Ereignis" />
      </div>
    </div>

    <div class="row g-2">
      <div class="col-md-6">
        <label class="form-label">Organisation</label>
        <select v-model="draft.organisation_ids" class="form-select" multiple size="4">
          <option v-for="entry in lookups.organisations" :key="entry.id" :value="entry.id">
            {{ entry.name }}
          </option>
        </select>
      </div>
      <div class="col-md-6">
        <label class="form-label">Funktion</label>
        <select v-model="draft.function_ids" class="form-select" multiple size="4">
          <option v-for="entry in lookups.functions" :key="entry.id" :value="entry.id">
            {{ entry.name }}
          </option>
        </select>
      </div>
      <div class="col-md-6">
        <div class="d-flex justify-content-between align-items-center">
          <label class="form-label">Thema</label>
          <button type="button" class="btn btn-sm btn-link p-0" @click="addTopic">+ Thema</button>
        </div>
        <select v-model="draft.topic_ids" class="form-select" multiple size="5">
          <option v-for="entry in lookups.topics" :key="entry.id" :value="entry.id">
            {{ entry.name }}
          </option>
        </select>
      </div>
      <div class="col-md-6">
        <label class="form-label">Tags</label>
        <select v-model="draft.tag_ids" class="form-select mb-2" multiple size="3">
          <option
            v-for="entry in lookups.tags"
            :key="entry.id"
            :value="entry.id"
            @dblclick="renameTag(entry)"
          >
            {{ entry.name }}
          </option>
        </select>
        <div class="input-group input-group-sm">
          <input v-model="newTag" class="form-control" placeholder="Neuer Tag" @keyup.enter="addTag" />
          <button class="btn btn-outline-secondary" type="button" @click="addTag">+</button>
        </div>
        <div class="form-text">Doppelklick auf einen Tag: umbenennen.</div>
      </div>
    </div>
  </div>
</template>
