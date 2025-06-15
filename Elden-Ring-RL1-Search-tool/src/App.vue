<script setup lang="ts">
import SearchForm from './components/SearchForm.vue'
import ResultsFilter from './components/ResultsFilter.vue'
import WeaponsTable from './components/WeaponsTable.vue'
</script>

<template>
  <div class="app">
    <SearchForm />
    <ResultsFilter />
    <main class="main-content">
      <WeaponsTable />
    </main>
  </div>
</template>

<style scoped>
.app {
  display: flex;
  min-height: 100vh;
  width: 100vw;
  overflow-x: hidden;
}

.main-content {
  flex: 1;
  margin-left: 17%; /* Same as the sidebar width */
  padding-top: 60px; /* Space for the filter bar */
  width: calc(100vw - 17%);
}
</style>
