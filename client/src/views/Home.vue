<script setup lang="ts">
import { useStream } from '@/store/stream';
import { storeToRefs } from 'pinia';

const { stats, feedSource } = storeToRefs(useStream())
</script>

<template>
  <main>
    <p style="color: red">{{ stats }}</p>
    <div class="live-streaming">
      <img :src="feedSource" width="640" height="480">
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
