import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useFiltersStore } from './filtersStore'
import { useStatsStore } from './statsStore'

export const usePaginationStore = defineStore('pagination', () => {
  const filtersStore = useFiltersStore()
  const statsStore = useStatsStore()

  const page = ref(1)
  const itemsPerPage = ref(10)

  const totalPages = computed(() => {
    return Math.ceil(filtersStore.filteredWeapons.length / itemsPerPage.value)
  })

  const paginatedWeapons = computed(() => {
    const start = (page.value - 1) * itemsPerPage.value
    const end = start + itemsPerPage.value
    return filtersStore.filteredWeapons.slice(start, end)
  })

  const resetPage = () => {
    page.value = 1
  }

  // Watch for changes that should reset pagination
  watch(() => statsStore.strength, resetPage)
  watch(() => statsStore.dexterity, resetPage)
  watch(() => statsStore.intelligence, resetPage)
  watch(() => statsStore.faith, resetPage)
  watch(() => statsStore.arcane, resetPage)
  watch(() => filtersStore.showDlcWeapons, resetPage)
  watch(() => filtersStore.selectedDamageTypes, resetPage, { deep: true })

  return {
    page,
    itemsPerPage,
    totalPages,
    paginatedWeapons,
    resetPage,
  }
})
