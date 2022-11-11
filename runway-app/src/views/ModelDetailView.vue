<script setup lang="ts">
import ModelDetail from '@/components/ModelDetail.vue';
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
            <MDBBreadcrumbItem><a href="/models">Models</a></MDBBreadcrumbItem>
            <MDBBreadcrumbItem active>
              Model detail
            </MDBBreadcrumbItem>
          </MDBBreadcrumb>
        </nav>
        <ModelDetail :id="id" />
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
