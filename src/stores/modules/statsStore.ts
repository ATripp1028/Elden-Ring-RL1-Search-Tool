import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { getStoredValue } from '../../model/utils'

export const useStatsStore = defineStore('stats', () => {
  // Character stats
  const strength = ref(getStoredValue('stats.strength', 10))
  const dexterity = ref(getStoredValue('stats.dexterity', 10))
  const intelligence = ref(getStoredValue('stats.intelligence', 10))
  const faith = ref(getStoredValue('stats.faith', 10))
  const arcane = ref(getStoredValue('stats.arcane', 10))

  // Settings
  const accountForTwoHanded = ref(true)
  const ignoreStats = ref(localStorage.getItem('stats.ignoreStats') === 'true')

  const resetStats = () => {
    strength.value = 10
    dexterity.value = 10
    intelligence.value = 10
    faith.value = 10
    arcane.value = 10
  }

  // Watch for changes and update localStorage
  watch(strength, (newValue) => {
    localStorage.setItem('stats.strength', newValue.toString())
  })

  watch(dexterity, (newValue) => {
    localStorage.setItem('stats.dexterity', newValue.toString())
  })

  watch(intelligence, (newValue) => {
    localStorage.setItem('stats.intelligence', newValue.toString())
  })

  watch(faith, (newValue) => {
    localStorage.setItem('stats.faith', newValue.toString())
  })

  watch(arcane, (newValue) => {
    localStorage.setItem('stats.arcane', newValue.toString())
  })

  // Persist settings
  watch(ignoreStats, (newValue) => {
    localStorage.setItem('stats.ignoreStats', newValue.toString())
  })

  return {
    strength,
    dexterity,
    intelligence,
    faith,
    arcane,
    accountForTwoHanded,
    ignoreStats,
    resetStats,
  }
})
