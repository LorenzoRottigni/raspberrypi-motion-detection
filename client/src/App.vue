<script setup lang="ts">
import { RouterView } from 'vue-router'
import Header from './components/layout/Header.vue';
import Footer from './components/layout/Footer.vue';
import { onMounted } from 'vue';
import { useStream } from './store/stream';

const $stream = useStream()

onMounted(() => {
  $stream.setStatsInterval()
})
</script>

<template>
  <Header />
  <RouterView />
  <Footer />
</template>

<style>

</style>
