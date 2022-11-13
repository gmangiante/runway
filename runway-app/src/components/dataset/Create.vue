<script setup lang="ts">
import { reactive } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue';
import { useFetch } from '@/composables/fetch'
import { useFileUpload } from '@/composables/fileUpload';
import router from '@/router';
import { Dataset } from '@/models/Dataset'
import { MDBBreadcrumb, MDBBreadcrumbItem, MDBInput, MDBBtn,
    MDBRow, MDBSwitch, MDBCardTitle, MDBFile, MDBListGroup, MDBListGroupItem } from 'mdb-vue-ui-kit';
import DropZone from '@/components/DropZone.vue'
import FilePreview from '@/components/FilePreview.vue'

const { user } = $(useAuth0())
const { files, addFiles, removeFile, uploadFiles } = useFileUpload()
const newDataset = reactive(new Dataset(-1, '', false, user.email || 'error', new Date(), new Date(), [], []))

const onInputChange = (e: any) => {
	addFiles(e.target.files)
}

const submitForm = async (e: Event) => {
    e.preventDefault()
    const { hasError, data } = await useFetch<{ new_dataset_id: number }>('http://localhost:5000/api/datasets/',
        { method: 'POST', body: JSON.stringify(newDataset) })
    if (!hasError.value && data.value) {
        const id = data.value['new_dataset_id']
        await uploadFiles(`http://localhost:5000/api/datasets/datafiles/${user.email}/${id}`)
        await router.push({ name: 'datasetDetail', params: { id: id }, replace: true, force: true })
    }
}
</script>

<template>
    <nav aria-label="breadcrumb">
        <MDBBreadcrumb>
            <MDBBreadcrumbItem><a href="/datasets">Datasets</a></MDBBreadcrumbItem>
            <MDBBreadcrumbItem active>Create new dataset</MDBBreadcrumbItem>
        </MDBBreadcrumb>
    </nav>
    <MDBRow tag="form" class="g-3" @submit="submitForm" style="max-width: 750px">
        <MDBInput label="Dataset name" v-model="newDataset.name" class="mb-3" required />
        <MDBSwitch :label="newDataset.is_public ? 'Public' : 'Private'" v-model="newDataset.is_public" />
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
        <div>
            <MDBBtn color="primary" type="submit">Create dataset</MDBBtn>
            <RouterLink to="/datasets"><MDBBtn color="secondary">Cancel</MDBBtn></RouterLink>
        </div>
    </MDBRow>
</template>