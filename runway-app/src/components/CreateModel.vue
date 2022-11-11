<script setup lang="ts">
import type { Dataset } from '@/models/Dataset'
import { ref} from 'vue'
import { MDBCard, MDBCardBody, MDBRow, MDBCol, MDBSelect } from 'mdb-vue-ui-kit';
import { useAuth0 } from '@auth0/auth0-vue';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import CreateLinearRegression from '@/components/CreateLinearRegression.vue'

const { user } = $(useAuth0())

const props = defineProps({
    dataset_id: String
})

const { isLoading, hasError, errorMessage, data } =
  $(await useFetch<Dataset>(`http://localhost:5000/api/datasets/${props.dataset_id}`))

const modelTypeOptions = ref([
    { text: "Linear Regression", value: "linearRegression" },
    { text: "Logistic Regression", value: "logisticRegression" }
]);
const selectedModelType = ref('');


</script>

<template>
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
</template>
