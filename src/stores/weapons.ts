import { defineStore } from 'pinia'
import { ref } from 'vue'

interface WeaponStats {
  strength: number
  dexterity: number
  intelligence: number
  faith: number
  arcane: number
}

interface Weapon {
  id: string
  name: string
  image: string
  description: string
  category: string
  weight: number
  attack: {
    physical: number
    magic: number
    fire: number
    lightning: number
    holy: number
    critical: number
  }
  defence: {
    physical: number
    magic: number
    fire: number
    lightning: number
    holy: number
    boost: number
  }
  requiredAttributes: WeaponStats
  scalesWith: WeaponStats
  wikiGGLink: string
  wikiFextralifeLink: string
}

interface ScrapedWeapon {
  weapon_name: string
  weapon_type: string
  attributes?: {
    strength?: number | { one_hand: number; two_hand: number }
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

// Import all weapon JSON files
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

const CACHE_KEY = 'elden-ring-weapons-cache'

export const useWeaponsStore = defineStore('weapons', () => {
  const weapons = ref<Weapon[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  function loadFromCache(): boolean {
    try {
      const cachedData = localStorage.getItem(CACHE_KEY)
      if (!cachedData) return false

      weapons.value = JSON.parse(cachedData)
      return true
    } catch (e) {
      console.error('Error loading weapons from cache:', e)
      return false
    }
  }

  function saveToCache(weaponsData: Weapon[]) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify(weaponsData))
    } catch (e) {
      console.error('Error saving weapons to cache:', e)
    }
  }

    async function fetchWeapons() {
    // Try to load from cache first
    if (loadFromCache()) {
      return
    }

    loading.value = true
    error.value = null

    try {
      // Combine all weapon arrays from the imported JSON files
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
        weaponsThrowingBlades
      ]

      // Flatten all arrays and process each weapon
      const processedWeapons = allWeaponArrays.flat().map((weapon: ScrapedWeapon, index: number) => {
        // Handle different attribute formats from the scraped data
        let strength = 0
        let dexterity = 0
        let intelligence = 0
        let faith = 0
        let arcane = 0

        if (weapon.attributes) {
          if (weapon.attributes.strength) {
            // Handle the new format with one_hand/two_hand structure
            if (typeof weapon.attributes.strength === 'object') {
              strength = weapon.attributes.strength.one_hand || 0
            } else {
              strength = weapon.attributes.strength || 0
            }
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
          description: weapon.weapon_type || '',
          category: weapon.weapon_type || '',
          weight: 0, // Not available in scraped data
          attack: {
            physical: 0,
            magic: 0,
            fire: 0,
            lightning: 0,
            holy: 0,
            critical: 0
          },
          defence: {
            physical: 0,
            magic: 0,
            fire: 0,
            lightning: 0,
            holy: 0,
            boost: 0
          },
          requiredAttributes: {
            strength,
            dexterity,
            intelligence,
            faith,
            arcane
          },
          scalesWith: {
            strength: 0,
            dexterity: 0,
            intelligence: 0,
            faith: 0,
            arcane: 0
          },
          wikiGGLink: weapon.wikiGGLink || '',
          wikiFextralifeLink: weapon.wikiFextralifeLink || ''
        }
      })

      weapons.value = processedWeapons
      saveToCache(processedWeapons)
      console.log(`Loaded ${processedWeapons.length} weapons from local JSON files`)
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'An error occurred while loading weapons'
    } finally {
      loading.value = false
    }
  }

  return {
    weapons,
    loading,
    error,
    fetchWeapons
  }
})
