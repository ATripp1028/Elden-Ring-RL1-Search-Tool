<script setup lang="ts">
import { useStatsStore } from '../stores/stats'
import { ref, onMounted, onUnmounted } from 'vue'

const stats = useStatsStore()

// Multiselect state
const isOpen = ref(false)
const multiselectRef = ref<HTMLDivElement>()
const isDamageTypeOpen = ref(false)
const damageTypeMultiselectRef = ref<HTMLDivElement>()
const isColumnOpen = ref(false)
const columnMultiselectRef = ref<HTMLDivElement>()

const toggleOption = (option: string) => {
  const index = stats.selectedWeaponTypes.indexOf(option)
  if (index > -1) {
    stats.selectedWeaponTypes.splice(index, 1)
  } else {
    stats.selectedWeaponTypes.push(option)
  }
}

const isSelected = (option: string) => {
  return stats.selectedWeaponTypes.includes(option)
}

const toggleDamageTypeOption = (option: string) => {
  const index = stats.selectedDamageTypes.indexOf(option)
  if (index > -1) {
    stats.selectedDamageTypes.splice(index, 1)
  } else {
    stats.selectedDamageTypes.push(option)
  }
}

const isDamageTypeSelected = (option: string) => {
  return stats.selectedDamageTypes.includes(option)
}

const toggleColumnOption = (option: string) => {
  // Prevent deselecting the last column - ensure at least one is always selected
  if (stats.selectedColumns.includes(option) && stats.selectedColumns.length === 1) {
    return
  }

  const index = stats.selectedColumns.indexOf(option)
  if (index > -1) {
    stats.selectedColumns.splice(index, 1)
  } else {
    stats.selectedColumns.push(option)
  }
}

const isColumnSelected = (option: string) => {
  return stats.selectedColumns.includes(option)
}

