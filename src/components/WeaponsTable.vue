<script setup lang="ts">
import { computed, ref } from 'vue'
import { useStatsStore } from '../stores/stats'
import { useFilterStore } from '../stores/filter'

interface ScrapedWeapon {
  weapon_name: string
  weapon_type: string
  attributes?: {
    strength?: number | { one_hand: number; two_hand: number }
    dexterity?: number
    intelligence?: number
    faith?: number
    arcane?: number
  }
  image?: {
    src: string
  }
  wikiGGLink?: string
  wikiFextralifeLink?: string
}

// Import all weapon JSON files directly
import weaponsThrustingShields from '../resources/weapons_thrusting_shields.json'
import weaponsGreatshields from '../resources/weapons_greatshields.json'
import weaponsMediumShields from '../resources/weapons_medium_shields.json'
import weaponsSmallShields from '../resources/weapons_small_shields.json'
import weaponsTorches from '../resources/weapons_torches.json'
import weaponsSacredSeals from '../resources/weapons_sacred_seals.json'
import weaponsStaves from '../resources/weapons_staves.json'
import weaponsBallista from '../resources/weapons_ballista.json'
import weaponsCrossbows from '../resources/weapons_crossbows.json'
import weaponsGreatbows from '../resources/weapons_greatbows.json'
import weaponsBows from '../resources/weapons_bows.json'
import weaponsLightBows from '../resources/weapons_light_bows.json'
import weaponsPerfumeBottles from '../resources/weapons_perfume_bottles.json'
import weaponsBeastClaws from '../resources/weapons_beast_claws.json'
import weaponsClaws from '../resources/weapons_claws.json'
import weaponsHandToHand from '../resources/weapons_hand_to_hand.json'
import weaponsFists from '../resources/weapons_fists.json'
import weaponsWhips from '../resources/weapons_whips.json'
import weaponsReapers from '../resources/weapons_reapers.json'
import weaponsHalberds from '../resources/weapons_halberds.json'
import weaponsGreatSpears from '../resources/weapons_great_spears.json'
import weaponsSpears from '../resources/weapons_spears.json'
import weaponsColossalWeapons from '../resources/weapons_colossal_weapons.json'
import weaponsGreatHammers from '../resources/weapons_great_hammers.json'
import weaponsFlails from '../resources/weapons_flails.json'
import weaponsHammers from '../resources/weapons_hammers.json'
import weaponsGreataxes from '../resources/weapons_greataxes.json'
import weaponsAxes from '../resources/weapons_axes.json'
import weaponsTwinblades from '../resources/weapons_twinblades.json'
import weaponsGreatKatanas from '../resources/weapons_great_katanas.json'
import weaponsKatanas from '../resources/weapons_katanas.json'
import weaponsBackhandBlades from '../resources/weapons_backhand_blades.json'
import weaponsCurvedGreatswords from '../resources/weapons_curved_greatswords.json'
import weaponsCurvedSwords from '../resources/weapons_curved_swords.json'
import weaponsHeavyThrustingSwords from '../resources/weapons_heavy_thrusting_swords.json'
import weaponsThrustingSwords from '../resources/weapons_thrusting_swords.json'
import weaponsColossalSwords from '../resources/weapons_colossal_swords.json'
import weaponsGreatswords from '../resources/weapons_greatswords.json'
import weaponsLightGreatswords from '../resources/weapons_light_greatswords.json'
import weaponsStraightSwords from '../resources/weapons_straight_swords.json'
import weaponsDaggers from '../resources/weapons_daggers.json'
import weaponsThrowingBlades from '../resources/weapons_throwing_blades.json'

const stats = useStatsStore()
const filter = useFilterStore()

