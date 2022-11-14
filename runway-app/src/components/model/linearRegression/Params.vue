<script setup lang="ts">
import { ref, getCurrentInstance, onMounted } from 'vue'
import type { ModelParams } from '@/models/Model'
import { MDBCheckbox } from 'mdb-vue-ui-kit'

const props = defineProps({
    modelType: String
})
defineEmits({
    paramsChanged(args: { newParams: ModelParams }) { return true }
})
const currentInst = getCurrentInstance()

const params = ref({
    'fit_intercept': true,
    'normalize': false,
    'positive': false
})

const handleParamsChanged = () =>
{
    currentInst?.emit('paramsChanged', { newParams: params.value })
}

onMounted(() => handleParamsChanged())

</script>
<template>
    <MDBCheckbox v-model="params['fit_intercept']" label="Fit Intercept" @vnode-updated="handleParamsChanged()" />
    <MDBCheckbox v-model="params['normalize']" label="Normalize" @vnode-updated="handleParamsChanged()" />
    <MDBCheckbox v-model="params['positive']" label="Positive" @vnode-updated="handleParamsChanged()" />
</template>