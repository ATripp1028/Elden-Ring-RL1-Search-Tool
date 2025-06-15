<script setup lang="ts">
import { useFilterStore } from '../stores/filter'

const filter = useFilterStore()
</script>

<template>
  <div class="results-filter">
    <div class="filter-group">
      <label for="filter1">Search Results</label>
      <input type="text" id="filter1" v-model="filter.searchQuery" placeholder="Filter...">
    </div>
  </div>
</template>

<style scoped>
.results-filter {
  display: flex;
  gap: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
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
