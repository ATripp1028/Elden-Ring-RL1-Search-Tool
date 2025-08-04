import { ref, watch } from 'vue'
import type { Ref } from 'vue'

/**
 * Composable for syncing reactive refs with localStorage
 */
export const useLocalStorage = <T>(
  key: string,
  defaultValue: T,
  serializer: {
    read: (value: string) => T
    write: (value: T) => string
  } = {
    read: JSON.parse,
    write: JSON.stringify,
  }
): [Ref<T>, (value: T) => void] => {
  const storedValue = localStorage.getItem(key)
  const initialValue = storedValue !== null ? serializer.read(storedValue) : defaultValue

  const state = ref<T>(initialValue) as Ref<T>

  const setState = (value: T) => {
    state.value = value
  }

  watch(
    state,
    (newValue) => {
      localStorage.setItem(key, serializer.write(newValue))
    },
    { deep: true }
  )

  return [state, setState]
}

/**
 * Specialized composable for number values in localStorage
 */
export const useLocalStorageNumber = (key: string, defaultValue: number) => {
  return useLocalStorage(key, defaultValue, {
    read: (value: string) => parseInt(value, 10),
    write: (value: number) => value.toString(),
  })
}

/**
 * Specialized composable for boolean values in localStorage
 */
export const useLocalStorageBoolean = (key: string, defaultValue: boolean) => {
  return useLocalStorage(key, defaultValue, {
    read: (value: string) => value === 'true',
    write: (value: boolean) => value.toString(),
  })
}
