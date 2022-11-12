<script setup lang="ts">
import type { Dataset } from '@/models/Dataset'
import { MDBCard, MDBCardBody, MDBCardFooter, MDBBtn, MDBTable, MDBCardHeader, MDBListGroup, MDBListGroupItem, MDBRow, MDBCol, MDBChart, MDBToast, MDBSpinner } from 'mdb-vue-ui-kit';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import { useAuth0 } from '@auth0/auth0-vue';
import { ref, computed } from 'vue'
import router from '@/router'
import { transformStyle } from '@vue/compiler-dom';

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

const evtSource = new EventSource("//localhost:5000/events?channel=model_fit", { withCredentials: true } )

evtSource.addEventListener("start", (event) => {
    const event_json = JSON.parse(event.data)
    if (event_json['model_id'] == data?.id) {
        toast.value.show = false
        isFitting.value = true
    }
})

evtSource.addEventListener("complete", (event) => {
    const event_json = JSON.parse(event.data)
    if (event_json['model_id'] == data?.id) {
        isFitting.value = false
        toast.value.model_name = data?.name || ''
        toast.value.train_score = event_json['train_score']
        toast.value.val_score = event_json['val_score']
        toast.value.show = true
    }
})

const isFitting = ref(false)
const toast = ref({show: false, model_name: '', train_score: 0, val_score: 0})

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
        <span v-if="isFitting">
            <MDBSpinner /> Fitting in progress...
        </span>
        <MDBToast
            v-model="toast.show"
            :position="'bottom-right'"
            width="350px"
            toast="primary"
            
        >
            <template #title> {{ toast.model_name }} </template>
            <template #small> Fit complete </template>
            train: {{ toast.train_score}}, val: {{ toast.val_score }}
        </MDBToast>
    </main>
</template>