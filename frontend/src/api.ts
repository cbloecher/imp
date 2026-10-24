import type { Item, Lookups, TreeNode } from './types'

const API_BASE = import.meta.env.VITE_API_BASE || ''

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || `HTTP ${response.status}`)
  }
  return response.json()
}

export const api = {
  tree: () => request<TreeNode[]>('/api/tree'),
  lookups: () => request<Lookups>('/api/lookups'),
  items: (filters: Record<string, string | boolean> = {}) => {
    const params = new URLSearchParams()
    Object.entries(filters).forEach(([key, value]) => params.set(key, String(value)))
    const suffix = params.size ? `?${params.toString()}` : ''
    return request<Item[]>(`/api/items${suffix}`)
  },
  createItem: (title: string) =>
    request<Item>('/api/items', {
      method: 'POST',
      body: JSON.stringify({ title, description: '', type: 'idea', state: 'open' }),
    }),
  updateItem: (id: string, payload: Record<string, unknown>) =>
    request<Item>(`/api/items/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    }),
  createLookup: (kind: keyof Lookups, name: string) =>
    request(`/api/lookups/${kind}`, {
      method: 'POST',
      body: JSON.stringify({ name }),
    }),
  renameLookup: (kind: keyof Lookups, id: string, name: string) =>
    request(`/api/lookups/${kind}/${id}`, {
      method: 'PATCH',
      body: JSON.stringify({ name }),
    }),
  setSprint: (id: string, included: boolean, kind = 'focus') =>
    request<Item>(`/api/items/${id}/sprint`, {
      method: 'PUT',
      body: JSON.stringify({ included, kind }),
    }),
}
