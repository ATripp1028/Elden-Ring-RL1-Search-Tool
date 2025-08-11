import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useUIStore = defineStore('ui', () => {

  const availableColumns = [
    'Image', 'Name', 'Strength', 'Dexterity', 'Intelligence', 'Faith', 'Arcane',
    'Primary Damage', 'Secondary Damage', 'Attack Type', 'Wiki.gg', 'Fextralife'
  ]

  const selectedColumns = ref<string[]>((() => {
    const stored = localStorage.getItem('stats.selectedColumns')
    return stored ? JSON.parse(stored) : availableColumns
  })())

  // Sorting state
  const sortBy = ref<string>((() => {
    const stored = localStorage.getItem('stats.sortBy')
    return stored ? stored : 'Name'
  })())

  const sortOrder = ref<'asc' | 'desc'>((() => {
    const stored = localStorage.getItem('stats.sortOrder') as 'asc' | 'desc' | null
    return stored === 'asc' || stored === 'desc' ? stored : 'asc'
  })())

  const nonSortableColumns = new Set(['Image', 'Wiki.gg', 'Fextralife'])

  const setSort = (columnLabel: string) => {
    if (nonSortableColumns.has(columnLabel)) return
    if (sortBy.value === columnLabel) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    } else {
      sortBy.value = columnLabel
      sortOrder.value = 'asc'
    }
  }

  // Watch for column changes and update localStorage
  watch(selectedColumns, (newValue) => {
    localStorage.setItem('stats.selectedColumns', JSON.stringify(newValue))
  }, { deep: true })

  // Persist sorting
  watch(sortBy, (newValue) => {
    localStorage.setItem('stats.sortBy', newValue)
  })

  watch(sortOrder, (newValue) => {
    localStorage.setItem('stats.sortOrder', newValue)
  })

  return {
    selectedColumns,
    availableColumns,
    sortBy,
    sortOrder,
    setSort,
  }
})
