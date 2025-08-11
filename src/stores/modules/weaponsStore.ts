import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loadWeaponsData } from '../../utils/weaponDataLoader'
import type { Weapon } from '../../model/types'

export interface ProcessedWeapon {
  id: string
  name: string
  image?: string
  category: string
  attack: {
    physical: number
    magic: number
    fire: number
    lightning: number
    holy: number
    critical: number
  }
  requiredAttributes: {
    strengthOneHand: number
    strengthTwoHand: number
    dexterity: number
    intelligence: number
    faith: number
    arcane: number
  }
  wikiGGLink: string
  wikiFextralifeLink: string
  damageTypes: {
    major: string
    minor: string[]
  }
  attackTypes: {
    primary: string
    secondary: string
  }
  statusBuildup: string
  dlcExclusive: boolean
}

export const useWeaponsStore = defineStore('weapons', () => {
  const weapons = ref<ProcessedWeapon[]>([])

  // Weapon metadata
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

  const damageTypes = ['Physical', 'Fire', 'Lightning', 'Holy', 'Magic']

  // Primary/secondary attack type options
  const attackTypes = ['Standard', 'Slash', 'Strike', 'Pierce']

  // Initialize weapons data
  const initializeWeapons = () => {
    const allWeaponArrays = loadWeaponsData()

    weapons.value = (allWeaponArrays.flat() as Weapon[]).map((weapon: Weapon) => {
      let strengthOneHand = 0
      let strengthTwoHand = 0
      let dexterity = 0
      let intelligence = 0
      let faith = 0
      let arcane = 0

      if (weapon.attributes) {
        if (weapon.attributes.strength) {
          strengthOneHand = weapon.attributes.strength.one_hand || 0
          strengthTwoHand = weapon.attributes.strength.two_hand || 0
        }
        dexterity = weapon.attributes.dexterity || 0
        intelligence = weapon.attributes.intelligence || 0
        faith = weapon.attributes.faith || 0
        arcane = weapon.attributes.arcane || 0
      }

      return {
        id: weapon.weapon_name,
        name: weapon.weapon_name,
        image: weapon.image?.src,
        category: weapon.weapon_type,
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
        wikiGGLink: weapon.wikiGGLink,
        wikiFextralifeLink: weapon.wikiFextralifeLink,
        damageTypes: weapon.damage_types,
        attackTypes: weapon.attack_types,
        statusBuildup: weapon.status_buildup,
        dlcExclusive: weapon.dlc_exclusive,
      }
    })
  }

  // Initialize weapons on store creation
  initializeWeapons()

  return {
    weapons: computed(() => weapons.value),
    weaponTypes,
    damageTypes,
    attackTypes,
  }
})
