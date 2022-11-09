<script setup lang="ts">
import NavBar from './components/NavBar.vue'
import { RouterView } from "vue-router";
</script>

<template>
  <header class="pb-3">
    <NavBar />
  </header>
  <main class="m-3 pt-5">
    <RouterView /> 
  </main>
</template>
