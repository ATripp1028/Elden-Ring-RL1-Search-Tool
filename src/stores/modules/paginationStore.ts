import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useFiltersStore } from './filtersStore'
import { useStatsStore } from './statsStore'
import { useUIStore } from './uiStore'

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
    const list = [...filtersStore.filteredWeapons]
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

    const getStrength = (w: any) => {
      return statsStore.accountForTwoHanded
        ? w.requiredAttributes.strengthTwoHand
        : w.requiredAttributes.strengthOneHand
    }

    list.sort((a: any, b: any) => {
      let result = 0
      switch (column) {
        case 'Name':
          result = compareStrings(a.name, b.name)
          break
        case 'Strength':
          result = compareNumbers(getStrength(a), getStrength(b))
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
        case 'Primary Damage':
          result = compareStrings(a.damageTypes.major, b.damageTypes.major)
          break
        case 'Secondary Damage': {
          const aMinor = (a.damageTypes.minor && a.damageTypes.minor.length)
            ? a.damageTypes.minor.join(', ')
            : ''
          const bMinor = (b.damageTypes.minor && b.damageTypes.minor.length)
            ? b.damageTypes.minor.join(', ')
            : ''
          result = compareStrings(aMinor, bMinor)
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
