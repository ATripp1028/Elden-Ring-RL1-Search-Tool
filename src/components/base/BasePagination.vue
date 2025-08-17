<script setup lang="ts">
interface Props {
  currentPage: number
  totalPages: number
  itemsPerPage: number
  totalItems: number
  itemsPerPageOptions?: number[]
}

interface Emits {
  (e: 'update:currentPage', page: number): void
  (e: 'update:itemsPerPage', items: number): void
}

const props = withDefaults(defineProps<Props>(), {
  itemsPerPageOptions: () => [10, 20, 40],
})

const emit = defineEmits<Emits>()

const goToPage = (page: number) => {
  if (page >= 1 && page <= props.totalPages) {
    emit('update:currentPage', page)
  }
}

const updateItemsPerPage = (event: Event) => {
  const target = event.target as HTMLSelectElement
  emit('update:itemsPerPage', Number(target.value))
}
</script>

<template>
  <div class="pagination">
    <div class="result-count">{{ totalItems }} weapon{{ totalItems !== 1 ? 's' : '' }} found</div>

    <div class="items-per-page">
      <label for="itemsPerPage" class="items-per-page-label">Items per page:</label>
      <select id="itemsPerPage" :value="itemsPerPage" @change="updateItemsPerPage">
        <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
          {{ option }}
        </option>
      </select>
    </div>

    <div class="page-navigation">
      <button :disabled="currentPage === 1" @click="goToPage(1)">First</button>
      <button :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">Previous</button>
      <span class="page-number"> Page {{ currentPage }} of {{ totalPages }} </span>
      <button :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">Next</button>
      <button :disabled="currentPage >= totalPages" @click="goToPage(totalPages)">Last</button>
    </div>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
}

.result-count {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.items-per-page-label {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.items-per-page select {
  padding: var(--space-xs) var(--space-xs);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-small);
  background-color: var(--color-bg-elevated);
  color: var(--color-text-primary);
  transition: var(--transition-fast);
}

.page-navigation {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.page-navigation button {
  padding: var(--space-xs) var(--space-md);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-small);
  background-color: var(--color-bg-elevated);
  color: var(--color-text-primary);
  cursor: pointer;
  transition: var(--transition-fast);
  font-size: 13px;
}

.page-navigation button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-navigation button:hover:not(:disabled) {
  background-color: var(--color-hover-bg);
  border-color: var(--color-hover-border);
  transform: translateY(-1px);
}

.page-number {
  font-weight: 500;
  color: var(--color-text-secondary);
  white-space: nowrap;
}
</style>
