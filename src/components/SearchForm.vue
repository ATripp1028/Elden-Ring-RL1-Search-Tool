<script setup lang="ts">
import { useStatsStore, useFiltersStore, usePaginationStore, useWeaponsStore } from '../stores'
import { ref, watch } from 'vue'
import BaseMultiSelect from './base/BaseMultiSelect.vue'
import { DataType } from '../model/types'

const statsStore = useStatsStore()
const filtersStore = useFiltersStore()
const paginationStore = usePaginationStore()
const weaponsStore = useWeaponsStore()

// Data type selection
const dataTypeSelection = ref<string[]>([DataType.WeaponsOnly])

// Watch for data type changes and update the store
watch(
  dataTypeSelection,
  (newValue) => {
    // Ensure only one item is selected at a time
    if (newValue.length > 1) {
      dataTypeSelection.value = [newValue[newValue.length - 1]]
      return
    }

    if (newValue.length > 0) {
      filtersStore.selectedDataType = newValue[0] as DataType
      paginationStore.resetPage()
    }
  },
  { immediate: true },
)

const showTwoHandedTooltip = ref(false)
const showDlcTooltip = ref(false)
const showHideShieldsTooltip = ref(false)

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

const toggleHideShieldsTooltip = () => {
  showHideShieldsTooltip.value = !showHideShieldsTooltip.value
  showDlcTooltip.value = false // Close other tooltip
}

const toggleIgnoreStats = () => {
  // v-model already updated statsStore.ignoreStats; just reset pagination
  paginationStore.resetPage()
}

const showBuildModeTooltip = ref(false)
const toggleBuildModeTooltip = () => {
  showBuildModeTooltip.value = !showBuildModeTooltip.value
  // Close other tooltips for consistency
  showTwoHandedTooltip.value = false
  showDlcTooltip.value = false
}
</script>

