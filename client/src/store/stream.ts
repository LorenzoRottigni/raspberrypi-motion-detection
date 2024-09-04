import type { Stats, Strategy } from "@/types"
import { defineStore } from "pinia"
import { computed, ref } from "vue"

export const useStream = defineStore('stream', () => {
  
  const stats = ref<Stats | null>(null)
  const statsUpdatedAt = ref<number | null>(null)
  const statsInterval = ref<number | null>(null)
  const tickRate = ref<number>(2000)
  const loading = ref<boolean>(false)
  const source = 'http://localhost:5000'

  const feedSource = computed(() => statsUpdatedAt.value ? `${source}/feed?t=${statsUpdatedAt.value}` : `${source}/feed`)

  function setLoading(status: boolean) {
    loading.value = status
  }

  function setTickrate(rate: number) {
    tickRate.value = rate
  }

  function setStatsInterval() {
    setInterval(() => {
        fetch(`${source}/stats`, {
            method: 'GET'
        })
        .then(data => data.json())
        .then(data => stats.value = data)
    }, tickRate.value)
  }

  function setStrategy(strategy: Strategy) {
    fetch(`${source}/set_strategy/${strategy}`)
      .then(() => {
        statsUpdatedAt.value = new Date().getTime()
      })
      .catch(error => {
          console.error('Error:', error);
      });
  }

  return {
    stats,
    source,
    feedSource,
    statsUpdatedAt,
    loading,
    tickRate,
    statsInterval,
    setLoading,
    setStatsInterval,
    setTickrate,
    setStrategy
  }
})