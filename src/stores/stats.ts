import { defineStore } from 'pinia'
import { ref, watch, computed } from 'vue'
import { getStoredValue } from '../model/utils'
import weaponsThrustingShields from '../resources/weapons_thrusting_shields.json'
import weaponsGreatshields from '../resources/weapons_greatshields.json'
import weaponsMediumShields from '../resources/weapons_medium_shields.json'
import weaponsSmallShields from '../resources/weapons_small_shields.json'
import weaponsTorches from '../resources/weapons_torches.json'
import weaponsSacredSeals from '../resources/weapons_sacred_seals.json'
import weaponsStaves from '../resources/weapons_staves.json'
import weaponsBallista from '../resources/weapons_ballista.json'
import weaponsCrossbows from '../resources/weapons_crossbows.json'
import weaponsGreatbows from '../resources/weapons_greatbows.json'
import weaponsBows from '../resources/weapons_bows.json'
import weaponsLightBows from '../resources/weapons_light_bows.json'
import weaponsPerfumeBottles from '../resources/weapons_perfume_bottles.json'
import weaponsBeastClaws from '../resources/weapons_beast_claws.json'
import weaponsClaws from '../resources/weapons_claws.json'
import weaponsHandToHand from '../resources/weapons_hand_to_hand.json'
import weaponsFists from '../resources/weapons_fists.json'
import weaponsWhips from '../resources/weapons_whips.json'
import weaponsReapers from '../resources/weapons_reapers.json'
import weaponsHalberds from '../resources/weapons_halberds.json'
import weaponsGreatSpears from '../resources/weapons_great_spears.json'
import weaponsSpears from '../resources/weapons_spears.json'
import weaponsColossalWeapons from '../resources/weapons_colossal_weapons.json'
import weaponsGreatHammers from '../resources/weapons_great_hammers.json'
import weaponsFlails from '../resources/weapons_flails.json'
import weaponsHammers from '../resources/weapons_hammers.json'
import weaponsGreataxes from '../resources/weapons_greataxes.json'
import weaponsAxes from '../resources/weapons_axes.json'
import weaponsTwinblades from '../resources/weapons_twinblades.json'
import weaponsGreatKatanas from '../resources/weapons_great_katanas.json'
import weaponsKatanas from '../resources/weapons_katanas.json'
import weaponsBackhandBlades from '../resources/weapons_backhand_blades.json'
import weaponsCurvedGreatswords from '../resources/weapons_curved_greatswords.json'
import weaponsCurvedSwords from '../resources/weapons_curved_swords.json'
import weaponsHeavyThrustingSwords from '../resources/weapons_heavy_thrusting_swords.json'
import weaponsThrustingSwords from '../resources/weapons_thrusting_swords.json'
import weaponsColossalSwords from '../resources/weapons_colossal_swords.json'
import weaponsGreatswords from '../resources/weapons_greatswords.json'
import weaponsLightGreatswords from '../resources/weapons_light_greatswords.json'
import weaponsStraightSwords from '../resources/weapons_straight_swords.json'
import weaponsDaggers from '../resources/weapons_daggers.json'
import weaponsThrowingBlades from '../resources/weapons_throwing_blades.json'

interface ScrapedWeapon {
  weapon_name: string
  weapon_type: string
  attributes?: {
    strength?: { one_hand: number; two_hand: number }
    dexterity?: number
    intelligence?: number
    faith?: number
    arcane?: number
  }
  image?: {
    src: string
  }
  wikiGGLink?: string
  wikiFextralifeLink?: string
}

