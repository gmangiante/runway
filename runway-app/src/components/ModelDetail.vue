<script setup lang="ts">
import type { Dataset } from '@/models/Dataset'
import { MDBCard, MDBCardBody, MDBCardFooter, MDBBtn, MDBTable, MDBCardHeader, MDBListGroup, MDBListGroupItem, MDBRow, MDBCol, MDBChart, MDBIcon, MDBToast, MDBSpinner } from 'mdb-vue-ui-kit';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import { useAuth0 } from '@auth0/auth0-vue';
import { ref } from 'vue'
import router from '@/router'

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
    isFitting.value = true
    const fitFetch = await useFetch<{success: Boolean}>(`http://localhost:5000/api/models/fit/${data?.id}`, 
        { method: 'POST' })
    if (fitFetch.data.value?.success) {
        console.log(fitFetch.data.value)
    }
    isFitting.value = false
}

const { user } = $(useAuth0())

const isOwner = ref(user.email === data?.created_by)


async function setPublic(isPublic: boolean) {
    const sharingFetch = await useFetch<{success: boolean}>(`http://localhost:5000/api/models/sharing/${data?.id}/${isPublic}`, { method: 'POST'})
    if (!sharingFetch.hasError.value) {
        if (data) data.is_public = isPublic
    }
}

const isFitting = ref(false)


</script>

<template>
        <MDBCard border="dark" style="max-width: 800px" >
        <MDBCardHeader border="dark">
            <MDBRow>
                <MDBCol col="8">Dataset info</MDBCol>
                <MDBCol col="3">
                    <span><strong>Sharing:</strong> {{ data?.is_public ? "Public" : "Private" }}</span>
                </MDBCol>
                <MDBCol col="1">
                    <template v-if="isOwner && data?.is_public">
                        <MDBBtn @click="setPublic(false)" floating color="primary" class="me-2">
                            <MDBIcon icon="lock" />
                        </MDBBtn>
                    </template>
                    <template v-if="isOwner && !data?.is_public">
                        <MDBBtn @click="setPublic(true)" floating color="primary" class="me-2">
                            <MDBIcon icon="share-alt" />
                        </MDBBtn>
                    </template>
                </MDBCol>
            </MDBRow>
        </MDBCardHeader>
        <MDBCardBody>
            <MDBRow>
                <MDBCol col="3"><strong>Name</strong></MDBCol>
                <MDBCol col="9">{{ data?.name }}</MDBCol>
            </MDBRow>
            <MDBRow>
                <MDBCol col="3"><strong>Author</strong></MDBCol>
                <MDBCol col="9">{{ data?.created_by }}</MDBCol>
            </MDBRow>
            <MDBRow>
                <MDBCol col="3"><strong>Created</strong></MDBCol>
                <MDBCol col="9">{{ data ? new Date(data.created_at).toLocaleString() : "" }}</MDBCol>
            </MDBRow>
            <MDBRow>
                <MDBCol col="3"><strong>Updated</strong></MDBCol>
                <MDBCol col="9">{{ data ? new Date(data.updated_at).toLocaleString() : "" }}</MDBCol>
            </MDBRow>
        </MDBCardBody>
        <MDBCardFooter border="dark">
            <MDBBtn color="primary" v-if="isOwner" @click="fitModel()">Fit model</MDBBtn>
            <MDBBtn color="danger" v-if="isOwner" @click="deleteModel()">Delete model</MDBBtn>
            <div v-if="isFitting" class="mt-3">
                <MDBSpinner /> Fitting in progress...
            </div>
        </MDBCardFooter>
    </MDBCard>
</template>