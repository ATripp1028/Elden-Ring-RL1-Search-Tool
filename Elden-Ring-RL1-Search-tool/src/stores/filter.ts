import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useFilterStore = defineStore('filter', () => {
  const searchQuery = ref('')

  function setSearchQuery(query: string) {
    searchQuery.value = query
  }

  return {
    searchQuery,
    setSearchQuery
  }
}) 