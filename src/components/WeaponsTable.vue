<script setup lang="ts">
import { computed } from 'vue'
import { useStatsStore } from '../stores/stats'

const stats = useStatsStore()

const paginatedWeapons = computed(() => {
  const start = (stats.page - 1) * stats.itemsPerPage
  const end = start + stats.itemsPerPage
  return stats.filteredWeapons.slice(start, end)
})
</script>

<template>
  <div class="weapons-table">
    <div class="pagination-controls">
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
      <div class="result-count">
        {{ stats.filteredWeapons.length }} weapon{{ stats.filteredWeapons.length !== 1 ? 's' : '' }}
        found
      </div>
      <div class="page-navigation">
        <button :disabled="stats.page === 1" @click="stats.page = 1">First</button>
        <button :disabled="stats.page === 1" @click="stats.page--">Previous</button>
        <span>Page {{ stats.page }} of {{ stats.totalPages }}</span>
        <button :disabled="stats.page >= stats.totalPages" @click="stats.page++">Next</button>
        <button :disabled="stats.page >= stats.totalPages" @click="stats.page = stats.totalPages">
          Last
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
        <tr v-for="weapon in paginatedWeapons" :key="weapon.id">
          <td>
            <img :src="weapon.image" :alt="weapon.name" class="weapon-image" />
          </td>
          <td>{{ weapon.name }}</td>
          <td>
            <div>One Hand: {{ weapon.requiredAttributes.strengthOneHand }}</div>
            <div>Two Hand: {{ weapon.requiredAttributes.strengthTwoHand }}</div>
          </td>
          <td>{{ weapon.requiredAttributes.dexterity }}</td>
          <td>{{ weapon.requiredAttributes.intelligence }}</td>
          <td>{{ weapon.requiredAttributes.faith }}</td>
          <td>{{ weapon.requiredAttributes.arcane }}</td>
          <td>
            <a :href="weapon.wikiGGLink" target="_blank" rel="noopener noreferrer">Wiki.gg</a>
          </td>
          <td>
            <a :href="weapon.wikiFextralifeLink" target="_blank" rel="noopener noreferrer"
              >Fextralife</a
            >
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

th,
td {
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

.loading,
.error {
  text-align: center;
  padding: 20px;
  font-size: 1.2em;
}

.error {
  color: red;
}

.pagination-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: white;
  border-bottom: 1px solid #ddd;
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
</style>
