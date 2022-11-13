<script setup lang="ts">
import { Dataset } from '@/models/Dataset'
import { reactive, ref } from 'vue'
import { MDBInput, MDBCard, MDBCardBody, MDBBtn, MDBRow, MDBCol, MDBSwitch, MDBCardTitle, MDBFile, MDBListGroup, MDBListGroupItem, MDBCardHeader, MDBCardFooter } from 'mdb-vue-ui-kit';
import { useAuth0 } from '@auth0/auth0-vue';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import router from '@/router';
import DropZone from '../components/DropZone.vue'
import FilePreview from '../components/FilePreview.vue'
import { useFileUpload } from '@/composables/fileUpload';

const { user } = $(useAuth0())
const newDataset = reactive(new Dataset(-1, '', false, user.email || 'error', new Date(), new Date(), []))

const { files, addFiles, removeFile, uploadFiles } = useFileUpload()

function onInputChange(e: any) {
	addFiles(e.target.files)
}

async function submitForm(e: Event) {
    e.preventDefault()
    let { isLoading, hasError, errorMessage, data } =
        await useFetch<{ new_dataset_id: number }>('http://localhost:5000/api/datasets/', { method: 'POST', body: JSON.stringify(newDataset) })
    if (!hasError.value && data.value) {
        const id = data.value['new_dataset_id']
        const upload_url = `http://localhost:5000/api/datasets/datafiles/${user.email}/${id}`
        await uploadFiles(upload_url)
        await router.push({ name: 'datasetDetail', params: { id: id }, replace: true, force: true })
    }
}

</script>

<template>
    <MDBCol tag="form" class="g-3" @submit="submitForm">
        <MDBCard border="dark" style="max-width: 800px">
            <MDBCardHeader border="dark">Dataset info</MDBCardHeader>
            <MDBCardBody>
                <MDBRow>
                    <MDBCol col="12">
                        <MDBInput label="Dataset name" v-model="newDataset.name" class="mb-3" required />
                    </MDBCol>
                    <MDBCol col="12">
                        <MDBSwitch :label="newDataset.is_public ? 'Public' : 'Private'" v-model="newDataset.is_public" />
                    </MDBCol>
                </MDBRow>
            </MDBCardBody>
        </MDBCard>
        <MDBCard border="dark" style="max-width: 800px" class="mt-3">
            <MDBCardHeader border="dark">Files</MDBCardHeader>
            <MDBCardBody>
                <MDBRow>
                    <MDBCol col="12">
                        <DropZone @files-dropped="addFiles" #default="{ dropZoneActive }">
                            <MDBCardTitle v-if="dropZoneActive">
                                Drop here
                            </MDBCardTitle>
                            <MDBCardTitle v-else>
                                Drag files here or
                            </MDBCardTitle>
                            <MDBFile multiple @change="onInputChange" />
                            <MDBListGroup flush v-show="files.length">
                                <MDBListGroupItem v-for="file of files" :key="file.id" >
                                    <FilePreview :file="file" @remove="removeFile" />
                                </MDBListGroupItem>
                            </MDBListGroup>
                        </DropZone>
                    </MDBCol>
                </MDBRow>
            </MDBCardBody>
            <MDBCardFooter border="dark">
                <MDBRow>
                    <MDBCol col="12">
                        <MDBBtn color="primary" type="submit">Create dataset</MDBBtn>
                        <RouterLink to="/datasets"><MDBBtn color="secondary">Cancel</MDBBtn></RouterLink>
                    </MDBCol>
                </MDBRow>
            </MDBCardFooter>
        </MDBCard>
    </MDBCol>
</template>

<style>
    .drop-zone { background-color: red;}
</style>