<script setup lang="ts">
import { computed } from 'vue'
import { usePaginationStore, useUIStore, useFiltersStore } from '../stores'
import { DataType } from '../model/types'

const paginationStore = usePaginationStore()
const uiStore = useUIStore()
const filtersStore = useFiltersStore()

const sortIndicator = computed(() => (column: string) => {
  if (uiStore.sortBy !== column) return ''
  return uiStore.sortOrder === 'asc' ? '▲' : '▼'
})

const handleSort = (column: string) => {
  uiStore.setSort(column)
}

// Determine which columns should be shown based on data type
const shouldShowColumn = computed(() => (column: string) => {
  if (!uiStore.selectedColumns.includes(column)) return false

  // For spells only, hide certain weapon-specific columns
  if (filtersStore.selectedDataType === DataType.SpellsOnly) {
    if (column === 'Strength' || column === 'Dexterity' || column === 'Attack Type') {
      return false
    }
  }

  return true
})
</script>

<template>
  <div class="weapons-table">
    <table>
      <thead>
        <tr>
          <th v-if="shouldShowColumn('Image')" class="image-col" title="Image">Image</th>
          <th
            v-if="shouldShowColumn('Name')"
            class="name-col sortable"
            title="Name"
            @click="handleSort('Name')"
          >
            Name <span class="sort-indicator">{{ sortIndicator('Name') }}</span>
          </th>
          <th
            v-if="shouldShowColumn('Weapon Type')"
            class="type-col sortable"
            title="Weapon Type"
            @click="handleSort('Weapon Type')"
          >
            Weapon Type <span class="sort-indicator">{{ sortIndicator('Weapon Type') }}</span>
          </th>
          <th
            v-if="shouldShowColumn('Strength')"
            class="stat-col sortable"
            title="Strength"
            @click="handleSort('Strength')"
          >
            Strength <span class="sort-indicator">{{ sortIndicator('Strength') }}</span>
          </th>
          <th
            v-if="shouldShowColumn('Dexterity')"
            class="stat-col sortable"
            title="Dexterity"
            @click="handleSort('Dexterity')"
          >
            Dexterity <span class="sort-indicator">{{ sortIndicator('Dexterity') }}</span>
          </th>
          <th
            v-if="shouldShowColumn('Intelligence')"
            class="stat-col sortable"
            title="Intelligence"
            @click="handleSort('Intelligence')"
          >
            Intelligence <span class="sort-indicator">{{ sortIndicator('Intelligence') }}</span>
          </th>
          <th
            v-if="shouldShowColumn('Faith')"
            class="stat-col sortable"
            title="Faith"
            @click="handleSort('Faith')"
          >
            Faith <span class="sort-indicator">{{ sortIndicator('Faith') }}</span>
          </th>
          <th
            v-if="shouldShowColumn('Arcane')"
            class="stat-col sortable"
            title="Arcane"
            @click="handleSort('Arcane')"
          >
            Arcane <span class="sort-indicator">{{ sortIndicator('Arcane') }}</span>
          </th>
          <th
            v-if="shouldShowColumn('Damage Type')"
            class="damage-type-col sortable"
            title="Damage Type"
            @click="handleSort('Damage Type')"
          >
            Damage Type <span class="sort-indicator">{{ sortIndicator('Damage Type') }}</span>
          </th>
          <th
            v-if="shouldShowColumn('Attack Type')"
            class="damage-type-col sortable"
            title="Attack Type"
            @click="handleSort('Attack Type')"
          >
            Attack Type
            <span class="sort-indicator">{{ sortIndicator('Attack Type') }}</span>
          </th>
          <th
            v-if="shouldShowColumn('Status Buildups')"
            class="status-buildups-col sortable"
            title="Status Buildups"
            @click="handleSort('Status Buildups')"
          >
            Status Buildup
            <span class="sort-indicator">{{ sortIndicator('Status Buildups') }}</span>
          </th>
          <th v-if="shouldShowColumn('Wiki')" class="wiki-col" title="Wiki">Wiki</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="weapon in paginationStore.paginatedWeapons" :key="weapon.id">
          <td v-if="shouldShowColumn('Image')">
            <img :src="weapon.image" :alt="weapon.name" class="weapon-image" />
          </td>
          <td v-if="shouldShowColumn('Name')">{{ weapon.name }}</td>
          <td v-if="shouldShowColumn('Weapon Type')">
            {{ weapon.category }}
          </td>
          <td v-if="shouldShowColumn('Strength')">
            <div v-if="weapon.type === 'weapon'">
              One Hand: {{ weapon.requiredAttributes.strengthOneHand }}
            </div>
            <div v-if="weapon.type === 'weapon'">
              Two Hand: {{ weapon.requiredAttributes.strengthTwoHand }}
            </div>
            <span v-else class="no-secondary">—</span>
          </td>
          <td v-if="shouldShowColumn('Dexterity')">
            <span v-if="weapon.type === 'weapon'">{{ weapon.requiredAttributes.dexterity }}</span>
            <span v-else class="no-secondary">—</span>
          </td>
          <td v-if="shouldShowColumn('Intelligence')">
            {{ weapon.requiredAttributes.intelligence }}
          </td>
          <td v-if="shouldShowColumn('Faith')">
            {{ weapon.requiredAttributes.faith }}
          </td>
          <td v-if="shouldShowColumn('Arcane')">
            {{ weapon.requiredAttributes.arcane }}
          </td>
          <td v-if="shouldShowColumn('Damage Type')">
            <span v-if="weapon.trackedDamageTypes && weapon.trackedDamageTypes.length > 0">
              {{ weapon.trackedDamageTypes.join(', ') }}
            </span>
            <span v-else class="no-secondary">—</span>
          </td>
          <td v-if="shouldShowColumn('Attack Type')">
            <span v-if="weapon.type === 'weapon'">{{ weapon.attackTypes.primary }}</span>
            <span v-else class="no-secondary">—</span>
          </td>
          <td v-if="shouldShowColumn('Status Buildups')">
            <span
              v-if="
                weapon.statusBuildup &&
                weapon.statusBuildup !== 'none' &&
                weapon.statusBuildup !== 'None'
              "
              class="status-buildup"
            >
              {{ weapon.statusBuildup.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()) }}
            </span>
            <span v-else class="no-status">—</span>
          </td>
          <td v-if="shouldShowColumn('Wiki')">
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
  color: var(--color-text-primary);
  margin: 0;
  padding: 0;
  flex: 1;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: var(--color-bg-elevated);
  box-shadow: var(--shadow-light);
  table-layout: auto;
  margin: 0;
  padding: 0;
}

th,
td {
  padding: var(--space-md);
  text-align: center;
  border-bottom: 1px solid var(--color-table-border);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--color-text-primary);
}

td {
  text-align: center;
  vertical-align: middle;
}

th {
  background-color: var(--color-table-header-bg);
  font-weight: 600;
  color: var(--color-text-primary);
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
  color: var(--color-primary);
  text-decoration: none;
  position: relative;
  z-index: 35;
  pointer-events: auto;
  transition: var(--transition-fast);
}

.wiki-links a:hover {
  text-decoration: underline;
  color: var(--color-primary-light);
}

tr:hover {
  background-color: var(--color-table-row-hover);
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
  color: var(--color-danger);
}

.no-secondary {
  color: var(--color-text-muted);
  font-style: italic;
}

.status-buildup {
  color: var(--color-danger);
  font-weight: 500;
}

.no-status {
  color: var(--color-text-muted);
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
