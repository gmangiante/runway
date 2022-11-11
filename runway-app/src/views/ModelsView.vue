<script setup lang="ts">
import ModelsTable from '@/components/ModelsTable.vue'
import { MDBBtn, MDBSpinner, MDBBreadcrumb, MDBBreadcrumbItem } from 'mdb-vue-ui-kit';
</script>

<template>
  <main>
    <Suspense>
      <div>
        <nav aria-label="breadcrumb">
          <MDBBreadcrumb>
            <MDBBreadcrumbItem active>Models</MDBBreadcrumbItem>
          </MDBBreadcrumb>
        </nav>
        <!--<RouterLink to="/models/create" custom v-slot="{ navigate }" v-if="$auth0.isAuthenticated.value">
          <MDBBtn @click="navigate" role="link" color="primary" class="m-3">Add Model</MDBBtn>
        </RouterLink>-->
        <ModelsTable />
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
