<script setup lang="ts">
import { ref } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue'
import { useFetch } from '@/composables/fetch'
import type { Model } from '@/models/Model'
import { MDBRow, MDBCol, MDBBreadcrumb, MDBBreadcrumbItem, MDBBtn, MDBIcon } from 'mdb-vue-ui-kit'
import ModelInfo from '@/components/model/Info.vue'
import ModelActions from '@/components/model/Actions.vue'

const props = defineProps({
    id: String
})
const { user } = $(useAuth0())
const { data } = $(await useFetch<Model>(`http://localhost:5000/api/models/${props.id}`))
const isOwner = ref(user?.email === data?.created_by)

const setPublic = async (isPublic: boolean) => {
    const sharingFetch = await useFetch<{success: boolean}>(`http://localhost:5000/api/models/sharing/${data?.id}/${isPublic}`, { method: 'POST'})
    if (!sharingFetch.hasError.value) {
        if (data) data.is_public = isPublic
    }
}
</script>

<template>
  <MDBRow>
    <MDBCol class="d-flex">
        <template v-if="isOwner && data?.is_public">
            <MDBBtn @click="setPublic(false)" floating color="primary">
                <MDBIcon icon="lock" />
            </MDBBtn>
        </template>
        <template v-if="isOwner && !data?.is_public">
            <MDBBtn @click="setPublic(true)" floating color="primary">
                <MDBIcon icon="share-alt" />
            </MDBBtn>
        </template>
        <nav aria-label="breadcrumb" class="ms-2 pt-1">
            <MDBBreadcrumb>
                <MDBBreadcrumbItem><a href="/models">Models</a></MDBBreadcrumbItem>
                <MDBBreadcrumbItem active>{{ data?.name }}</MDBBreadcrumbItem>
            </MDBBreadcrumb>
        </nav>
    </MDBCol>
  </MDBRow> 
  <ModelInfo :model="data || undefined" />
  <ModelActions :model="data || undefined" />
</template>
