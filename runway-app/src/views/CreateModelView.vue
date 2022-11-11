<script setup lang="ts">
import { Dataset } from '@/models/Dataset'
import { reactive } from 'vue'
import { MDBInput, MDBCard, MDBCardBody, MDBBreadcrumb, MDBBreadcrumbItem, MDBCheckbox, MDBBtn, MDBRow, MDBCol, MDBSpinner } from 'mdb-vue-ui-kit';
import { useAuth0 } from '@auth0/auth0-vue';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import router from '@/router';
import CreateModel from '@/components/CreateModel.vue'

defineProps({
    dataset_id: String
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
              Create new model
            </MDBBreadcrumbItem>
          </MDBBreadcrumb>
        </nav>
        <CreateModel :dataset_id="dataset_id" />
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
