<script setup lang="ts">
import { useFiltersStore, useWeaponsStore, useUIStore, usePaginationStore } from '../stores'
import BaseMultiSelect from './base/BaseMultiSelect.vue'
import BasePagination from './base/BasePagination.vue'

const filtersStore = useFiltersStore()
const weaponsStore = useWeaponsStore()
const uiStore = useUIStore()
const paginationStore = usePaginationStore()
</script>

<template>
  <div class="results-filter">
    <div class="filter-row">
      <div class="filter-group">
        <label for="filter1">Search Results</label>
        <input
          type="text"
          id="filter1"
          v-model="filtersStore.searchQuery"
          placeholder="Filter..."
        />
      </div>

      <div class="filter-group">
        <label>Show Columns</label>
        <BaseMultiSelect
          :options="uiStore.availableColumns"
          v-model:selected-items="uiStore.selectedColumns"
          placeholder="Select Columns..."
          :prevent-deselection-of-last="true"
        />
      </div>

      <BasePagination
        v-model:current-page="paginationStore.page"
        v-model:items-per-page="paginationStore.itemsPerPage"
        :total-pages="paginationStore.totalPages"
        :total-items="filtersStore.filteredWeapons.length"
      />
    </div>

    <div class="filter-row">
      <div class="filter-group">
        <label>Filter by Type</label>
        <BaseMultiSelect
          :options="filtersStore.filteredWeaponTypes"
          v-model:selected-items="filtersStore.selectedWeaponTypes"
          placeholder="Select Weapon Types..."
        />
      </div>

      <div class="filter-group">
        <label>Filter by Damage Type</label>
        <BaseMultiSelect
          :options="weaponsStore.damageTypes"
          v-model:selected-items="filtersStore.selectedDamageTypes"
          placeholder="Select Damage Types..."
        />
      </div>

      <div class="filter-group">
        <label>Filter by Attack Type</label>
        <BaseMultiSelect
          :options="weaponsStore.attackTypes"
          v-model:selected-items="filtersStore.selectedAttackTypes"
          placeholder="Select Attack Types..."
        />
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

label {
  font-weight: 500;
  color: #333;
  white-space: nowrap;
  flex-shrink: 0;
}

input {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  flex: 1;
  min-width: 0;
}

input:focus {
  outline: none;
  border-color: #666;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.1);
}
</style>
