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

export const useWeaponsStore = defineStore('weapons', () => {
  const weapons = ref<Weapon[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const currentPage = ref(1)
  const itemsPerPage = ref(10)
  const totalItems = ref(0)

  async function fetchWeapons() {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(
        `https://eldenring.fanapis.com/api/weapons?limit=${itemsPerPage.value}&page=${currentPage.value}`
      )
      const data = await response.json()
      
      if (data.success) {
        weapons.value = data.data.map((weapon: any) => ({
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
            strength: weapon.requiredAttributes?.strength || 0,
            dexterity: weapon.requiredAttributes?.dexterity || 0,
            intelligence: weapon.requiredAttributes?.intelligence || 0,
            faith: weapon.requiredAttributes?.faith || 0,
            arcane: weapon.requiredAttributes?.arcane || 0
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
        }))
        totalItems.value = data.count || 0
      } else {
        throw new Error('Failed to fetch weapons')
      }
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'An error occurred while fetching weapons'
    } finally {
      loading.value = false
    }
  }

  function setItemsPerPage(value: number) {
    itemsPerPage.value = value
    currentPage.value = 1 // Reset to first page when changing items per page
    fetchWeapons()
  }

  function setPage(page: number) {
    currentPage.value = page
    fetchWeapons()
  }

  return {
    weapons,
    loading,
    error,
    currentPage,
    itemsPerPage,
    totalItems,
    fetchWeapons,
    setItemsPerPage,
    setPage
  }
})
