<script setup lang="ts">

import { type Stats } from '@/types';
import { ref, onMounted } from 'vue';

const stats = ref<Stats | null>(null)
const source = ref('http://localhost:5000/feed')

onMounted(() => {
  setInterval(() => {
    fetch('http://localhost:5000/stats', {
        method: 'GET'
    })
    .then(data => data.json())
    .then(data => stats.value = data)
}, 2000)
})
</script>

<template>
  <main>
    <p style="color: red">{{ stats }}</p>
    <div class="live-streaming">
      <img :src="source" width="640" height="480">
    </div>
  </main>
</template>

<style scoped>
main {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.live-streaming {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>