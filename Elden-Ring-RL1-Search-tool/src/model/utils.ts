export const getStoredValue = (key: string, defaultValue: number): number => {
    const stored = localStorage.getItem(key)
    return stored ? parseInt(stored, 10) : defaultValue
}