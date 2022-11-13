<script setup lang="ts">
import type { PropType } from 'vue'
import type { Model } from '@/models/Model'
import { MDBTable } from 'mdb-vue-ui-kit'

const props = defineProps({
    model: Object as PropType<Model>
})

</script>

<template>
    <MDBTable style="max-width: 750px">
        <tr>
            <th scope="row"><strong>Name</strong></th>
            <td>{{ model?.name }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Author</strong></th>
            <td>{{ model?.created_by }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Created</strong></th>
            <td>{{ model ? new Date(model.created_at).toLocaleString() : '' }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Updated</strong></th>
            <td>{{ model ? new Date(model.updated_at).toLocaleString() : '' }}</td>
        </tr>
        <tr>
            <th scope="row"><strong>Sharing</strong></th>
            <td>{{ model?.is_public ? "Public" : "Private" }}</td>
        </tr>
    </MDBTable>
</template>