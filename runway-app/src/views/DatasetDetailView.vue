<script setup lang="ts">
import DatasetDetail from '@/components/DatasetDetail.vue';
import { MDBSpinner, MDBBreadcrumb, MDBBreadcrumbItem } from 'mdb-vue-ui-kit';

defineProps({
    id: String
})

</script>

<template>
  <main>
    <Suspense>
      <div>
        <nav aria-label="breadcrumb">
          <MDBBreadcrumb>
            <MDBBreadcrumbItem><a href="/datasets">Datasets</a></MDBBreadcrumbItem>
            <MDBBreadcrumbItem active>
              Dataset detail
            </MDBBreadcrumbItem>
          </MDBBreadcrumb>
        </nav>
        <DatasetDetail :id="id" />
      </div>
      <template #fallback>
        <div class="d-flex justify-content-center mt-5">
          <MDBSpinner color="primary" />
          <h4 class="ms-2">Loading...</h4>
        </div>
      </template>
    </Suspense>
  </main>
</template>
