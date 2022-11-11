<script setup lang="ts">
import type { Dataset } from '@/models/Dataset'
import { MDBCard, MDBCardBody, MDBCardFooter, MDBBtn, MDBTable, MDBCardHeader, MDBListGroup, MDBListGroupItem, MDBRow, MDBCol, MDBChart } from 'mdb-vue-ui-kit';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import { useAuth0 } from '@auth0/auth0-vue';
import { ref, computed } from 'vue'
import router from '@/router';

const props = defineProps({
    id: String
})

const { isLoading, hasError, errorMessage, data } =
  $(await useFetch<Dataset>(`http://localhost:5000/api/models/${props.id}`))

async function deleteModel() {
    const delFetch = await useFetch<{success: Boolean}>(`http://localhost:5000/api/models/${data?.id}`, 
        { method: 'DELETE' })
    if (delFetch.data.value?.success) {
        await router.push({ name: 'models', replace: true, force: true})
    }
}

async function fitModel() {
    const fitFetch = await useFetch<{success: Boolean}>(`http://localhost:5000/api/models/fit/${data?.id}`, 
        { method: 'POST' })
    if (fitFetch.data.value?.success) {
        console.log(fitFetch.data.value)
    }
}

const { user } = $(useAuth0())

const isOwner = ref(user.email === data?.created_by)

</script>

<template>
    <main>
        <MDBCard class="w-100">
            <MDBCardBody>
                <MDBTable>
                    <tr>
                        <th scope="row">Name</th>
                        <td>{{ data?.name }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Public</th>
                        <td>{{ data?.is_public }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Created by</th>
                        <td>{{ data?.created_by }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Created at</th>
                        <td>{{ data?.created_at }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Updated at</th>
                        <td>{{ data?.updated_at }}</td>
                    </tr>
                </MDBTable>
            </MDBCardBody>
            <MDBCardFooter>
                <MDBBtn color="primary" v-if="isOwner" @click="fitModel()">Fit model</MDBBtn>
                <RouterLink to="/models"><MDBBtn color="primary">Go back</MDBBtn></RouterLink>
                <MDBBtn color="danger" v-if="isOwner" @click="deleteModel()">Delete model</MDBBtn>
            </MDBCardFooter>
        </MDBCard>
    </main>
</template>