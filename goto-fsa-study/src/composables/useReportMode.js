import { ref, watch } from 'vue'

const STORAGE_KEY = 'goto_fsa_report_view_mode'

const readInitialMode = () => {
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY)
    if (saved === 'original' || saved === 'restated') return saved
  } catch {
    // ignore storage access errors
  }
  return 'original'
}

const reportViewMode = ref(readInitialMode()) // 'original' (Previous / With 2023) | 'restated' (Current / Post-Exit)

watch(reportViewMode, (val) => {
  try {
    window.localStorage.setItem(STORAGE_KEY, val)
  } catch {
    // ignore storage access errors
  }
})

export function useReportMode() {
  return { reportViewMode }
}
