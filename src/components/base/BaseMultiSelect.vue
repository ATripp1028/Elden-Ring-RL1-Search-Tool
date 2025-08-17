<script setup lang="ts">
import { computed } from 'vue'
import { useMultiSelect } from '../../composables/useMultiSelect'

interface Props {
  options: string[]
  selectedItems: string[]
  placeholder?: string
  preventDeselectionOfLast?: boolean
}

interface Emits {
  (e: 'update:selectedItems', items: string[]): void
  (e: 'toggle', option: string): void
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Select options...',
  preventDeselectionOfLast: false,
})

const emit = defineEmits<Emits>()

const displayText = computed(() => {
  return props.selectedItems.length > 0
    ? `${props.selectedItems.length} selected`
    : props.placeholder
})

const { isOpen, multiselectRef, toggleOption, isSelected } = useMultiSelect({
  onToggle: (option: string) => {
    // Prevent deselecting the last item if specified
    if (
      props.preventDeselectionOfLast &&
      props.selectedItems.includes(option) &&
      props.selectedItems.length === 1
    ) {
      return
    }

    const index = props.selectedItems.indexOf(option)
    const newSelection = [...props.selectedItems]

    if (index > -1) {
      newSelection.splice(index, 1)
    } else {
      newSelection.push(option)
    }

    emit('update:selectedItems', newSelection)
    emit('toggle', option)
  },
  isSelected: (option: string) => props.selectedItems.includes(option),
})
</script>

<template>
  <div class="multiselect" ref="multiselectRef">
    <div class="multiselect-trigger" @click="isOpen = !isOpen" :class="{ open: isOpen }">
      <span class="multiselect-display">{{ displayText }}</span>
      <span class="multiselect-arrow">▼</span>
    </div>
    <div class="multiselect-dropdown" v-if="isOpen">
      <div class="multiselect-options">
        <div
          v-for="option in options"
          :key="option"
          class="multiselect-option"
          :class="{ selected: isSelected(option) }"
          @click="toggleOption(option)"
        >
          <span class="checkbox">{{ isSelected(option) ? '✓' : '' }}</span>
          <span class="option-text">{{ option }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.multiselect {
  position: relative;
  flex: 1;
  min-width: 0;
}

.multiselect-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-xs) var(--space-sm);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-small);
  background-color: var(--color-bg-elevated);
  cursor: pointer;
  font-size: 14px;
  min-height: 32px;
  transition: var(--transition-fast);
}

.multiselect-trigger:hover {
  border-color: var(--color-hover-border);
  background-color: var(--color-hover-bg);
}

.multiselect-trigger.open {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-focus-ring);
}

.multiselect-display {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--color-text-primary);
}

.multiselect-arrow {
  font-size: 10px;
  color: var(--color-text-secondary);
  transition: transform var(--transition-fast);
  margin-left: var(--space-sm);
}

.multiselect-trigger.open .multiselect-arrow {
  transform: rotate(180deg);
}

.multiselect-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: var(--color-bg-elevated);
  border: 1px solid var(--color-border-medium);
  border-top: none;
  border-radius: 0 0 var(--radius-small) var(--radius-small);
  box-shadow: var(--shadow-medium);
  z-index: 30;
  max-height: 200px;
  overflow-y: auto;
}

.multiselect-options {
  padding: var(--space-xs) 0;
}

.multiselect-option {
  display: flex;
  align-items: center;
  padding: var(--space-sm) var(--space-md);
  cursor: pointer;
  transition: var(--transition-fast);
  color: var(--color-text-primary);
}

.multiselect-option:hover {
  background-color: var(--color-hover-bg);
}

.multiselect-option.selected {
  background-color: var(--color-active-bg);
  color: var(--color-primary);
}

.checkbox {
  width: 16px;
  height: 16px;
  border: 1px solid var(--color-border-medium);
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--space-sm);
  font-size: 12px;
  color: var(--color-primary);
  background-color: var(--color-bg-elevated);
}

.multiselect-option.selected .checkbox {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-bg-primary);
}

.option-text {
  flex: 1;
  color: var(--color-text-primary);
}
</style>
