<script setup lang="ts">
import { computed, ref } from 'vue'
import { useStatsStore } from '../stores/stats'
import { useFilterStore } from '../stores/filter'
import weapons from '../model/weapons'

const stats = useStatsStore()
const filter = useFilterStore()

const currentPage = ref(1)
const itemsPerPage = ref(10)

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

const paginatedWeapons = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredWeapons.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredWeapons.value.length / itemsPerPage.value)
})

const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const changeItemsPerPage = (newSize: number) => {
  itemsPerPage.value = newSize
  currentPage.value = 1 // Reset to first page when changing items per page
}
</script>

<template>
  <div class="weapons-table">
    <div class="pagination-controls">
      <div class="items-per-page">
        <label for="itemsPerPage">Items per page:</label>
        <select id="itemsPerPage" v-model="itemsPerPage" @change="changeItemsPerPage(Number(itemsPerPage))">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="40">40</option>
        </select>
      </div>
      <div class="page-navigation">
        <button 
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="page-button"
        >
          Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="page-button"
        >
          Next
        </button>
      </div>
    </div>

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
          <th class="wiki-link-cell">Wiki.gg</th>
          <th class="wiki-link-cell">Fextralife</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="weapon in paginatedWeapons" :key="weapon.name">
          <td>
            <img :src="weapon.imgPath" :alt="weapon.name" class="weapon-image">
          </td>
          <td>{{ weapon.name }}</td>
          <td>{{ weapon.stats.strength }}</td>
          <td>{{ weapon.stats.dexterity }}</td>
          <td>{{ weapon.stats.intelligence }}</td>
          <td>{{ weapon.stats.faith }}</td>
          <td>{{ weapon.stats.arcane }}</td>
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

.pagination-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.items-per-page select {
  padding: 0.25rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.page-navigation {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  transition: background-color 0.2s;
}

.page-button:hover:not(:disabled) {
  background-color: #f0f0f0;
}

.page-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: #666;
}
</style> 