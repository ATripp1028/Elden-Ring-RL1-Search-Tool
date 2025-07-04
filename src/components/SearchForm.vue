<script setup lang="ts">
import { useStatsStore } from '../stores/stats'

const stats = useStatsStore()

const resetStats = () => {
  stats.strength = 10
  stats.dexterity = 10
  stats.intelligence = 10
  stats.faith = 10
  stats.arcane = 10
  stats.page = 1
}
</script>

<template>
  <div class="search-form">
    <h1 class="title">Elden Ring RL1 Search Tool</h1>
    <p class="subtitle">Enter stats to see what your options are.</p>
    <div class="form-group">
      <label for="field1">Strength</label>
      <input type="number" id="field1" v-model="stats.strength" placeholder="Enter Strength" />
    </div>

    <div class="form-group">
      <label for="field2">Dexterity</label>
      <input type="number" id="field2" v-model="stats.dexterity" placeholder="Enter Dexterity" />
    </div>

    <div class="form-group">
      <label for="field3">Intelligence</label>
      <input
        type="number"
        id="field3"
        v-model="stats.intelligence"
        placeholder="Enter Intelligence"
      />
    </div>

    <div class="form-group">
      <label for="field4">Faith</label>
      <input type="number" id="field4" v-model="stats.faith" placeholder="Enter Faith" />
    </div>

    <div class="form-group">
      <label for="field5">Arcane</label>
      <input type="number" id="field5" v-model="stats.arcane" placeholder="Enter Arcane" />
    </div>

    <div class="form-group">
      <div class="checkbox-line">
        <label for="field6" class="checkbox-label">Account for Two Hands</label>
        <input
          type="checkbox"
          id="field6"
          v-model="stats.accountForTwoHanded"
          style="width: auto"
        />
      </div>
      <p class="form-group-description">
        If checked, the tool will query for weapons that can be effectively wielded with two hands
        for your desired strength. If unchecked, the tool will only compare against the in-game
        listed strength.
      </p>
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

.form-group-description {
  font-size: 12px;
  color: #666;
}

.checkbox-label {
  font-size: 12px;
  width: 100%;
}
</style>
