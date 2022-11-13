<script setup lang="ts">
import { ref } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue';
import { useFetch } from '@/composables/fetch'
import type { Dataset } from '@/models/Dataset'
import { MDBCard, MDBCardBody, MDBBreadcrumb, MDBBreadcrumbItem, MDBRow, MDBCol, MDBSelect, MDBSpinner } from 'mdb-vue-ui-kit';
import CreateLinearRegression from '@/components/model/linearRegression/Create.vue'

const props = defineProps({
    dataset_id: String
})

const { user } = $(useAuth0())

const { data } = $(await useFetch<Dataset>(`http://localhost:5000/api/datasets/${props.dataset_id}`))

const modelTypeOptions = ref([
    { text: "Linear Regression", value: "linearRegression" },
    { text: "Logistic Regression", value: "logisticRegression" }
]);

const selectedModelType = ref('');
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
        <MDBCard class="w-50">
          <MDBCardBody>
              <MDBRow class="g-3">
                  <MDBCol col="12">
                      Dataset name: {{ data?.name }}
                  </MDBCol>
                  <MDBCol col="12">
                      <MDBSelect v-model:options="modelTypeOptions" v-model:selected="selectedModelType" />
                  </MDBCol>
                  <MDBCol col="12">
                      <template v-if="selectedModelType == 'linearRegression'">
                          <CreateLinearRegression :dataset="data || undefined" />
                      </template>
                  </MDBCol>
              </MDBRow>
          </MDBCardBody>
      </MDBCard>
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