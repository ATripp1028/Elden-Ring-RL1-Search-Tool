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
  gap: 1rem;
  padding: 1rem;
}

.result-count {
  font-weight: 500;
  color: #666;
}

.items-per-page {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.items-per-page-label {
  font-weight: 500;
  color: #666;
}

.items-per-page select {
  padding: 0.25rem 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.page-navigation {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.page-number {
  font-weight: 500;
  color: #666;
}
</style>
