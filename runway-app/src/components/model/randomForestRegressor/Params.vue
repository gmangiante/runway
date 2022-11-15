<script setup lang="ts">
// Random forest regression parameters
// # estimators, criterion, min_samples_split, min_samples_leaf, max_features
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
    n_estimators: 100,
    criterion: 'squared_error',
    min_samples_split: 2,
    min_samples_leaf: 1,
    max_features: 1.0
})

const criterionOptions = [
    {'text': 'squared error', value: 'squared_error' },
    {'text': 'absolute error', value: 'absolute_error' },
    {'text': 'poisson', value: 'poisson' },
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
    <MDBInput class="mt-3" v-model="params['n_estimators']" label="# estimators" @vnode-updated="handleParamsChanged()" />
    <MDBSelect class="mt-3" v-model:options="criterionOptions" v-model:selected="params['criterion']" label="Criterion"  @vnode-updated="handleParamsChanged()" />
    <MDBInput class="mt-3" v-model="params['min_samples_split']" label="Min samples to split" @vnode-updated="handleParamsChanged()" />
    <MDBInput class="mt-3" v-model="params['min_samples_leaf']" label="Min samples per leaf" @vnode-updated="handleParamsChanged()" />
    <MDBInput class="mt-3" v-model="params['max_features']" label="Max # features" @vnode-updated="handleParamsChanged()" />
</template>