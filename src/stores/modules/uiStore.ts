import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const selectedColumns = ref<string[]>((() => {
    const stored = localStorage.getItem('stats.selectedColumns')
    return stored ? JSON.parse(stored) : [
      'Image', 'Name', 'Strength', 'Dexterity', 'Intelligence', 'Faith', 'Arcane',
      'Primary Damage', 'Secondary Damage', 'Wiki.gg', 'Fextralife'
    ]
  })())

  const availableColumns = [
    'Image', 'Name', 'Strength', 'Dexterity', 'Intelligence', 'Faith', 'Arcane',
    'Primary Damage', 'Secondary Damage', 'Wiki.gg', 'Fextralife'
  ]

  // Watch for column changes and update localStorage
  watch(selectedColumns, (newValue) => {
    localStorage.setItem('stats.selectedColumns', JSON.stringify(newValue))
  }, { deep: true })

  return {
    selectedColumns,
    availableColumns,
  }
})
