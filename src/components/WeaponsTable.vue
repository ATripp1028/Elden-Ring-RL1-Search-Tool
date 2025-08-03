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
          <th v-if="stats.selectedColumns.includes('Image')" class="image-col" title="Image">
            Image
          </th>
          <th v-if="stats.selectedColumns.includes('Name')" class="name-col" title="Name">Name</th>
          <th v-if="stats.selectedColumns.includes('Strength')" class="stat-col" title="Strength">
            Strength
          </th>
          <th v-if="stats.selectedColumns.includes('Dexterity')" class="stat-col" title="Dexterity">
            Dexterity
          </th>
          <th
            v-if="stats.selectedColumns.includes('Intelligence')"
            class="stat-col"
            title="Intelligence"
          >
            Intelligence
          </th>
          <th v-if="stats.selectedColumns.includes('Faith')" class="stat-col" title="Faith">
            Faith
          </th>
          <th v-if="stats.selectedColumns.includes('Arcane')" class="stat-col" title="Arcane">
            Arcane
          </th>
          <th
            v-if="stats.selectedColumns.includes('Primary Damage')"
            class="damage-type-col"
            title="Primary Damage"
          >
            Primary Damage
          </th>
          <th
            v-if="stats.selectedColumns.includes('Secondary Damage')"
            class="damage-type-col"
            title="Secondary Damage"
          >
            Secondary Damage
          </th>
          <th
            v-if="stats.selectedColumns.includes('Wiki.gg')"
            class="wiki-link-cell"
            title="Wiki.gg"
          >
            Wiki.gg
          </th>
          <th
            v-if="stats.selectedColumns.includes('Fextralife')"
            class="wiki-link-cell"
            title="Fextralife"
          >
            Fextralife
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="weapon in paginatedWeapons" :key="weapon.id">
          <td v-if="stats.selectedColumns.includes('Image')">
            <img :src="weapon.image" :alt="weapon.name" class="weapon-image" />
          </td>
          <td v-if="stats.selectedColumns.includes('Name')">{{ weapon.name }}</td>
          <td v-if="stats.selectedColumns.includes('Strength')">
            <div>One Hand: {{ weapon.requiredAttributes.strengthOneHand }}</div>
            <div>Two Hand: {{ weapon.requiredAttributes.strengthTwoHand }}</div>
          </td>
          <td v-if="stats.selectedColumns.includes('Dexterity')">
            {{ weapon.requiredAttributes.dexterity }}
          </td>
          <td v-if="stats.selectedColumns.includes('Intelligence')">
            {{ weapon.requiredAttributes.intelligence }}
          </td>
          <td v-if="stats.selectedColumns.includes('Faith')">
            {{ weapon.requiredAttributes.faith }}
          </td>
          <td v-if="stats.selectedColumns.includes('Arcane')">
            {{ weapon.requiredAttributes.arcane }}
          </td>
          <td v-if="stats.selectedColumns.includes('Primary Damage')">
            {{ weapon.damageTypes.major }}
          </td>
          <td v-if="stats.selectedColumns.includes('Secondary Damage')">
            <span v-if="weapon.damageTypes.minor.length > 0">
              {{ weapon.damageTypes.minor.join(', ') }}
            </span>
            <span v-else class="no-secondary">—</span>
          </td>
          <td v-if="stats.selectedColumns.includes('Wiki.gg')">
            <a :href="weapon.wikiGGLink" target="_blank" rel="noopener noreferrer">Wiki.gg</a>
          </td>
          <td v-if="stats.selectedColumns.includes('Fextralife')">
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
  table-layout: auto;
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
