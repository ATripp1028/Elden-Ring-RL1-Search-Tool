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
      const response = await fetch(
        `https://eldenring.fanapis.com/api/weapons?limit=400`
      )
      const data = await response.json()
      
      if (data.success && data.data.length > 0) {
        const processedWeapons = data.data.map((weapon: any) => {
            const requiredAttributes = weapon.requiredAttributes
            const requiredAttributesObject = {
                strength: 0,
                dexterity: 0,
                intelligence: 0,
                faith: 0,
                arcane: 0
            }
            requiredAttributes.forEach((stat: any) => {
                if (stat.name === 'Str') {
                    requiredAttributesObject.strength = stat.amount
                } else if (stat.name === 'Dex') {
                    requiredAttributesObject.dexterity = stat.amount
                } else if (stat.name === 'Int') {
                    requiredAttributesObject.intelligence = stat.amount
                } else if (stat.name === 'Fai') {
                    requiredAttributesObject.faith = stat.amount
                } else if (stat.name === 'Arc') {
                    requiredAttributesObject.arcane = stat.amount
                }
            })
            return {
                id: weapon.id,
                name: weapon.name,
                image: weapon.image,
                description: weapon.description,
                category: weapon.category,
                weight: weapon.weight,
                attack: {
                    physical: weapon.attack?.physical || 0,
                    magic: weapon.attack?.magic || 0,
                    fire: weapon.attack?.fire || 0,
                    lightning: weapon.attack?.lightning || 0,
                    holy: weapon.attack?.holy || 0,
                    critical: weapon.attack?.critical || 0
                },
                defence: {
                    physical: weapon.defence?.physical || 0,
                    magic: weapon.defence?.magic || 0,
                    fire: weapon.defence?.fire || 0,
                    lightning: weapon.defence?.lightning || 0,
                    holy: weapon.defence?.holy || 0,
                    boost: weapon.defence?.boost || 0
                },
                requiredAttributes: {
                    strength: requiredAttributesObject.strength || 0,
                    dexterity: requiredAttributesObject.dexterity || 0,
                    intelligence: requiredAttributesObject.intelligence || 0,
                    faith: requiredAttributesObject.faith || 0,
                    arcane: requiredAttributesObject.arcane || 0
                },
                scalesWith: {
                    strength: weapon.scalesWith?.strength || 0,
                    dexterity: weapon.scalesWith?.dexterity || 0,
                    intelligence: weapon.scalesWith?.intelligence || 0,
                    faith: weapon.scalesWith?.faith || 0,
                    arcane: weapon.scalesWith?.arcane || 0
                },
                wikiGGLink: `https://eldenring.wiki.gg/wiki/${weapon.name.replace(/\s+/g, '_')}`,
                wikiFextralifeLink: `https://eldenring.wiki.fextralife.com/${weapon.name.replace(/\s+/g, '+')}`
            }
        })
        
        weapons.value = processedWeapons
        saveToCache(processedWeapons)
      } else {
        throw new Error('Failed to fetch weapons')
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'An error occurred while fetching weapons'
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
