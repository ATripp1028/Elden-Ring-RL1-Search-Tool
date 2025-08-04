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
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  font-size: 14px;
  min-height: 32px;
}

.multiselect-trigger:hover {
  border-color: #666;
}

.multiselect-trigger.open {
  border-color: #666;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.1);
}

.multiselect-display {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #666;
}

.multiselect-arrow {
  font-size: 10px;
  color: #666;
  transition: transform 0.2s;
  margin-left: 8px;
}

.multiselect-trigger.open .multiselect-arrow {
  transform: rotate(180deg);
}

.multiselect-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 30;
  max-height: 200px;
  overflow-y: auto;
}

.multiselect-options {
  padding: 4px 0;
}

.multiselect-option {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.multiselect-option:hover {
  background-color: #f5f5f5;
}

.multiselect-option.selected {
  background-color: #e3f2fd;
}

.checkbox {
  width: 16px;
  height: 16px;
  border: 1px solid #ddd;
  border-radius: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  font-size: 12px;
  color: #2196f3;
  background-color: white;
}

.multiselect-option.selected .checkbox {
  background-color: #2196f3;
  border-color: #2196f3;
  color: white;
}

.option-text {
  flex: 1;
  color: #666;
}
</style>
