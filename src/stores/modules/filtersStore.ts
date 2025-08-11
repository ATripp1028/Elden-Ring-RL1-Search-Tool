import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useStatsStore } from './statsStore'
import { useWeaponsStore } from './weaponsStore'
import { transformName } from '../../model/utils'
import { SHIELD_CATEGORIES } from '@/model/constants'

export const useFiltersStore = defineStore('filters', () => {
  const statsStore = useStatsStore()
  const weaponsStore = useWeaponsStore()

  const searchQuery = ref('')
  const selectedWeaponTypes = ref<string[]>([])
  const selectedDamageTypes = ref<string[]>([])
  const showDlcWeapons = ref(localStorage.getItem('stats.showDlcWeapons') !== 'false')
  const hideShields = ref(localStorage.getItem('stats.hideShields') === 'true')

  const setSearchQuery = (query: string) => {
    searchQuery.value = query
  }

  const filteredWeapons = computed(() => {
    return weaponsStore.weapons.filter((weapon) => {
      // Check if weapon name contains the search query
      const matchesSearch = searchQuery.value === '' ||
        transformName(weapon.name).includes(transformName(searchQuery.value))

      // Check if weapon is a shield
      const isShield = SHIELD_CATEGORIES.includes(weapon.category)
      const shouldHideShield = hideShields.value && isShield

      // Check if weapon type is selected (if no types selected, show all)
      const matchesWeaponType = selectedWeaponTypes.value.length === 0 ||
        selectedWeaponTypes.value.includes(weapon.category)

      // Check if damage type is selected (if no types selected, show all)
      const matchesDamageType = selectedDamageTypes.value.length === 0 ||
        selectedDamageTypes.value.includes(weapon.damageTypes.major) ||
        weapon.damageTypes.minor.some(damageType => selectedDamageTypes.value.includes(damageType))

      // Check DLC filter
      const matchesDlcFilter = showDlcWeapons.value || !weapon.dlcExclusive

      // Check if weapon stats are less than or equal to current stats (unless ignoring stats)
      const meetsRequirements = statsStore.ignoreStats || (
        (
          statsStore.accountForTwoHanded
            ? weapon.requiredAttributes.strengthTwoHand <= statsStore.strength
            : weapon.requiredAttributes.strengthOneHand <= statsStore.strength
        ) &&
        weapon.requiredAttributes.dexterity <= statsStore.dexterity &&
        weapon.requiredAttributes.intelligence <= statsStore.intelligence &&
        weapon.requiredAttributes.faith <= statsStore.faith &&
        weapon.requiredAttributes.arcane <= statsStore.arcane
      )

      return matchesSearch && matchesWeaponType && matchesDamageType && matchesDlcFilter && meetsRequirements && !shouldHideShield
    })
  })

  const filteredWeaponTypes = computed(() => {
    return hideShields.value ? weaponsStore.weaponTypes.filter((type) => !SHIELD_CATEGORIES.includes(type)) : weaponsStore.weaponTypes
  })

  watch(showDlcWeapons, (newValue) => {
    localStorage.setItem('stats.showDlcWeapons', newValue.toString())
  })

  watch(hideShields, (newValue) => {
    localStorage.setItem('stats.hideShields', newValue.toString())
    if (newValue) {
      selectedWeaponTypes.value = selectedWeaponTypes.value.filter((type) => !SHIELD_CATEGORIES.includes(type))
    }
  })

  return {
    searchQuery,
    selectedWeaponTypes,
    selectedDamageTypes,
    showDlcWeapons,
    hideShields,
    setSearchQuery,
    filteredWeapons,
    filteredWeaponTypes,
  }
})
