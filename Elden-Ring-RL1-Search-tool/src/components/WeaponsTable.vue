<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useStatsStore } from '../stores/stats'
import { useFilterStore } from '../stores/filter'
import { useWeaponsStore } from '../stores/weapons'

const stats = useStatsStore()
const filter = useFilterStore()
const weaponsStore = useWeaponsStore()

onMounted(() => {
  weaponsStore.fetchWeapons()
})

const filteredWeapons = computed(() => {
  return weaponsStore.weapons.filter(weapon => {
    // Check if weapon name contains the search query
    const matchesSearch = weapon.name.toLowerCase().includes(filter.searchQuery.toLowerCase())
    
    // Check if weapon stats are less than or equal to current stats
    const meetsRequirements = 
      weapon.requiredAttributes.strength <= stats.strength &&
      weapon.requiredAttributes.dexterity <= stats.dexterity &&
      weapon.requiredAttributes.intelligence <= stats.intelligence &&
      weapon.requiredAttributes.faith <= stats.faith &&
      weapon.requiredAttributes.arcane <= stats.arcane

    return matchesSearch && meetsRequirements
  })
})
</script>

<template>
  <div class="weapons-table">
    <div v-if="weaponsStore.loading" class="loading">Loading weapons...</div>
    <div v-else-if="weaponsStore.error" class="error">{{ weaponsStore.error }}</div>
    <table v-else>
      <thead>
        <tr>
          <th class="image-col">Image</th>
          <th class="name-col">Name</th>
          <th class="stat-col">Strength</th>
          <th class="stat-col">Dexterity</th>
          <th class="stat-col">Intelligence</th>
          <th class="stat-col">Faith</th>
          <th class="stat-col">Arcane</th>
          <th class="wiki-link-cell">Wiki.gg</th>
          <th class="wiki-link-cell">Fextralife</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="weapon in filteredWeapons" :key="weapon.id">
          <td>
            <img :src="weapon.image" :alt="weapon.name" class="weapon-image">
          </td>
          <td>{{ weapon.name }}</td>
          <td>{{ weapon.requiredAttributes.strength }}</td>
          <td>{{ weapon.requiredAttributes.dexterity }}</td>
          <td>{{ weapon.requiredAttributes.intelligence }}</td>
          <td>{{ weapon.requiredAttributes.faith }}</td>
          <td>{{ weapon.requiredAttributes.arcane }}</td>
          <td>
            <a :href="weapon.wikiGGLink" target="_blank" rel="noopener noreferrer">Wiki.gg</a>
          </td>
          <td>
            <a :href="weapon.wikiFextralifeLink" target="_blank" rel="noopener noreferrer">Fextralife</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.weapons-table {
  width: 100%;
  overflow-x: auto;
  color: black;
  margin: 0;
  padding: 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  table-layout: fixed;
  margin: 0;
  padding: 0;
}

th, td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: black;
}

td {
    text-align: center;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: black;
  position: sticky;
}

.image-col {
  width: 10%;
}

.name-col {
  width: 20%;
}

.stat-col {
  width: 10%;
  text-align: center;
}

.links-col {
  width: 10%;
}

.weapon-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.wiki-link-cell {
    width: 10%;
    text-align: center;
    white-space: nowrap;
}

.wiki-link-cell a {
  margin-right: 10px;
  color: black;
  text-decoration: none;
}

.wiki-link-cell a:hover {
  text-decoration: underline;
}

tr:hover {
  background-color: #f9f9f9;
}

.loading, .error {
  text-align: center;
  padding: 20px;
  font-size: 1.2em;
}

.error {
  color: red;
}
</style> 