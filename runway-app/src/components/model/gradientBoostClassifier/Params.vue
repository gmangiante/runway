<script setup lang="ts">
// Gradient boost classifier parameters
// loss, learning rate, # estimators, min_samples_leaf, max_depth
import { ref, getCurrentInstance, onMounted, type PropType } from 'vue'
import type { ModelParams } from '@/models/Model'
import { MDBInput, MDBSelect } from 'mdb-vue-ui-kit'

const props = defineProps({
    existingParams: Object as PropType<ModelParams>
})

defineEmits({
    paramsChanged(args: { newParams: ModelParams }) { return true }
})
const currentInst = getCurrentInstance()

const params = ref({
    loss: 'log_loss',
    learning_rate: 0.1,
    n_estimators: 100,
    min_samples_leaf: 1,
    max_depth: 3
})

const lossOptions = [
    { text: 'log_loss', value: 'log_loss'},
    { text: 'deviance', value: 'deviance'},
    { text: 'exponential', value: 'exponential'}
]

const handleParamsChanged = () =>
{
    currentInst?.emit('paramsChanged', { newParams: params.value })
}

onMounted(() => {
    if (props.existingParams) Object.assign(params.value, props.existingParams)
    console.log(params.value)
    handleParamsChanged()
})

</script>
<template>
    <MDBSelect class="mt-3" v-model:options="lossOptions" v-model:selected="params['loss']" label="Loss" @vnode-updated="handleParamsChanged()" />
    <MDBInput class="mt-3" v-model="params['learning_rate']" label="Learning rate" @vnode-updated="handleParamsChanged()" />
    <MDBInput class="mt-3" v-model="params['n_estimators']" label="# estimators" @vnode-updated="handleParamsChanged()" />
    <MDBInput class="mt-3" v-model="params['min_samples_leaf']" label="Min samples per leaf" @vnode-updated="handleParamsChanged()" />
    <MDBInput class="mt-3" v-model="params['max_depth']" label="Max tree depth" @vnode-updated="handleParamsChanged()" />
</template>