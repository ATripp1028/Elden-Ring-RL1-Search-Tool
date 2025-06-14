import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useStatsStore = defineStore('stats', () => {
  const strength = ref(10)
  const dexterity = ref(10)
  const intelligence = ref(10)
  const faith = ref(10)
  const arcane = ref(10)

  function setStrength(value: number) {
    strength.value = value
  }

  function setDexterity(value: number) {
    dexterity.value = value
  }

  function setIntelligence(value: number) {
    intelligence.value = value
  }

  function setFaith(value: number) {
    faith.value = value
  }

  function setArcane(value: number) {
    arcane.value = value
  }

  return {
    strength,
    dexterity,
    intelligence,
    faith,
    arcane,
    setStrength,
    setDexterity,
    setIntelligence,
    setFaith,
    setArcane
  }
}) 