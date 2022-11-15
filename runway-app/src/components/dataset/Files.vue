<script setup lang="ts">
// Files subcomponent of dataset detail
// Allows download (if authenticated), delete (if owner)
// TODO should also be able to add new files here, not yet
import type { PropType } from 'vue'
import { ref } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue';
import { useFetch } from '@/composables/fetch'
import type { Dataset } from '@/models/Dataset'
import { MDBRow, MDBCol, MDBIcon, MDBBtn } from 'mdb-vue-ui-kit';

const props = defineProps({
    dataset: Object as PropType<Dataset>
})

const { user } = $(useAuth0())
const isOwner = ref(user?.email && (user.email === props.dataset?.created_by))

const downloadFile = async (datafile_id: number, datafile_name: string) => {
    const fileDownload = await useFetch<Blob>(`https://runway-demo.herokuapp.com/api/datasets/datafiles/${datafile_id}`)

    if (!fileDownload.hasError.value) {
        let link = document.createElement('a')
        link.href = window.URL.createObjectURL(fileDownload.blob.value as Blob)
        link.download = datafile_name
        document.body.appendChild(link);
        link.click()
        document.body.removeChild(link);
    }
}

const deleteFile = async (datafile_id: number) => {
    const delFetch = await useFetch<{success: Boolean}>(`https://runway-demo.herokuapp.com/api/datasets/datafiles/${datafile_id}`, 
        { method: 'DELETE' })
    if (delFetch.data.value?.success) {
        props.dataset?.files?.splice(props.dataset?.files?.findIndex(file => file.id === datafile_id), 1)
    }
}

</script>

<template>
    <strong class="ms-4"><u>Files</u></strong>
    <MDBRow v-for="file in props.dataset?.files" style="max-width: 750px">
        <div class="d-flex align-items-center mt-2">
            <span class="ms-4">{{ file.name }}</span>
            <MDBBtn v-if="isOwner || props.dataset?.is_public" @click="downloadFile(file.id, file.name)"
                floating color="primary" class="ms-2 me-2">
                <MDBIcon icon="download" />
            </MDBBtn>
            <MDBBtn v-if="isOwner" @click="deleteFile(file.id)" floating color="danger">
                <MDBIcon icon="trash" />
            </MDBBtn>
        </div>
    </MDBRow>
</template>