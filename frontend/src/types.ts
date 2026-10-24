export interface Lookup {
  id: string
  slug: string
  name: string
}

export interface Lookups {
  organisations: Lookup[]
  functions: Lookup[]
  topics: Lookup[]
  tags: Lookup[]
}

export interface SourceInfo {
  source_type: string
  source_name: string
  external_id: string
  external_url?: string | null
  source_state: string
}

export interface Item {
  id: string
  title: string
  description: string
  type: 'idea' | 'action' | 'commitment' | 'process' | 'waiting' | 'reference'
  state: 'open' | 'active' | 'done' | 'cancelled' | 'archived'
  due_at?: string | null
  review_after?: string | null
  delegated_to?: string | null
  waiting_for?: string | null
  organisations: Lookup[]
  functions: Lookup[]
  topics: Lookup[]
  tags: Lookup[]
  source?: SourceInfo | null
  in_current_sprint: boolean
  sprint_kind?: string | null
  created_at: string
  updated_at: string
}

export interface TreeNode {
  id: string
  text: string
  kind: string
  count: number
  filters: Record<string, string | boolean>
  children: TreeNode[]
}
