import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useUIStore = defineStore('ui', () => {

  const availableColumns = [
    'Image', 'Name', 'Strength', 'Dexterity', 'Intelligence', 'Faith', 'Arcane',
    'Damage Type', 'Attack Type', 'Wiki.gg', 'Fextralife'
  ]

  const selectedColumns = ref<string[]>((() => {
    const stored = localStorage.getItem('stats.selectedColumns')
    const parsed: unknown = stored ? JSON.parse(stored) : availableColumns
    let cols = Array.isArray(parsed) ? (parsed as string[]) : availableColumns
    const hadOldDamageCols = cols.includes('Primary Damage') || cols.includes('Secondary Damage')
    // Remove deprecated columns and any unknowns
    cols = cols.filter((c) => c !== 'Primary Damage' && c !== 'Secondary Damage' && availableColumns.includes(c))
    // If user previously showed either old damage column, include the new combined column
    if (hadOldDamageCols && !cols.includes('Damage Type')) {
      // Insert near stats columns by default: after Arcane if present, else append
      const arcaneIndex = cols.indexOf('Arcane')
      if (arcaneIndex >= 0) {
        cols.splice(arcaneIndex + 1, 0, 'Damage Type')
      } else {
        cols.push('Damage Type')
      }
    }
    return cols
  })())

  // Sorting state
  const sortBy = ref<string>((() => {
    const stored = localStorage.getItem('stats.sortBy')
    let value = stored ? stored : 'Name'
    if (value === 'Primary Damage' || value === 'Secondary Damage') {
      value = 'Damage Type'
      localStorage.setItem('stats.sortBy', value)
    }
    return value
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
