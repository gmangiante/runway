<script setup lang="ts">
import { RouterView } from "vue-router";
import { MDBSpinner } from "mdb-vue-ui-kit";
import NavBar from './components/NavBar.vue'
</script>

<template>
  <header class="pb-3">
    <NavBar />
  </header>
  <main class="m-3 pt-5">
    <Suspense>
      <RouterView :key="$route.path" /> 
      <template #fallback>
        <div class="d-flex justify-content-center mt-5">
          <MDBSpinner color="primary" />
          <h4 class="ms-2">Loading...</h4>
        </div>
      </template>
    </Suspense>
  </main>
</template>
