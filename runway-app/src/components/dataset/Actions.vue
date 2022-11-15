<script setup lang="ts">
// Dataset actions component (delete if owner, create model if authenticated)
import type { PropType } from 'vue'
import { ref } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue'
import { useFetch } from '@/composables/fetch'
import type { Dataset } from '@/models/Dataset'
import router from '@/router'
import { MDBBtn } from 'mdb-vue-ui-kit'

const props = defineProps({
    dataset: Object as PropType<Dataset>
})

const { user, isAuthenticated } = $(useAuth0())
const isOwner = ref(user?.email && (user.email === props.dataset?.created_by))

const deleteDataset = async () => {
    const delFetch = await useFetch<{success: Boolean}>(`https://runway-demo.herokuapp.com/api/datasets/${props.dataset?.id}`, 
        { method: 'DELETE' })
    if (delFetch.data.value?.success) {
        await router.push({ name: 'datasetList', replace: true, force: true})
    }
}
</script>

<template>
    <RouterLink :to="'/models/create/' + dataset?.id" v-if="isAuthenticated">
        <MDBBtn color="primary" class="ms-4 mt-4">Create Model</MDBBtn>
    </RouterLink>
    <MDBBtn v-if="isOwner" color="danger" @click="deleteDataset()">Delete dataset</MDBBtn>
</template>