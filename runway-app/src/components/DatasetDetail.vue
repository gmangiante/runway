<script setup lang="ts">
import type { Dataset } from '@/models/Dataset'
import { reactive } from 'vue'
import { MDBCard, MDBCardBody, MDBCardFooter, MDBBtn, MDBTable } from 'mdb-vue-ui-kit';
import { useAuth0 } from '@auth0/auth0-vue';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'

const props = defineProps({
    id: String
})

const { isLoading, hasError, errorMessage, data } =
  $(await useFetch<Dataset>(`http://localhost:5000/api/datasets/${props.id}`))

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
                <RouterLink to="/datasets"><MDBBtn color="primary">Go back</MDBBtn></RouterLink>
            </MDBCardFooter>
        </MDBCard>
    </main>
</template>