// Process all weapons on component initialization
const allWeaponArrays = [
  weaponsThrustingShields,
  weaponsGreatshields,
  weaponsMediumShields,
  weaponsSmallShields,
  weaponsTorches,
  weaponsSacredSeals,
  weaponsStaves,
  weaponsBallista,
  weaponsCrossbows,
  weaponsGreatbows,
  weaponsBows,
  weaponsLightBows,
  weaponsPerfumeBottles,
  weaponsBeastClaws,
  weaponsClaws,
  weaponsHandToHand,
  weaponsFists,
  weaponsWhips,
  weaponsReapers,
  weaponsHalberds,
  weaponsGreatSpears,
  weaponsSpears,
  weaponsColossalWeapons,
  weaponsGreatHammers,
  weaponsFlails,
  weaponsHammers,
  weaponsGreataxes,
  weaponsAxes,
  weaponsTwinblades,
  weaponsGreatKatanas,
  weaponsKatanas,
  weaponsBackhandBlades,
  weaponsCurvedGreatswords,
  weaponsCurvedSwords,
  weaponsHeavyThrustingSwords,
  weaponsThrustingSwords,
  weaponsColossalSwords,
  weaponsGreatswords,
  weaponsLightGreatswords,
  weaponsStraightSwords,
  weaponsDaggers,
  weaponsThrowingBlades,
]

const weapons = ref(
  allWeaponArrays.flat().map((weapon: ScrapedWeapon, index: number) => {
    // Handle different attribute formats from the scraped data
    let strength = 0
    let dexterity = 0
    let intelligence = 0
    let faith = 0
    let arcane = 0

    if (weapon.attributes) {
      if (weapon.attributes.strength) {
        // Handle the new format with one_hand/two_hand structure
        if (typeof weapon.attributes.strength === 'object') {
          strength = weapon.attributes.strength.one_hand || 0
        } else {
          strength = weapon.attributes.strength || 0
        }
      }
      dexterity = weapon.attributes.dexterity || 0
      intelligence = weapon.attributes.intelligence || 0
      faith = weapon.attributes.faith || 0
      arcane = weapon.attributes.arcane || 0
    }

    return {
      id: weapon.weapon_name || `weapon-${index}`,
      name: weapon.weapon_name || 'Unknown Weapon',
      image: weapon.image?.src || '',
      description: weapon.weapon_type || '',
      category: weapon.weapon_type || '',
      weight: 0, // Not available in scraped data
      attack: {
        physical: 0,
        magic: 0,
        fire: 0,
        lightning: 0,
        holy: 0,
        critical: 0,
      },
      defence: {
        physical: 0,
        magic: 0,
        fire: 0,
        lightning: 0,
        holy: 0,
        boost: 0,
      },
      requiredAttributes: {
        strength,
        dexterity,
        intelligence,
        faith,
        arcane,
      },
      scalesWith: {
        strength: 0,
        dexterity: 0,
        intelligence: 0,
        faith: 0,
        arcane: 0,
      },
      wikiGGLink: weapon.wikiGGLink || '',
      wikiFextralifeLink: weapon.wikiFextralifeLink || '',
    }
  }),
)

const totalPages = computed(() => {
  return Math.ceil(filteredWeapons.value.length / stats.itemsPerPage)
})

const filteredWeapons = computed(() => {
  return weapons.value.filter((weapon) => {
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

const paginatedWeapons = computed(() => {
  const start = (stats.page - 1) * stats.itemsPerPage
  const end = start + stats.itemsPerPage
  return filteredWeapons.value.slice(start, end)
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
        {{ filteredWeapons.length }} weapon{{ filteredWeapons.length !== 1 ? 's' : '' }} found
      </div>
      <div class="page-navigation">
        <button :disabled="stats.page === 1" @click="stats.page = 1">First</button>
        <button :disabled="stats.page === 1" @click="stats.page--">Previous</button>
        <span>Page {{ stats.page }} of {{ totalPages }}</span>
        <button :disabled="stats.page >= totalPages" @click="stats.page++">Next</button>
        <button :disabled="stats.page >= totalPages" @click="stats.page = totalPages">Last</button>
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
          <td>{{ weapon.requiredAttributes.strength }}</td>
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
