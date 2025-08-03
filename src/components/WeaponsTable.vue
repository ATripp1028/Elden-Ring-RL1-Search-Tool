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
          <th class="damage-type-col">Primary Damage</th>
          <th class="damage-type-col">Secondary Damage</th>
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
          <td>{{ weapon.damageTypes.major }}</td>
          <td>
            <span v-if="weapon.damageTypes.minor.length > 0">
              {{ weapon.damageTypes.minor.join(', ') }}
            </span>
            <span v-else class="no-secondary">—</span>
          </td>
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
  height: 100%;
  overflow: auto;
  color: black;
  margin: 0;
  padding: 0;
  flex: 1;
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
  top: 0;
  z-index: 10;
}

.image-col {
  width: 8%;
}

.name-col {
  width: 16%;
}

.stat-col {
  width: 8%;
  text-align: center;
}

.damage-type-col {
  width: 10%;
  text-align: center;
}

.links-col {
  width: 8%;
}

.weapon-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.wiki-link-cell {
  width: 8%;
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

.no-secondary {
  color: #999;
  font-style: italic;
}
</style>
