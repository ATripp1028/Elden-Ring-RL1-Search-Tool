<script setup lang="ts">
import { computed } from 'vue'
import { useStatsStore } from '../stores/stats'
import { useFilterStore } from '../stores/filter'
import weapons from '../model/weapons'

const stats = useStatsStore()
const filter = useFilterStore()

const filteredWeapons = computed(() => {
  return weapons.filter(weapon => {
    // Check if weapon name contains the search query
    const matchesSearch = weapon.name.toLowerCase().includes(filter.searchQuery.toLowerCase())
    
    // Check if weapon stats are less than or equal to current stats
    const meetsRequirements = 
      weapon.stats.strength <= stats.strength &&
      weapon.stats.dexterity <= stats.dexterity &&
      weapon.stats.intelligence <= stats.intelligence &&
      weapon.stats.faith <= stats.faith &&
      weapon.stats.arcane <= stats.arcane

    return matchesSearch && meetsRequirements
  })
})
</script>

<template>
  <div class="weapons-table">
    <table>
      <thead>
        <tr>
          <th class="image-col">Image</th>
          <th class="name-col">Name</th>
          <th class="stat-col">Strength</th>
          <th class="stat-col">Dexterity</th>
          <th class="stat-col">Intelligence</th>
          <th class="stat-col">Faith</th>
          <th class="stat-col">Arcane</th>
          <th class="links-col">Links</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="weapon in filteredWeapons" :key="weapon.name">
          <td class="image-cell">
            <img :src="weapon.imgPath" :alt="weapon.name" class="weapon-image">
          </td>
          <td>{{ weapon.name }}</td>
          <td>{{ weapon.stats.strength }}</td>
          <td>{{ weapon.stats.dexterity }}</td>
          <td>{{ weapon.stats.intelligence }}</td>
          <td>{{ weapon.stats.faith }}</td>
          <td>{{ weapon.stats.arcane }}</td>
          <td class="links-cell">
            <a :href="weapon.wikiGGLink" target="_blank" rel="noopener noreferrer">Wiki.gg</a>
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
  text-align: left;
  border-bottom: 1px solid #ddd;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: black;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: black;
}

.image-col {
  width: 100px;
}

.name-col {
  width: 200px;
}

.stat-col {
  width: 100px;
}

.links-col {
  width: 150px;
}

.image-cell {
  width: 100px;
  padding: 8px;
}

.weapon-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.links-cell {
  white-space: nowrap;
}

.links-cell a {
  margin-right: 10px;
  color: black;
  text-decoration: none;
}

.links-cell a:hover {
  text-decoration: underline;
}

tr:hover {
  background-color: #f9f9f9;
}
</style> 