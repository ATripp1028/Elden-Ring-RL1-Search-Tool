import { defineStore } from 'pinia'
import { ref, watch, computed } from 'vue'

// Elden Ring ending-based themes
export type EndingTheme =
  | 'age-of-fracture'
  | 'age-of-duskborn'
  | 'age-of-order'
  | 'blessing-of-despair'
  | 'age-of-stars'
  | 'lord-of-frenzied-flame'

export interface ThemeDefinition {
  id: EndingTheme
  name: string
  description: string
  icon: string
}

export const AVAILABLE_THEMES: ThemeDefinition[] = [
  {
    id: 'age-of-fracture',
    name: 'Age of Fracture',
    description: 'The Erdtree endures, cracked but golden',
    icon: '🌳'
  },
  {
    id: 'age-of-duskborn',
    name: 'Age of the Duskborn',
    description: 'Death becomes life, life becomes death',
    icon: '💀'
  },
  {
    id: 'age-of-order',
    name: 'Age of Order',
    description: 'Perfect Order through divine geometry',
    icon: '⚡'
  },
  {
    id: 'blessing-of-despair',
    name: 'Blessing of Despair',
    description: 'The curse spreads to all living things',
    icon: '🩸'
  },
  {
    id: 'age-of-stars',
    name: 'Age of Stars',
    description: 'Cold lunar light guides the way',
    icon: '🌙'
  },
  {
    id: 'lord-of-frenzied-flame',
    name: 'Lord of Frenzied Flame',
    description: 'May chaos take the world!',
    icon: '🔥'
  }
]

export const useThemeStore = defineStore('theme', () => {
  // Current theme - default to Age of Fracture
  const currentTheme = ref<EndingTheme>(
    (localStorage.getItem('theme.currentTheme') as EndingTheme) || 'age-of-fracture'
  )

  // Get current theme definition
  const currentThemeDefinition = computed(() =>
    AVAILABLE_THEMES.find(theme => theme.id === currentTheme.value) || AVAILABLE_THEMES[0]
  )

  // Legacy computed for backwards compatibility
  const isDark = computed(() => {
    // Most themes are "dark" except Age of Order and Age of Duskborn
    return !['age-of-order', 'age-of-duskborn'].includes(currentTheme.value)
  })

  // Legacy theme name for backwards compatibility
  const themeName = computed(() => currentTheme.value)

  // Set specific theme
  const setTheme = (theme: EndingTheme) => {
    currentTheme.value = theme
    applyTheme()
  }

  // Legacy toggle function - cycles through themes
  const toggleTheme = () => {
    const currentIndex = AVAILABLE_THEMES.findIndex(theme => theme.id === currentTheme.value)
    const nextIndex = (currentIndex + 1) % AVAILABLE_THEMES.length
    setTheme(AVAILABLE_THEMES[nextIndex].id)
  }

  // Apply theme to document
  const applyTheme = () => {
    document.documentElement.setAttribute('data-theme', currentTheme.value)
  }

  // Initialize theme on store creation
  const initializeTheme = () => {
    applyTheme()
  }

  // Watch for changes and update localStorage
  watch(currentTheme, (newValue) => {
    localStorage.setItem('theme.currentTheme', newValue)
  })

  // Watch for theme changes and apply
  watch(currentTheme, () => {
    applyTheme()
  })

  return {
    // New theme system
    currentTheme,
    currentThemeDefinition,
    availableThemes: AVAILABLE_THEMES,
    setTheme,

    // Legacy compatibility
    isDark,
    themeName,
    toggleTheme,
    initializeTheme,
  }
})
