<script setup lang="ts">
import SearchForm from './components/SearchForm.vue'
import ResultsFilter from './components/ResultsFilter.vue'
</script>

<template>
  <div class="app">
    <SearchForm />
    <ResultsFilter />
    <main class="main-content">
      <!-- Main content will go here -->
    </main>
  </div>
</template>

<style scoped>
.app {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 300px; /* Same as the sidebar width */
  padding: 20px;
}
</style>
