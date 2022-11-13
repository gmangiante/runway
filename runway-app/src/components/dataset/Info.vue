<script setup lang="ts">
import type { PropType } from 'vue'
import type { Dataset } from '@/models/Dataset'
import { MDBTable } from 'mdb-vue-ui-kit'
import DatasetFiles from '@/components/dataset/Files.vue'

const props = defineProps({
    dataset: Object as PropType<Dataset>
})

</script>

<template>
    <MDBTable style="max-width: 750px">
        <tr>
            <th scope="row"><strong>Name</strong></th>
            <td>{{ props.dataset?.name }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Author</strong></th>
            <td>{{ props.dataset?.created_by }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Created</strong></th>
            <td>{{ props.dataset ? new Date(props.dataset.created_at).toLocaleString() : '' }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Updated</strong></th>
            <td>{{ props.dataset ? new Date(props.dataset.updated_at).toLocaleString() : '' }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Sharing</strong></th>
            <td>{{ props.dataset?.is_public ? "Public" : "Private" }}</td>
        </tr>
    </MDBTable>

    <DatasetFiles :dataset="dataset" />
</template>