<script setup lang="ts">
import { useStatsStore, useFiltersStore, usePaginationStore } from '../stores'
import { ref } from 'vue'

const statsStore = useStatsStore()
const filtersStore = useFiltersStore()
const paginationStore = usePaginationStore()

const showTwoHandedTooltip = ref(false)
const showDlcTooltip = ref(false)

const resetStats = () => {
  statsStore.resetStats()
  paginationStore.resetPage()
}

const toggleTwoHandedTooltip = () => {
  showTwoHandedTooltip.value = !showTwoHandedTooltip.value
  showDlcTooltip.value = false // Close other tooltip
}

const toggleDlcTooltip = () => {
  showDlcTooltip.value = !showDlcTooltip.value
  showTwoHandedTooltip.value = false // Close other tooltip
}
</script>

<template>
  <div class="search-form">
    <h1 class="title">Elden Ring RL1 Search Tool</h1>
    <p class="subtitle">Enter stats to see what your options are.</p>
    <div class="form-group">
      <label for="field1">Strength</label>
      <input type="number" id="field1" v-model="statsStore.strength" placeholder="Enter Strength" />
    </div>

    <div class="form-group">
      <label for="field2">Dexterity</label>
      <input
        type="number"
        id="field2"
        v-model="statsStore.dexterity"
        placeholder="Enter Dexterity"
      />
    </div>

    <div class="form-group">
      <label for="field3">Intelligence</label>
      <input
        type="number"
        id="field3"
        v-model="statsStore.intelligence"
        placeholder="Enter Intelligence"
      />
    </div>

    <div class="form-group">
      <label for="field4">Faith</label>
      <input type="number" id="field4" v-model="statsStore.faith" placeholder="Enter Faith" />
    </div>

    <div class="form-group">
      <label for="field5">Arcane</label>
      <input type="number" id="field5" v-model="statsStore.arcane" placeholder="Enter Arcane" />
    </div>

    <div class="form-group">
      <div class="checkbox-line">
        <label for="field6" class="checkbox-label">Account for Two Hands</label>
        <div class="checkbox-with-help">
          <input
            type="checkbox"
            id="field6"
            v-model="statsStore.accountForTwoHanded"
            style="width: auto"
          />
          <button
            type="button"
            class="help-button"
            @click="toggleTwoHandedTooltip"
            :class="{ active: showTwoHandedTooltip }"
          >
            ?
          </button>
        </div>
      </div>
      <div v-if="showTwoHandedTooltip" class="tooltip-bubble">
        If checked, the tool will query for weapons that can be effectively wielded with two hands
        for your desired strength. If unchecked, the tool will only compare against the in-game
        listed strength.
      </div>
    </div>

    <div class="form-group">
      <div class="checkbox-line">
        <label for="dlcCheckbox" class="checkbox-label">Include DLC Weapons</label>
        <div class="checkbox-with-help">
          <input
            type="checkbox"
            id="dlcCheckbox"
            v-model="filtersStore.showDlcWeapons"
            style="width: auto"
          />
          <button
            type="button"
            class="help-button"
            @click="toggleDlcTooltip"
            :class="{ active: showDlcTooltip }"
          >
            ?
          </button>
        </div>
      </div>
      <div v-if="showDlcTooltip" class="tooltip-bubble">
        If checked, weapons from the Shadow of the Erdtree DLC will be included in the results. If
        unchecked, only base game weapons will be shown.
      </div>
    </div>

    <button @click="resetStats">Reset</button>

    <!-- <div class="debug-section">
      <h3>Debug Info</h3>
      <pre>{{ JSON.stringify({
        stats: {
          strength: stats.strength,
          dexterity: stats.dexterity,
          intelligence: stats.intelligence,
          faith: stats.faith,
          arcane: stats.arcane
        },
        filter: {
          searchQuery: filter.searchQuery
        }
      }, null, 2) }}</pre>
    </div> -->
    <p class="made-by">Made by MrSporkMan</p>
  </div>
</template>

<style scoped>
.search-form {
  width: 100%;
  padding: 20px;
  background-color: #f5f5f5;
  height: 100vh;
  position: sticky;
  left: 0;
  top: 0;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.subtitle {
  text-align: center;
  font-size: 16px;
  color: #666;
}

.form-group {
  margin-bottom: 20px;
}

.checkbox-line {
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: space-between;
  gap: 8px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: #666;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.1);
}

.debug-section {
  margin-top: 30px;
  padding: 15px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.debug-section h3 {
  margin: 0 0 10px 0;
  color: #666;
  font-size: 14px;
}

.debug-section pre {
  margin: 0;
  font-size: 12px;
  color: #333;
  white-space: pre-wrap;
  word-break: break-all;
}

.made-by {
  text-align: center;
  font-size: 12px;
  color: #666;
}

.checkbox-label {
  font-size: 12px;
  width: 100%;
}

.checkbox-with-help {
  display: flex;
  align-items: center;
  gap: 8px;
}

.help-button {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  color: #666;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.help-button:hover {
  border-color: #999;
  background-color: #e9ecef;
  color: #333;
}

.help-button.active {
  border-color: #007bff;
  background-color: #007bff;
  color: white;
}

.tooltip-bubble {
  margin-top: 8px;
  padding: 10px 12px;
  background-color: #333;
  color: white;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.4;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.2s ease-in-out;
}

.tooltip-bubble::before {
  content: '';
  position: absolute;
  top: -6px;
  left: 20px;
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-bottom: 6px solid #333;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
