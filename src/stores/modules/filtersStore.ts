import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useStatsStore } from './statsStore'
import { useWeaponsStore } from './weaponsStore'
import { transformName } from '../../model/utils'
import { SHIELD_CATEGORIES } from '@/model/constants'
import { DataType } from '@/model/types'

export const useFiltersStore = defineStore('filters', () => {
  const statsStore = useStatsStore()
  const weaponsStore = useWeaponsStore()

  const searchQuery = ref('')
  const selectedDataType = ref<DataType>(DataType.WeaponsOnly)
  const selectedWeaponTypes = ref<string[]>([])
  const selectedDamageTypes = ref<string[]>([])
  const selectedAttackTypes = ref<string[]>([])
  const selectedStatusBuildups = ref<string[]>([])
  const showDlcWeapons = ref(localStorage.getItem('stats.showDlcWeapons') !== 'false')
  const hideShields = ref(localStorage.getItem('stats.hideShields') === 'true')

  const setSearchQuery = (query: string) => {
    searchQuery.value = query
  }

  const filteredWeapons = computed(() => {
    return weaponsStore.weapons.filter((item) => {
      // Check data type filter
      const isWeapon = item.type === 'weapon'
      const isSpell = item.type === 'spell'
      const isStaveOrSeal = isWeapon && (item.category === 'Staves' || item.category === 'Sacred Seals')

      let matchesDataType = false
      if (selectedDataType.value === DataType.WeaponsOnly) {
        // For weapons only, exclude spells and include staves/seals only if showing spells too
        matchesDataType = isWeapon && !isStaveOrSeal
      } else if (selectedDataType.value === DataType.SpellsOnly) {
        // For spells only, include spells and staves/seals
        matchesDataType = isSpell || isStaveOrSeal
      } else { // Both
        matchesDataType = true
      }

      // Check if item name contains the search query
      const matchesSearch = searchQuery.value === '' ||
        transformName(item.name).includes(transformName(searchQuery.value))

      // Check if weapon is a shield (only applicable to weapons)
      const isShield = isWeapon && SHIELD_CATEGORIES.includes(item.category)
      const shouldHideShield = hideShields.value && isShield

      // Check if item type is selected (if no types selected, show all)
      const matchesItemType = selectedWeaponTypes.value.length === 0 ||
        selectedWeaponTypes.value.includes(item.category)

      // Check if damage type is selected (if no types selected, show all)
      // For items with Physical + Elemental, only match on elemental types
      const matchesDamageType = selectedDamageTypes.value.length === 0 ||
        item.trackedDamageTypes.some((damageType) => selectedDamageTypes.value.includes(damageType))

      // Check if primary attack type is selected (if no types selected, show all)
      // For spells, this might not be applicable
      const matchesAttackType = selectedAttackTypes.value.length === 0 ||
        (isWeapon && selectedAttackTypes.value.includes(item.attackTypes.primary))

      // Check if status buildup is selected (if no types selected, show all)
      const matchesStatusBuildup = selectedStatusBuildups.value.length === 0 ||
        selectedStatusBuildups.value.includes(item.statusBuildup)

      // Check DLC filter
      const matchesDlcFilter = showDlcWeapons.value || !item.dlcExclusive

      // Check if item stats are less than or equal to current stats (unless ignoring stats)
      const meetsRequirements = statsStore.ignoreStats || (
        (isWeapon ? (
          statsStore.accountForTwoHanded
            ? item.requiredAttributes.strengthTwoHand <= statsStore.strength
            : item.requiredAttributes.strengthOneHand <= statsStore.strength
        ) : true) &&
        (isWeapon ? item.requiredAttributes.dexterity <= statsStore.dexterity : true) &&
        item.requiredAttributes.intelligence <= statsStore.intelligence &&
        item.requiredAttributes.faith <= statsStore.faith &&
        item.requiredAttributes.arcane <= statsStore.arcane
      )

      return matchesDataType && matchesSearch && matchesItemType && matchesDamageType && matchesAttackType && matchesStatusBuildup && matchesDlcFilter && meetsRequirements && !shouldHideShield
    })
  })

  const filteredWeaponTypes = computed(() => {
    let types: string[] = []

    if (selectedDataType.value === DataType.WeaponsOnly) {
      // Show weapon types excluding staves and seals
      types = weaponsStore.weaponTypes.filter((type) =>
        type !== 'Staves' && type !== 'Sacred Seals'
      )
    } else if (selectedDataType.value === DataType.SpellsOnly) {
      // Show spell types and staves/seals
      types = [...weaponsStore.spellTypes, 'Staves', 'Sacred Seals']
    } else { // Both
      // Show all types
      types = [...weaponsStore.weaponTypes, ...weaponsStore.spellTypes]
    }

    // Apply shield filter if needed
    return hideShields.value ? types.filter((type) => !SHIELD_CATEGORIES.includes(type)) : types
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
    selectedDataType,
    selectedWeaponTypes,
    selectedDamageTypes,
    selectedAttackTypes,
    selectedStatusBuildups,
    showDlcWeapons,
    hideShields,
    setSearchQuery,
    filteredWeapons,
    filteredWeaponTypes,
  }
})