<template>
  <div class="search-form">
    <h1 class="title">Elden Ring RL1 Search Tool</h1>
    <p class="subtitle">Enter stats to see what your options are.</p>

    <div class="form-group">
      <label>Data Type</label>
      <BaseMultiSelect
        :options="['Weapons Only', 'Spells Only', 'Both']"
        v-model:selected-items="dataTypeSelection"
        placeholder="Select data type..."
        :prevent-deselection-of-last="true"
      />
    </div>

    <div class="form-group">
      <div class="checkbox-line">
        <label for="ignoreStatsCheckbox" class="checkbox-label">Ignore Stats</label>
        <div class="checkbox-with-help">
          <input
            type="checkbox"
            id="ignoreStatsCheckbox"
            v-model="statsStore.ignoreStats"
            @change="toggleIgnoreStats"
            style="width: auto"
          />
          <button
            type="button"
            class="help-button"
            @click="toggleBuildModeTooltip"
            :class="{ active: showBuildModeTooltip }"
            aria-label="Ignore Stats info"
          >
            ?
          </button>
        </div>
      </div>
      <div v-if="showBuildModeTooltip" class="tooltip-bubble">
        Toggle to ignore stats and search all other filters
      </div>
    </div>
    <div class="form-group" :class="{ disabled: statsStore.ignoreStats }">
      <label for="field1">Strength</label>
      <input
        type="number"
        id="field1"
        v-model="statsStore.strength"
        :disabled="statsStore.ignoreStats"
        placeholder="Enter Strength"
      />
    </div>

    <div class="form-group" :class="{ disabled: statsStore.ignoreStats }">
      <label for="field2">Dexterity</label>
      <input
        type="number"
        id="field2"
        v-model="statsStore.dexterity"
        :disabled="statsStore.ignoreStats"
        placeholder="Enter Dexterity"
      />
    </div>

    <div class="form-group" :class="{ disabled: statsStore.ignoreStats }">
      <label for="field3">Intelligence</label>
      <input
        type="number"
        id="field3"
        v-model="statsStore.intelligence"
        :disabled="statsStore.ignoreStats"
        placeholder="Enter Intelligence"
      />
    </div>

    <div class="form-group" :class="{ disabled: statsStore.ignoreStats }">
      <label for="field4">Faith</label>
      <input
        type="number"
        id="field4"
        v-model="statsStore.faith"
        :disabled="statsStore.ignoreStats"
        placeholder="Enter Faith"
      />
    </div>

    <div class="form-group" :class="{ disabled: statsStore.ignoreStats }">
      <label for="field5">Arcane</label>
      <input
        type="number"
        id="field5"
        v-model="statsStore.arcane"
        :disabled="statsStore.ignoreStats"
        placeholder="Enter Arcane"
      />
    </div>

    <div class="form-group" :class="{ disabled: statsStore.ignoreStats }">
      <div class="checkbox-line">
        <label for="field6" class="checkbox-label">Account for Two Hands</label>
        <div class="checkbox-with-help">
          <input
            type="checkbox"
            id="field6"
            v-model="statsStore.accountForTwoHanded"
            :disabled="statsStore.ignoreStats"
            style="width: auto"
          />
          <button
            type="button"
            class="help-button"
            @click="toggleTwoHandedTooltip"
            :class="{ active: showTwoHandedTooltip }"
            :disabled="statsStore.ignoreStats"
          >
            ?
          </button>
        </div>
      </div>
      <div v-if="showTwoHandedTooltip && !statsStore.ignoreStats" class="tooltip-bubble">
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

    <div class="form-group">
      <div class="checkbox-line">
        <label for="dlcCheckbox" class="checkbox-label">Hide Shields</label>
        <div class="checkbox-with-help">
          <input
            type="checkbox"
            id="hideShieldsCheckbox"
            v-model="filtersStore.hideShields"
            style="width: auto"
          />
          <button
            type="button"
            class="help-button"
            @click="toggleHideShieldsTooltip"
            :class="{ active: showHideShieldsTooltip }"
          >
            ?
          </button>
        </div>
      </div>
      <div v-if="showHideShieldsTooltip" class="tooltip-bubble">
        If checked, shields will be hidden from the results.
      </div>
    </div>

    <div class="form-group">
      <label>Filter by Type</label>
      <BaseMultiSelect
        :options="filtersStore.filteredWeaponTypes"
        v-model:selected-items="filtersStore.selectedWeaponTypes"
        placeholder="Select Weapon Types..."
      />
    </div>

    <div class="form-group">
      <label>Filter by Damage Type</label>
      <BaseMultiSelect
        :options="weaponsStore.damageTypes"
        v-model:selected-items="filtersStore.selectedDamageTypes"
        placeholder="Select Damage Types..."
      />
    </div>

    <div class="form-group">
      <label>Filter by Attack Type</label>
      <BaseMultiSelect
        :options="weaponsStore.attackTypes"
        v-model:selected-items="filtersStore.selectedAttackTypes"
        placeholder="Select Attack Types..."
      />
    </div>

    <div class="form-group">
      <label>Filter by Status Buildups</label>
      <BaseMultiSelect
        :options="weaponsStore.statusBuildups"
        v-model:selected-items="filtersStore.selectedStatusBuildups"
        placeholder="Select Status Buildups..."
      />
    </div>

    <button @click="resetStats" :disabled="statsStore.ignoreStats">Reset</button>
    <p class="made-by">Made by MrSporkMan</p>
  </div>
</template>

<style scoped>
.search-form {
  width: 100%;
  padding: var(--space-xl);
  background-color: var(--color-sidebar-bg);
  height: 100vh;
  position: sticky;
  left: 0;
  top: 0;
  box-shadow: var(--color-sidebar-shadow);
  overflow-y: auto;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: var(--color-text-primary);
  margin-top: var(--space-2xl);
}

.subtitle {
  text-align: center;
  font-size: 16px;
  color: var(--color-text-secondary);
}

.form-group {
  margin-bottom: 20px;
}

.form-group.disabled {
  opacity: 0.6;
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
  margin-bottom: var(--space-xs);
  font-weight: 500;
  color: var(--color-text-primary);
}

input {
  width: 100%;
  padding: var(--space-sm);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-small);
  font-size: 14px;
  background-color: var(--color-bg-elevated);
  color: var(--color-text-primary);
  transition: var(--transition-fast);
}

input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-focus-ring);
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
  color: var(--color-text-muted);
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

/* Switch styles */
.switch-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.switch-text {
  display: flex;
  flex-direction: column;
}

.switch-title {
  font-weight: 600;
  color: #333;
}

.switch-subtitle {
  font-size: 12px;
  color: #666;
}

.switch-with-help {
  display: flex;
  align-items: center;
  gap: 8px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.2s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: '';
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.2s;
  border-radius: 50%;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

input:checked + .slider {
  background-color: #4caf50;
}

input:focus + .slider {
  box-shadow: 0 0 1px #4caf50;
}

input:checked + .slider:before {
  transform: translateX(12px);
}
</style>
