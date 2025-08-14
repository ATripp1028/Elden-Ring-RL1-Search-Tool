<script setup lang="ts">
import { computed } from 'vue'
import { usePaginationStore, useUIStore } from '../stores'

const paginationStore = usePaginationStore()
const uiStore = useUIStore()

const sortIndicator = computed(() => (column: string) => {
  if (uiStore.sortBy !== column) return ''
  return uiStore.sortOrder === 'asc' ? '▲' : '▼'
})

const handleSort = (column: string) => {
  uiStore.setSort(column)
}
</script>

<template>
  <div class="weapons-table">
    <table>
      <thead>
        <tr>
          <th v-if="uiStore.selectedColumns.includes('Image')" class="image-col" title="Image">
            Image
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Name')"
            class="name-col sortable"
            title="Name"
            @click="handleSort('Name')"
          >
            Name <span class="sort-indicator">{{ sortIndicator('Name') }}</span>
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Weapon Type')"
            class="type-col sortable"
            title="Weapon Type"
            @click="handleSort('Weapon Type')"
          >
            Weapon Type <span class="sort-indicator">{{ sortIndicator('Weapon Type') }}</span>
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Strength')"
            class="stat-col sortable"
            title="Strength"
            @click="handleSort('Strength')"
          >
            Strength <span class="sort-indicator">{{ sortIndicator('Strength') }}</span>
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Dexterity')"
            class="stat-col sortable"
            title="Dexterity"
            @click="handleSort('Dexterity')"
          >
            Dexterity <span class="sort-indicator">{{ sortIndicator('Dexterity') }}</span>
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Intelligence')"
            class="stat-col sortable"
            title="Intelligence"
            @click="handleSort('Intelligence')"
          >
            Intelligence <span class="sort-indicator">{{ sortIndicator('Intelligence') }}</span>
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Faith')"
            class="stat-col sortable"
            title="Faith"
            @click="handleSort('Faith')"
          >
            Faith <span class="sort-indicator">{{ sortIndicator('Faith') }}</span>
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Arcane')"
            class="stat-col sortable"
            title="Arcane"
            @click="handleSort('Arcane')"
          >
            Arcane <span class="sort-indicator">{{ sortIndicator('Arcane') }}</span>
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Damage Type')"
            class="damage-type-col sortable"
            title="Damage Type"
            @click="handleSort('Damage Type')"
          >
            Damage Type <span class="sort-indicator">{{ sortIndicator('Damage Type') }}</span>
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Attack Type')"
            class="damage-type-col sortable"
            title="Attack Type"
            @click="handleSort('Attack Type')"
          >
            Attack Type
            <span class="sort-indicator">{{ sortIndicator('Attack Type') }}</span>
          </th>
          <th
            v-if="uiStore.selectedColumns.includes('Status Buildups')"
            class="status-buildups-col sortable"
            title="Status Buildups"
            @click="handleSort('Status Buildups')"
          >
            Status Buildups
            <span class="sort-indicator">{{ sortIndicator('Status Buildups') }}</span>
          </th>
          <th v-if="uiStore.selectedColumns.includes('Wiki')" class="wiki-col" title="Wiki">
            Wiki
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="weapon in paginationStore.paginatedWeapons" :key="weapon.id">
          <td v-if="uiStore.selectedColumns.includes('Image')">
            <img :src="weapon.image" :alt="weapon.name" class="weapon-image" />
          </td>
          <td v-if="uiStore.selectedColumns.includes('Name')">{{ weapon.name }}</td>
          <td v-if="uiStore.selectedColumns.includes('Weapon Type')">
            {{ weapon.category }}
          </td>
          <td v-if="uiStore.selectedColumns.includes('Strength')">
            <div>One Hand: {{ weapon.requiredAttributes.strengthOneHand }}</div>
            <div>Two Hand: {{ weapon.requiredAttributes.strengthTwoHand }}</div>
          </td>
          <td v-if="uiStore.selectedColumns.includes('Dexterity')">
            {{ weapon.requiredAttributes.dexterity }}
          </td>
          <td v-if="uiStore.selectedColumns.includes('Intelligence')">
            {{ weapon.requiredAttributes.intelligence }}
          </td>
          <td v-if="uiStore.selectedColumns.includes('Faith')">
            {{ weapon.requiredAttributes.faith }}
          </td>
          <td v-if="uiStore.selectedColumns.includes('Arcane')">
            {{ weapon.requiredAttributes.arcane }}
          </td>
          <td v-if="uiStore.selectedColumns.includes('Damage Type')">
            <span v-if="weapon.trackedDamageTypes && weapon.trackedDamageTypes.length > 0">
              {{ weapon.trackedDamageTypes.join(', ') }}
            </span>
            <span v-else class="no-secondary">—</span>
          </td>
          <td v-if="uiStore.selectedColumns.includes('Attack Type')">
            <span>{{ weapon.attackTypes.primary }}</span>
          </td>
          <td v-if="uiStore.selectedColumns.includes('Status Buildups')">
            <span
              v-if="weapon.statusBuildup && weapon.statusBuildup !== 'none'"
              class="status-buildup"
            >
              {{ weapon.statusBuildup.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()) }}
            </span>
            <span v-else class="no-status">—</span>
          </td>
          <td v-if="uiStore.selectedColumns.includes('Wiki')">
            <div class="wiki-links">
              <a :href="weapon.wikiGGLink" target="_blank" rel="noopener noreferrer">Wiki.gg</a>
              <a :href="weapon.wikiFextralifeLink" target="_blank" rel="noopener noreferrer"
                >Fextralife</a
              >
            </div>
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
  vertical-align: middle;
}

th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: black;
  position: sticky;
  top: 0;
  z-index: 20;
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

.status-buildups-col {
  width: 12%;
  text-align: center;
}

.wiki-col {
  width: 5%;
}

.weapon-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.wiki-links {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.wiki-links a {
  color: green;
  text-decoration: none;
  position: relative;
  z-index: 35;
  pointer-events: auto;
}

.wiki-links a:hover {
  text-decoration: underline;
}

tr:hover {
  background-color: #f9f9f9;
}

tbody tr {
  position: relative;
  z-index: 15;
}

tbody td {
  position: relative;
  z-index: 15;
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

.status-buildup {
  color: #d63384;
  font-weight: 500;
}

.no-status {
  color: #999;
  font-style: italic;
}

.sortable {
  cursor: pointer;
}

.sort-indicator {
  font-size: 0.8em;
  margin-left: 4px;
}
</style>
