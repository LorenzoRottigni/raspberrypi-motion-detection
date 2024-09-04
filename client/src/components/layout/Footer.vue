<script lang="ts" setup>
import { Strategy } from '@/types';
import EntityRecognition from '@/components/icons/EntityRecognition.vue';
import Live from '@/components/icons/Live.vue';
import MotionDetection from '@/components/icons/MotionDetection.vue';
import Record from '@/components/icons/Record.vue';
import { useStream } from '@/store/stream';
import { storeToRefs } from 'pinia';

const $stream = useStream()
const { stats } = storeToRefs($stream)

const strategies = [
  {
    name: Strategy.live,
    icon: Live,
    label: 'LIVE'
  },
  {
    name: Strategy.record,
    icon: Record,
    label: 'RECORD'
  },
  {
    name: Strategy.motion_detection,
    icon: MotionDetection,
    label: 'MOTION DETECTION'
  },
  {
    name: Strategy.entity_recognition,
    icon: EntityRecognition,
    label: 'ENTITY RECOGNITION'
  },
  {
    name: Strategy.off,
    icon: EntityRecognition,
    label: 'POWER OFF'
  },
]


</script>

<template>
<footer>
    <button
      v-for="(strategy, index) in strategies"
      :key="`strategy-${index}`"
      :disabled="stats?.strategy === strategy.name"
      :class="stats?.strategy === strategy.name ? 'active' : ''"
      @click="$stream.setStrategy(strategy.name)"
    >
      {{ strategy.label }}
      <component :is="strategy.icon" />
    </button>
</footer>
</template>

<style scoped>
footer {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    gap: .5rem;
    padding: 1rem;
    background-color: #23022E;
}

button {
    width: 100%;
    padding: .5rem 1rem;
    background-color: #E6E8E6;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    font-weight: bold;
}

button.active {
  background-color: #B47EB3;
  cursor: auto;
  color: black;
}

svg {
  width: 1.5rem;
  height: 1.5rem;
}
</style>