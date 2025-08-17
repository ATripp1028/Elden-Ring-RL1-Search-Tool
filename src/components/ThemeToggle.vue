<script setup lang="ts">
import { computed } from 'vue'
import { useThemeStore } from '../stores'
import BaseSingleSelect from './base/BaseSingleSelect.vue'

const themeStore = useThemeStore()

// Create options array for BaseSingleSelect
const themeOptions = computed(() =>
  themeStore.availableThemes.map((theme) => `${theme.icon} ${theme.name}`),
)

// Current selection for BaseSingleSelect (single string)
const selectedTheme = computed({
  get: () => {
    const current = themeStore.currentThemeDefinition
    return `${current.icon} ${current.name}`
  },
  set: (value: string) => {
    // Extract theme name from the option string
    const themeName = value.split(' ').slice(1).join(' ')
    const theme = themeStore.availableThemes.find((t) => t.name === themeName)
    if (theme) {
      themeStore.setTheme(theme.id)
    }
  },
})
</script>

<template>
  <div class="theme-selector">
    <BaseSingleSelect
      :options="themeOptions"
      v-model="selectedTheme"
      placeholder="Choose your ending..."
      class="theme-singleselect"
    />
  </div>
</template>

<style scoped>
.theme-selector {
  position: fixed;
  top: var(--space-lg);
  left: var(--space-lg);
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  background-color: var(--color-bg-elevated);
  border-radius: var(--radius-medium);
  box-shadow: var(--shadow-medium);
  border: 1px solid var(--color-border-medium);
  min-width: 240px;
}

.theme-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  white-space: nowrap;
  flex-shrink: 0;
}

.theme-singleselect {
  flex: 1;
  min-width: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .theme-selector {
    min-width: 60px;
    padding: var(--space-sm);
  }

  .theme-label {
    display: none;
  }
}
</style>
