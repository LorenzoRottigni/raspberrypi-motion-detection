<script setup lang="ts">
import { useStream } from '@/store/stream';
import { storeToRefs } from 'pinia';

const { stats, feedSource } = storeToRefs(useStream())
</script>

<template>
  <main :style="stats?.recording ? 'border: 6px solid #B47EB3' : ''">
    <p style="color: red">{{ stats }}</p>
    <div v-if="stats?.recording" class="recording-badge">
      {{ stats?.recording_start_time ? (new Date().getTime() - parseInt(stats.recording_start_time.toString())) : '-' }}
      <span />
      REC
    </div>
    <div class="live-streaming">
      <img :src="feedSource" width="900">
    </div>
  </main>
</template>

<style scoped>
@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

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

.recording-badge {
  position: fixed;
  top: 125px;
  right: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #B47EB3;
  font-size: 26px;
  font-weight: bold;
}

.recording-badge span {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background-color: #B47EB3;
  animation: pulse 2s infinite;
}
</style>
