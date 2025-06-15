<script setup lang="ts">
import { useStatsStore } from '../stores/stats'
import { useFilterStore } from '../stores/filter'

const stats = useStatsStore()
const filter = useFilterStore()
</script>

<template>
  <div class="search-form">
    <div class="form-group">
      <label for="field1">Strength</label>
      <input type="number" id="field1" v-model="stats.strength" placeholder="Enter Strength">
    </div>
    
    <div class="form-group">
      <label for="field2">Dexterity</label>
      <input type="number" id="field2" v-model="stats.dexterity" placeholder="Enter Dexterity">
    </div>
    
    <div class="form-group">
      <label for="field3">Intelligence</label>
      <input type="number" id="field3" v-model="stats.intelligence" placeholder="Enter Intelligence">
    </div>
    
    <div class="form-group">
      <label for="field4">Faith</label>
      <input type="number" id="field4" v-model="stats.faith" placeholder="Enter Faith">
    </div>
    
    <div class="form-group">
      <label for="field5">Arcane</label>
      <input type="number" id="field5" v-model="stats.arcane" placeholder="Enter Arcane">
    </div>

    <div class="debug-section">
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
    </div>
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

.form-group {
  margin-bottom: 20px;
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
</style>
