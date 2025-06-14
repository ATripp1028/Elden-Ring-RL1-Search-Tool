<template>
  <Menubar :model="items" class="border-noround">
    <template #start>
    </template>
  </Menubar>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Menubar from 'primevue/menubar'

const items = ref([
  {
    label: 'Home',
    icon: 'pi pi-home',
    to: '/'
  },
  {
    label: 'Builds',
    icon: 'pi pi-list',
    to: '/builds'
  },
  {
    label: 'Weapons',
    icon: 'pi pi-box',
    to: '/weapons'
  },
  {
    label: 'Armor',
    icon: 'pi pi-shield',
    to: '/armor'
  },
  {
    label: 'About',
    icon: 'pi pi-info-circle',
    to: '/about'
  }
])
</script>

<style scoped>
.border-noround {
  border-radius: 0 !important;
  background-color: #000000 !important;
  width: 100%;
}

.p-menubar {
  padding: 0.5rem;
  background: var(--surface-card);
  border: 1px solid var(--surface-border);
  border-radius: 6px;
  margin-bottom: 1rem;
}

.p-menubar .p-menubar-root-list > .p-menuitem > .p-menuitem-link {
  padding: 0.75rem 1rem;
}

.p-menubar .p-menubar-root-list > .p-menuitem > .p-menuitem-link .p-menuitem-icon {
  margin-right: 0.5rem;
}
</style> 