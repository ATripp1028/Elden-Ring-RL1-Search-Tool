import { ref, onMounted, onUnmounted } from 'vue'

export interface MultiSelectOptions {
  onToggle?: (option: string) => void
  isSelected?: (option: string) => boolean
  preventDeselectionOfLast?: boolean
  selectedItems?: string[]
}

export const useMultiSelect = (options: MultiSelectOptions = {}) => {
  const isOpen = ref(false)
  const multiselectRef = ref<HTMLDivElement>()

  const toggleOption = (option: string) => {
    if (options.onToggle) {
      options.onToggle(option)
    }
  }

  const isSelected = (option: string) => {
    if (options.isSelected) {
      return options.isSelected(option)
    }
    return false
  }

  const handleClickOutside = (event: Event) => {
    if (multiselectRef.value && !multiselectRef.value.contains(event.target as Node)) {
      isOpen.value = false
    }
  }

  const handleKeydown = (event: KeyboardEvent) => {
    if (event.key === 'Escape') {
      isOpen.value = false
    }
  }

  onMounted(() => {
    document.addEventListener('click', handleClickOutside)
    document.addEventListener('keydown', handleKeydown)
  })

  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
    document.removeEventListener('keydown', handleKeydown)
  })

  return {
    isOpen,
    multiselectRef,
    toggleOption,
    isSelected,
  }
}
