<script setup lang="ts">
import { Dataset } from '@/models/Dataset'
import { reactive } from 'vue'
import { MDBInput, MDBCard, MDBCardBody, MDBCheckbox, MDBBtn, MDBRow, MDBCol, MDBCardFooter } from 'mdb-vue-ui-kit';
import { useAuth0 } from '@auth0/auth0-vue';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import router from '@/router';

const { user } = $(useAuth0())
const newDataset = reactive(new Dataset(-1, '', false, user.email || 'error', new Date(), new Date()))

async function submitForm(e: Event) {
    e.preventDefault()
    const { isLoading, hasError, errorMessage, data } =
        await useFetch<{ new_dataset_id: number }>('http://localhost:5000/api/datasets/', { method: 'POST', body: JSON.stringify(newDataset) })
    if (!hasError.value && data.value)
        await router.push({ name: 'datasetDetail', params: { id: data.value['new_dataset_id'] } })
}

</script>

<template>
    <MDBCard class="w-50">
        <MDBCardBody>
            <MDBRow tag="form" class="g-3" @submit="submitForm">
                <MDBCol col="12">
                    <MDBInput label="Dataset name" v-model="newDataset.name" class="mb-3" required />
                </MDBCol>
                <MDBCol col="12">
                    <MDBCheckbox label="Public" v-model="newDataset.is_public" />
                </MDBCol>
                <MDBCol col="12">
                    <MDBBtn color="primary" type="submit">Create dataset</MDBBtn>
                    <RouterLink to="/datasets"><MDBBtn color="secondary">Cancel</MDBBtn></RouterLink>
                </MDBCol>
            </MDBRow>
        </MDBCardBody>
    </MDBCard>
</template>
