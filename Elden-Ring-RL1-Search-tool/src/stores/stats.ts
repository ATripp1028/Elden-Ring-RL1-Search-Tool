import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { getStoredValue } from '../model/utils'

export const useStatsStore = defineStore('stats', () => {
  const strength = ref(getStoredValue('stats.strength', 10))
  const dexterity = ref(getStoredValue('stats.dexterity', 10))
  const intelligence = ref(getStoredValue('stats.intelligence', 10))
  const faith = ref(getStoredValue('stats.faith', 10))
  const arcane = ref(getStoredValue('stats.arcane', 10))

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

  return {
    strength,
    dexterity,
    intelligence,
    faith,
    arcane,
  }
}) 