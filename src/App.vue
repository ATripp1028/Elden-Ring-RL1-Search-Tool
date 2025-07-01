<script setup lang="ts">
import SearchForm from './components/SearchForm.vue'
import ResultsFilter from './components/ResultsFilter.vue'
import WeaponsTable from './components/WeaponsTable.vue'
</script>

<template>
  <div class="app">
    <div class="sidebar">
      <SearchForm />
    </div>
    <main class="main-content">
      <ResultsFilter />
      <WeaponsTable />
    </main>
  </div>
</template>

<style scoped>
.app {
  display: flex;
  min-height: 100vh;
  width: 100vw;
}

.sidebar {
  width: 17%;
  background-color: white;
}

.main-content {
  flex: 1;
  width: 83%;
  background-color: white;
}
</style>
