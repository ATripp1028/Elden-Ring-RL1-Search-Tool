import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loadWeaponsData } from '../../utils/weaponDataLoader'
import { loadSpellsData } from '../../utils/spellDataLoader'
import type { Weapon, Spell } from '../../model/types'

export interface ProcessedItem {
  id: string
  name: string
  image?: string
  category: string
  type: 'weapon' | 'spell'
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
  // Combined, display- and filter-ready damage types.
  // If any elemental (non-Physical) types are present, Physical is excluded.
  trackedDamageTypes: string[]
  attackTypes: {
    primary: string
    secondary: string
  }
  statusBuildup: string
  dlcExclusive: boolean
}

// Keep backwards compatibility alias
export type ProcessedWeapon = ProcessedItem

export const useWeaponsStore = defineStore('weapons', () => {
  const weapons = ref<ProcessedItem[]>([])

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

  // Spell metadata
  const spellTypes = [
    'Sorcery',
    'Incantation'
  ]

  // Combined list of all types for filtering
  const allTypes = [...weaponTypes, ...spellTypes]

  const damageTypes = ['Physical', 'Fire', 'Lightning', 'Holy', 'Magic']

  // Primary/secondary attack type options
  const attackTypes = ['Standard', 'Slash', 'Strike', 'Pierce']

  // Status buildup options
  const statusBuildups = ['None', 'Blood Loss', 'Frostbite', 'Madness', 'Poison', 'Scarlet Rot', 'Sleep']

  // Initialize weapons and spells data
  const initializeWeapons = () => {
    const allWeaponArrays = loadWeaponsData()
    const allSpells = loadSpellsData()

    // Process weapons
    const processedWeapons = (allWeaponArrays.flat() as Weapon[]).map((weapon: Weapon) => {
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
        type: 'weapon' as const,
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
        trackedDamageTypes: (() => {
          // Remove damage types for staves and sacred seals
          if (weapon.weapon_type === 'Staves' || weapon.weapon_type === 'Sacred Seals') {
            return []
          }

          const major = weapon.damage_types?.major
          const minors = weapon.damage_types?.minor || []
          const allTypes = [major, ...minors].filter(Boolean) as string[]
          const hasElemental = allTypes.some((t) => t !== 'Physical')
          return hasElemental ? allTypes.filter((t) => t !== 'Physical') : ['Physical']
        })(),
        attackTypes: weapon.attack_types,
        statusBuildup: weapon.status_buildup,
        dlcExclusive: weapon.dlc_exclusive,
      }
    })

    // Process spells
    const processedSpells = allSpells.map((spell: Spell) => {
      return {
        id: spell.spell_name,
        name: spell.spell_name,
        image: spell.imageUrl,
        category: spell.spell_type,
        type: 'spell' as const,
        attack: {
          physical: 0,
          magic: 0,
          fire: 0,
          lightning: 0,
          holy: 0,
          critical: 0,
        },
        requiredAttributes: {
          strengthOneHand: 0,
          strengthTwoHand: 0,
          dexterity: 0,
          intelligence: spell.requirements.intelligence || 0,
          faith: spell.requirements.faith || 0,
          arcane: spell.requirements.arcane || 0,
        },
        wikiGGLink: spell.wikiGGLink,
        wikiFextralifeLink: spell.wikiFextralifeLink,
        damageTypes: {
          major: spell.damage_types.length > 0 ? spell.damage_types[0] : '',
          minor: spell.damage_types.slice(1)
        },
        trackedDamageTypes: spell.damage_types.length > 0 ? spell.damage_types : ['None'],
        attackTypes: {
          primary: 'None',
          secondary: 'None'
        },
        statusBuildup: spell.status_buildup || 'None',
        dlcExclusive: spell.dlc_exclusive,
      }
    })

    weapons.value = [...processedWeapons, ...processedSpells]
  }

  // Initialize weapons on store creation
  initializeWeapons()

  return {
    weapons: computed(() => weapons.value),
    weaponTypes,
    spellTypes,
    allTypes,
    damageTypes,
    attackTypes,
    statusBuildups,
  }
})
