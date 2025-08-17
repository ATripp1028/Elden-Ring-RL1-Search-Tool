<script setup lang="ts">
import { onMounted } from 'vue'
import SearchForm from './components/SearchForm.vue'
import ResultsFilter from './components/ResultsFilter.vue'
import WeaponsTable from './components/WeaponsTable.vue'
import ThemeToggle from './components/ThemeToggle.vue'
import { useThemeStore } from './stores'

const themeStore = useThemeStore()

// Initialize theme on app mount
onMounted(() => {
  themeStore.initializeTheme()
})
</script>

<template>
  <div class="app">
    <ThemeToggle />
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
  background-color: var(--color-bg-primary);
}

.sidebar {
  width: 17%;
  background-color: var(--color-sidebar-bg);
  box-shadow: var(--color-sidebar-shadow);
}

.main-content {
  flex: 1;
  width: 83%;
  background-color: var(--color-bg-primary);
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
</style>
