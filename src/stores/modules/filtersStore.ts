import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useStatsStore } from './statsStore'
import { useWeaponsStore } from './weaponsStore'
import { transformName } from '../../model/utils'

export const useFiltersStore = defineStore('filters', () => {
  const statsStore = useStatsStore()
  const weaponsStore = useWeaponsStore()

  // Filter states
  const searchQuery = ref('')
  const selectedWeaponTypes = ref<string[]>([])
  const selectedDamageTypes = ref<string[]>([])
  const showDlcWeapons = ref(localStorage.getItem('stats.showDlcWeapons') !== 'false')

  const setSearchQuery = (query: string) => {
    searchQuery.value = query
  }

  // Filtered weapons computed property
  const filteredWeapons = computed(() => {
    return weaponsStore.weapons.filter((weapon) => {
      // Check if weapon name contains the search query
      const matchesSearch = searchQuery.value === '' ||
        transformName(weapon.name).includes(transformName(searchQuery.value))

      // Check if weapon type is selected (if no types selected, show all)
      const matchesWeaponType = selectedWeaponTypes.value.length === 0 ||
        selectedWeaponTypes.value.includes(weapon.category)

      // Check if damage type is selected (if no types selected, show all)
      const matchesDamageType = selectedDamageTypes.value.length === 0 ||
        selectedDamageTypes.value.includes(weapon.damageTypes.major) ||
        weapon.damageTypes.minor.some(damageType => selectedDamageTypes.value.includes(damageType))

      // Check DLC filter
      const matchesDlcFilter = showDlcWeapons.value || !weapon.dlcExclusive

      // Check if weapon stats are less than or equal to current stats
      const meetsRequirements =
        (
          statsStore.accountForTwoHanded
            ? weapon.requiredAttributes.strengthTwoHand <= statsStore.strength
            : weapon.requiredAttributes.strengthOneHand <= statsStore.strength
        ) &&
        weapon.requiredAttributes.dexterity <= statsStore.dexterity &&
        weapon.requiredAttributes.intelligence <= statsStore.intelligence &&
        weapon.requiredAttributes.faith <= statsStore.faith &&
        weapon.requiredAttributes.arcane <= statsStore.arcane

      return matchesSearch && matchesWeaponType && matchesDamageType && matchesDlcFilter && meetsRequirements
    })
  })

  // Watch for DLC filter changes and update localStorage
  watch(showDlcWeapons, (newValue) => {
    localStorage.setItem('stats.showDlcWeapons', newValue.toString())
  })

  return {
    searchQuery,
    selectedWeaponTypes,
    selectedDamageTypes,
    showDlcWeapons,
    setSearchQuery,
    filteredWeapons,
  }
})
