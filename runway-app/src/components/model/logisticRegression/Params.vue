<script setup lang="ts">
import { ref, getCurrentInstance, onMounted } from 'vue'
import type { ModelParams } from '@/models/Model'
import { MDBSelect, MDBInput } from 'mdb-vue-ui-kit'

defineEmits({
    paramsChanged(args: { newParams: ModelParams }) { return true }
})
const currentInst = getCurrentInstance()

const penaltyOptions = [
    { text: 'l2', value: 'l2'},
    { text: 'l1', value: 'l1'},
    { text: 'elasticnet', value: 'elasticnet'},
    { text: 'none', value: 'none'}
]

const solverOptions = [
    { text: 'lbfgs', value: 'lbfgs'},
    { text: 'newton-cg', value: 'newton-cg'},
    { text: 'liblinear', value: 'liblinear'},
    { text: 'sag', value: 'sag'},
    { text: 'saga', value: 'saga'}
]

const params = ref({
    'penalty': 'l2',
    'solver': 'lbfgs',
    'C': 1.0,
    'max_iter': 100
})

const handleParamsChanged = () =>
{
    currentInst?.emit('paramsChanged', { newParams: params.value })
}

onMounted(() => handleParamsChanged())

</script>
<template>
    <MDBSelect class="mt-3" v-model:options="penaltyOptions" v-model:selected="params['penalty']" label="Penalty" @vnode-updated="handleParamsChanged()" />
    <MDBSelect class="mt-3" v-model:options="solverOptions" v-model:selected="params['solver']" label="Solver" @vnode-updated="handleParamsChanged()" />
    <MDBInput class="mt-3" v-model="params['C']" label="C" @vnode-updated="handleParamsChanged()" />
    <MDBInput class="mt-3" v-model="params['max_iter']" label="Max iterations" @vnode-updated="handleParamsChanged()" />
</template>