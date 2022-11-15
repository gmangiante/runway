<script setup lang="ts">
import { computed } from 'vue'
import type { PropType } from 'vue'
import { ref } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue'
import { useFetch } from '@/composables/fetch'
import type { Model } from '@/models/Model'
import { ModelDatafileAssociation } from '@/models/Model'
import type { Dataset } from '@/models/Dataset'
import router from '@/router'
import { MDBBtn, MDBSpinner } from 'mdb-vue-ui-kit'

const props = defineProps({
    model: Object as PropType<Model>
})

const { user, isAuthenticated } = $(useAuth0())
const isOwner = ref(user?.email && (user.email === props.model?.created_by))
const isFitting = ref(false)

const fitModel = async () => {
    isFitting.value = true
    const fitFetch = await useFetch<{success: Boolean}>(`http://localhost:5000/api/models/fit/${props.model?.id}`, 
        { method: 'POST' })
    if (fitFetch.data.value?.success) {
        console.log(fitFetch.data.value)
    }
    isFitting.value = false
}

const deleteModel = async () => {
    const delFetch = await useFetch<{success: Boolean}>(`http://localhost:5000/api/models/${props.model?.id}`, 
        { method: 'DELETE' })
    if (delFetch.data.value?.success) {
        await router.push({ name: 'modelList', replace: true, force: true})
    }
}

const dupModel = async() => {
    if (props.model) {
        await router.push({ name: 'createModel', params: { dataset_id: props.model.dataset_id }, query: { 'dup': props.model.id}, replace: true, force: true })
    }
}

const isTrained = computed(() => props.model && props.model.train_score != 0 && props.model.val_score != 0)

</script>

<template>
    <MDBBtn color="primary" v-if="isOwner && !isTrained" @click="fitModel()">Train</MDBBtn>
    <MDBBtn color="primary" v-if="isAuthenticated" @click="dupModel()">Duplicate</MDBBtn>
    <MDBBtn color="danger" v-if="isOwner" @click="deleteModel()">Delete</MDBBtn>
    <div v-if="isFitting" class="mt-3">
        <MDBSpinner /> Fitting in progress...
    </div>
</template>