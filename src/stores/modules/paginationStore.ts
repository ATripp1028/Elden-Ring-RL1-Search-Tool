import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useFiltersStore } from './filtersStore'
import { useStatsStore } from './statsStore'
import { useUIStore } from './uiStore'
import type { ProcessedWeapon } from './weaponsStore'

export const usePaginationStore = defineStore('pagination', () => {
  const filtersStore = useFiltersStore()
  const statsStore = useStatsStore()
  const uiStore = useUIStore()

  const page = ref(1)
  const itemsPerPage = ref(10)

  const totalPages = computed(() => {
    return Math.ceil(filtersStore.filteredWeapons.length / itemsPerPage.value)
  })

  const sortedWeapons = computed(() => {
    const list: ProcessedWeapon[] = [...filtersStore.filteredWeapons]
    const column = uiStore.sortBy
    const order = uiStore.sortOrder

    const compareStrings = (a: string | undefined, b: string | undefined) => {
      return (a || '').localeCompare(b || '', undefined, { sensitivity: 'base' })
    }

    const compareNumbers = (a: number | undefined, b: number | undefined) => {
      const na = a ?? Number.NEGATIVE_INFINITY
      const nb = b ?? Number.NEGATIVE_INFINITY
      return na - nb
    }

    list.sort((a: ProcessedWeapon, b: ProcessedWeapon) => {
      let result = 0
      switch (column) {
        case 'Name':
          result = compareStrings(a.name, b.name)
          break
        case 'Weapon Type':
          result = compareStrings(a.category, b.category)
          break
        case 'Strength':
          result = compareNumbers(a.requiredAttributes.strengthOneHand, b.requiredAttributes.strengthOneHand)
          break
        case 'Dexterity':
          result = compareNumbers(a.requiredAttributes.dexterity, b.requiredAttributes.dexterity)
          break
        case 'Intelligence':
          result = compareNumbers(a.requiredAttributes.intelligence, b.requiredAttributes.intelligence)
          break
        case 'Faith':
          result = compareNumbers(a.requiredAttributes.faith, b.requiredAttributes.faith)
          break
        case 'Arcane':
          result = compareNumbers(a.requiredAttributes.arcane, b.requiredAttributes.arcane)
          break
        case 'Damage Type': {
          const aJoined = (a.trackedDamageTypes && a.trackedDamageTypes.length)
            ? a.trackedDamageTypes.join(', ')
            : ''
          const bJoined = (b.trackedDamageTypes && b.trackedDamageTypes.length)
            ? b.trackedDamageTypes.join(', ')
            : ''
          result = compareStrings(aJoined, bJoined)
          break
        }
        case 'Attack Type': {
          result = compareStrings(a.attackTypes.primary, b.attackTypes.primary)
          break
        }
        default:
          // If unknown or non-sortable, keep original order
          result = 0
      }

      return order === 'asc' ? result : -result
    })

    return list
  })

  const paginatedWeapons = computed(() => {
    const start = (page.value - 1) * itemsPerPage.value
    const end = start + itemsPerPage.value
    return sortedWeapons.value.slice(start, end)
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
  watch(() => filtersStore.selectedAttackTypes, resetPage, { deep: true })
  watch(() => uiStore.sortBy, resetPage)
  watch(() => uiStore.sortOrder, resetPage)

  return {
    page,
    itemsPerPage,
    totalPages,
    sortedWeapons,
    paginatedWeapons,
    resetPage,
  }
})
