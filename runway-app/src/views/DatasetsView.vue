<script setup lang="ts">
import DatasetsTable from '@/components/DatasetsTable.vue'
import { MDBSpinner } from 'mdb-vue-ui-kit';
</script>

<template>
  <main>
    <Suspense>
      <DatasetsTable />
      <template #fallback>
        <div class="d-flex justify-content-center mt-5">
          <MDBSpinner />
          <h4 class="ms-2">Loading...</h4>
        </div>
      </template>
    </Suspense>
  </main>
</template>