const handleClickOutside = (event: Event) => {
  if (multiselectRef.value && !multiselectRef.value.contains(event.target as Node)) {
    isOpen.value = false
  }
  if (
    damageTypeMultiselectRef.value &&
    !damageTypeMultiselectRef.value.contains(event.target as Node)
  ) {
    isDamageTypeOpen.value = false
  }
  if (columnMultiselectRef.value && !columnMultiselectRef.value.contains(event.target as Node)) {
    isColumnOpen.value = false
  }
}

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    isOpen.value = false
    isDamageTypeOpen.value = false
    isColumnOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <div class="results-filter">
    <div class="filter-row">
      <div class="filter-group">
        <label for="filter1">Search Results</label>
        <input type="text" id="filter1" v-model="stats.searchQuery" placeholder="Filter..." />
      </div>
      <div class="page-navigation">
        <div class="result-count">
          {{ stats.filteredWeapons.length }} weapon{{
            stats.filteredWeapons.length !== 1 ? 's' : ''
          }}
          found
        </div>
        <div class="items-per-page">
          <label for="itemsPerPage">Items per page:</label>
          <select
            id="itemsPerPage"
            :value="stats.itemsPerPage"
            @change="
              (e: Event) => (stats.itemsPerPage = Number((e.target as HTMLSelectElement).value))
            "
          >
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="40">40</option>
          </select>
        </div>
        <button :disabled="stats.page === 1" @click="stats.page = 1">First</button>
        <button :disabled="stats.page === 1" @click="stats.page--">Previous</button>
        <span class="page-number">Page {{ stats.page }} of {{ stats.totalPages }}</span>
        <button :disabled="stats.page >= stats.totalPages" @click="stats.page++">Next</button>
        <button :disabled="stats.page >= stats.totalPages" @click="stats.page = stats.totalPages">
          Last
        </button>
      </div>
    </div>
    <div class="filter-row">
      <div class="filter-group">
        <label>Filter by Type</label>
        <div class="multiselect" ref="multiselectRef">
          <div class="multiselect-trigger" @click="isOpen = !isOpen" :class="{ open: isOpen }">
            <span class="multiselect-display">
              {{
                stats.selectedWeaponTypes.length > 0
                  ? `${stats.selectedWeaponTypes.length} selected`
                  : 'Select Weapon Types...'
              }}
            </span>
            <span class="multiselect-arrow">▼</span>
          </div>
          <div class="multiselect-dropdown" v-if="isOpen">
            <div class="multiselect-options">
              <div
                v-for="option in stats.weaponTypes"
                :key="option"
                class="multiselect-option"
                :class="{ selected: isSelected(option) }"
                @click="toggleOption(option)"
              >
                <span class="checkbox">{{ isSelected(option) ? '✓' : '' }}</span>
                <span class="option-text">{{ option }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="filter-group">
        <label>Filter by Damage Type</label>
        <div class="multiselect" ref="damageTypeMultiselectRef">
          <div
            class="multiselect-trigger"
            @click="isDamageTypeOpen = !isDamageTypeOpen"
            :class="{ open: isDamageTypeOpen }"
          >
            <span class="multiselect-display">
              {{
                stats.selectedDamageTypes.length > 0
                  ? `${stats.selectedDamageTypes.length} selected`
                  : 'Select Damage Types...'
              }}
            </span>
            <span class="multiselect-arrow">▼</span>
          </div>
          <div class="multiselect-dropdown" v-if="isDamageTypeOpen">
            <div class="multiselect-options">
              <div
                v-for="option in stats.damageTypes"
                :key="option"
                class="multiselect-option"
                :class="{ selected: isDamageTypeSelected(option) }"
                @click="toggleDamageTypeOption(option)"
              >
                <span class="checkbox">{{ isDamageTypeSelected(option) ? '✓' : '' }}</span>
                <span class="option-text">{{ option }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="filter-group">
        <label>Show Columns</label>
        <div class="multiselect" ref="columnMultiselectRef">
          <div
            class="multiselect-trigger"
            @click="isColumnOpen = !isColumnOpen"
            :class="{ open: isColumnOpen }"
          >
            <span class="multiselect-display">
              {{
                stats.selectedColumns.length > 0
                  ? `${stats.selectedColumns.length} selected`
                  : 'Select Columns...'
              }}
            </span>
            <span class="multiselect-arrow">▼</span>
          </div>
          <div class="multiselect-dropdown" v-if="isColumnOpen">
            <div class="multiselect-options">
              <div
                v-for="option in stats.availableColumns"
                :key="option"
                class="multiselect-option"
                :class="{ selected: isColumnSelected(option) }"
                @click="toggleColumnOption(option)"
              >
                <span class="checkbox">{{ isColumnSelected(option) ? '✓' : '' }}</span>
                <span class="option-text">{{ option }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.results-filter {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 15px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
  width: 100%;
  flex-shrink: 0;
}

.filter-row {
  display: flex;
  gap: 20px;
  align-items: center;
  width: 100%;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.pagination-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.items-per-page select {
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.result-count {
  font-weight: 500;
  color: #666;
}

.page-navigation {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-navigation button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
}

.page-navigation button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-navigation button:hover:not(:disabled) {
  background-color: #f5f5f5;
}

label {
  font-weight: 500;
  color: #333;
  white-space: nowrap;
  flex-shrink: 0;
}

input,
select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  flex: 1;
  min-width: 0;
}

input:focus,
select:focus {
  outline: none;
  border-color: #666;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.1);
}

.page-number {
  font-weight: 500;
  color: #666;
}

.multiselect {
  position: relative;
  flex: 1;
  min-width: 0;
}

.multiselect-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  font-size: 14px;
  min-height: 32px;
}

.multiselect-trigger:hover {
  border-color: #666;
}

.multiselect-trigger.open {
  border-color: #666;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.1);
}

.multiselect-display {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #666;
}

.multiselect-arrow {
  font-size: 10px;
  color: #666;
  transition: transform 0.2s;
  margin-left: 8px;
}

.multiselect-trigger.open .multiselect-arrow {
  transform: rotate(180deg);
}

.multiselect-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 30;
  max-height: 200px;
  overflow-y: auto;
}

.multiselect-options {
  padding: 4px 0;
}

.multiselect-option {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.multiselect-option:hover {
  background-color: #f5f5f5;
}

.multiselect-option.selected {
  background-color: #e3f2fd;
}

.checkbox {
  width: 16px;
  height: 16px;
  border: 1px solid #ddd;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  font-size: 12px;
  color: #2196f3;
  background-color: white;
}

.multiselect-option.selected .checkbox {
  background-color: #2196f3;
  border-color: #2196f3;
  color: white;
}

.option-text {
  flex: 1;
  color: #666;
}
</style>
