<script lang="ts" setup>
import { Strategy } from '@/types';
import EntityRecognition from '@/components/icons/EntityRecognition.vue';
import Live from '@/components/icons/Live.vue';
import MotionDetection from '@/components/icons/MotionDetection.vue';
import Record from '@/components/icons/Record.vue';
import { ref } from 'vue';

const source = ref('http://localhost:5000/feed')

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

function setStrategy(strategy: Strategy) {
  fetch(`/set_strategy/${strategy}`)
    .then(() => {
        source.value = `${source.value.split('?')[0]}?t=${new Date().getTime()}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
</script>

<template>
<footer>
    <button v-for="(strategy, index) in strategies" :key="`strategy-${index}`" @click="setStrategy(strategy.name)">
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
}
</style>