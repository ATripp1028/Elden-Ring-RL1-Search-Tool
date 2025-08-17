<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface Props {
  options: string[]
  modelValue: string
  placeholder?: string
  disabled?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: string): void
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Select an option...',
  disabled: false,
})

const emit = defineEmits<Emits>()

const isOpen = ref(false)
const selectRef = ref<HTMLElement>()

const displayText = computed(() => {
  if (props.modelValue) {
    return props.modelValue
  }
  return props.placeholder
})

const toggleDropdown = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value
  }
}

const selectOption = (option: string) => {
  emit('update:modelValue', option)
  isOpen.value = false
}

const isSelected = (option: string) => {
  return props.modelValue === option
}

// Close dropdown when clicking outside
const handleClickOutside = (event: Event) => {
  if (selectRef.value && !selectRef.value.contains(event.target as Node)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<template>
  <div class="singleselect" ref="selectRef">
    <div
      class="singleselect-trigger"
      @click="toggleDropdown"
      :class="{
        open: isOpen,
        disabled: disabled,
        'has-value': modelValue,
      }"
    >
      <span class="singleselect-display">{{ displayText }}</span>
      <span class="singleselect-arrow">▼</span>
    </div>
    <div class="singleselect-dropdown" v-if="isOpen && !disabled">
      <div class="singleselect-options">
        <div
          v-for="option in options"
          :key="option"
          class="singleselect-option"
          :class="{ selected: isSelected(option) }"
          @click="selectOption(option)"
        >
          <span class="option-text">{{ option }}</span>
          <span v-if="isSelected(option)" class="selected-indicator">✓</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.singleselect {
  position: relative;
  flex: 1;
  min-width: 0;
}

.singleselect-trigger {
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

.singleselect-trigger:hover:not(.disabled) {
  border-color: var(--color-hover-border);
  background-color: var(--color-hover-bg);
}

.singleselect-trigger.open {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-focus-ring);
}

.singleselect-trigger.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--color-bg-tertiary);
}

.singleselect-display {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--color-text-primary);
  text-align: left;
}

.singleselect-trigger:not(.has-value) .singleselect-display {
  color: var(--color-text-muted);
}

.singleselect-arrow {
  font-size: 10px;
  color: var(--color-text-secondary);
  transition: transform var(--transition-fast);
  margin-left: var(--space-sm);
  flex-shrink: 0;
}

.singleselect-trigger.open .singleselect-arrow {
  transform: rotate(180deg);
}

.singleselect-dropdown {
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

.singleselect-options {
  padding: var(--space-xs) 0;
}

.singleselect-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-sm) var(--space-md);
  cursor: pointer;
  transition: var(--transition-fast);
  color: var(--color-text-primary);
}

.singleselect-option:hover {
  background-color: var(--color-hover-bg);
}

.singleselect-option.selected {
  background-color: var(--color-active-bg);
  color: var(--color-primary);
  font-weight: 500;
}

.option-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.selected-indicator {
  font-size: 12px;
  color: var(--color-primary);
  font-weight: bold;
  flex-shrink: 0;
  margin-left: var(--space-sm);
}
</style>