export const useStatsStore = defineStore('stats', () => {
  const strength = ref(getStoredValue('stats.strength', 10))
  const dexterity = ref(getStoredValue('stats.dexterity', 10))
  const intelligence = ref(getStoredValue('stats.intelligence', 10))
  const faith = ref(getStoredValue('stats.faith', 10))
  const arcane = ref(getStoredValue('stats.arcane', 10))

  const weaponTypes = [
    'Axes',
    'Backhand Blades',
    'Ballistas',
    'Beast Claws',
    'Bows',
    'Claws',
    'Colossal Swords',
    'Colossal Weapons',
    'Crossbows',
    'Curved Greatswords',
    'Curved Swords',
    'Daggers',
    'Fists',
    'Flails',
    'Great Hammers',
    'Great Katanas',
    'Great Spears',
    'Greataxes',
    'Greatbows',
    'Greatshields',
    'Greatswords',
    'Halberds',
    'Hammers',
    'Hand-to-Hand',
    'Heavy Thrusting Swords',
    'Katanas',
    'Light Bows',
    'Light Greatswords',
    'Medium Shields',
    'Perfume Bottles',
    'Reapers',
    'Sacred Seals',
    'Small Shields',
    'Spears',
    'Staves',
    'Straight Swords',
    'Throwing Blades',
    'Thrusting Shields',
    'Thrusting Swords',
    'Torches',
    'Twinblades',
    'Whips',
  ]

  const page = ref(1)
  const itemsPerPage = ref(10)
  const selectedWeaponTypes = ref<string[]>([])

  const searchQuery = ref('')
  const accountForTwoHanded = ref(true)

  function setSearchQuery(query: string) {
    searchQuery.value = query
  }

  // Process all weapons on component initialization
  const allWeaponArrays = [
    weaponsThrustingShields,
    weaponsGreatshields,
    weaponsMediumShields,
    weaponsSmallShields,
    weaponsTorches,
    weaponsSacredSeals,
    weaponsStaves,
    weaponsBallista,
    weaponsCrossbows,
    weaponsGreatbows,
    weaponsBows,
    weaponsLightBows,
    weaponsPerfumeBottles,
    weaponsBeastClaws,
    weaponsClaws,
    weaponsHandToHand,
    weaponsFists,
    weaponsWhips,
    weaponsReapers,
    weaponsHalberds,
    weaponsGreatSpears,
    weaponsSpears,
    weaponsColossalWeapons,
    weaponsGreatHammers,
    weaponsFlails,
    weaponsHammers,
    weaponsGreataxes,
    weaponsAxes,
    weaponsTwinblades,
    weaponsGreatKatanas,
    weaponsKatanas,
    weaponsBackhandBlades,
    weaponsCurvedGreatswords,
    weaponsCurvedSwords,
    weaponsHeavyThrustingSwords,
    weaponsThrustingSwords,
    weaponsColossalSwords,
    weaponsGreatswords,
    weaponsLightGreatswords,
    weaponsStraightSwords,
    weaponsDaggers,
    weaponsThrowingBlades,
  ]

  const weapons = ref(
    allWeaponArrays.flat().map((weapon: ScrapedWeapon, index: number) => {
      // Handle different attribute formats from the scraped data
      let strengthOneHand = 0
      let strengthTwoHand = 0
      let dexterity = 0
      let intelligence = 0
      let faith = 0
      let arcane = 0

      if (weapon.attributes) {
        if (weapon.attributes.strength) {
          // Handle the new format with one_hand/two_hand structure
          strengthOneHand = weapon.attributes.strength.one_hand || 0
          strengthTwoHand = weapon.attributes.strength.two_hand || 0
        }
        dexterity = weapon.attributes.dexterity || 0
        intelligence = weapon.attributes.intelligence || 0
        faith = weapon.attributes.faith || 0
        arcane = weapon.attributes.arcane || 0
      }

      return {
        id: weapon.weapon_name || `weapon-${index}`,
        name: weapon.weapon_name || 'Unknown Weapon',
        image: weapon.image?.src || '',
        category: weapon.weapon_type || '',
        attack: {
          physical: 0,
          magic: 0,
          fire: 0,
          lightning: 0,
          holy: 0,
          critical: 0,
        },
        requiredAttributes: {
          strengthOneHand,
          strengthTwoHand,
          dexterity,
          intelligence,
          faith,
          arcane,
        },
        wikiGGLink: weapon.wikiGGLink || '',
        wikiFextralifeLink: weapon.wikiFextralifeLink || '',
      }
    }),
  )

  const totalPages = computed(() => {
    return Math.ceil(filteredWeapons.value.length / itemsPerPage.value)
  })

  const filteredWeapons = computed(() => {
    return weapons.value.filter((weapon) => {
      // Check if weapon name contains the search query
      const matchesSearch = weapon.name.toLowerCase().includes(searchQuery.value.toLowerCase())

      // Check if weapon type is selected (if no types selected, show all)
      const matchesWeaponType = selectedWeaponTypes.value.length === 0 ||
        selectedWeaponTypes.value.includes(weapon.category)

      // Check if weapon stats are less than or equal to current stats
      const meetsRequirements =
        (
          accountForTwoHanded.value
            ? weapon.requiredAttributes.strengthTwoHand <= strength.value
            : weapon.requiredAttributes.strengthOneHand <= strength.value
        ) &&
        weapon.requiredAttributes.dexterity <= dexterity.value &&
        weapon.requiredAttributes.intelligence <= intelligence.value &&
        weapon.requiredAttributes.faith <= faith.value &&
        weapon.requiredAttributes.arcane <= arcane.value

      return matchesSearch && matchesWeaponType && meetsRequirements
    })
  })

  // Watch for changes and update localStorage
  watch(strength, (newValue) => {
    localStorage.setItem('stats.strength', newValue.toString())
    page.value = 1
  })

  watch(dexterity, (newValue) => {
    localStorage.setItem('stats.dexterity', newValue.toString())
    page.value = 1
  })

  watch(intelligence, (newValue) => {
    localStorage.setItem('stats.intelligence', newValue.toString())
    page.value = 1
  })

  watch(faith, (newValue) => {
    localStorage.setItem('stats.faith', newValue.toString())
    page.value = 1
  })

  watch(arcane, (newValue) => {
    localStorage.setItem('stats.arcane', newValue.toString())
    page.value = 1
  })

  return {
    strength,
    dexterity,
    intelligence,
    faith,
    arcane,
    page,
    itemsPerPage,
    searchQuery,
    setSearchQuery,
    totalPages,
    filteredWeapons,
    accountForTwoHanded,
    weaponTypes,
    selectedWeaponTypes,
  }
})
