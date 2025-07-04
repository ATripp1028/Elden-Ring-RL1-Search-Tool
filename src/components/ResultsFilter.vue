<script setup lang="ts">
import { useStatsStore } from '../stores/stats'

const stats = useStatsStore()
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
    <div class="filter-row"></div>
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
  position: sticky;
  top: 0;
  z-index: 1;
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
</style>
