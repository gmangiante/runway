<script setup lang="ts">
// https://stackoverflow.com/questions/37320296/how-to-calculate-intersection-of-multiple-arrays-in-javascript-and-what-does-e
import { computed, ref, getCurrentInstance, onMounted } from 'vue'
import type { PropType } from 'vue'
import type { DatasetAnalysis } from '@/models/DatasetAnalysis'
import { MDBSelect } from 'mdb-vue-ui-kit'

const props = defineProps({
    analysis: Object as PropType<DatasetAnalysis>
})
defineEmits({
    targetSelected(args: { selectedTarget: string }) { return true },
    featuresSelected(args: { selectedFeatures: string[] }) { return true }
})
const currentInst = getCurrentInstance()

const potentialTargets = computed(() => {
    if (!props.analysis) return []
    const colNames = Object.keys(props.analysis!.value as any as DatasetAnalysis).map(f => (props.analysis!.value as any as DatasetAnalysis)[f].columns)
        .map(c => Object.keys(c).map(k => c[k].name))
    return colNames.reduce((intersection, array) => {
        return intersection.filter(intersectedItem => array.some(item => intersectedItem === item));
    }, colNames[0]).filter(c => !c.startsWith('Unnamed'))
})
const potentialTargetsAsOptions = computed(() => potentialTargets.value ? potentialTargets.value
    .map(t => { return { text: t, value: t}})
    : [])
const selectedTarget = ref('')
const doEmitSelectedTarget = () => {
    currentInst?.emit('targetSelected', { selectedTarget: selectedTarget.value })
    doEmitSelectedFeatures()
}

const potentialFeatures = computed(() => potentialTargets.value.filter(t => t != selectedTarget.value))
const doEmitSelectedFeatures = () => {
    currentInst?.emit('featuresSelected', { selectedFeatures: potentialFeatures.value })
}

onMounted(() => { doEmitSelectedTarget(); doEmitSelectedFeatures(); })

</script>
<template>
    <div>
        <MDBSelect v-model:options="potentialTargetsAsOptions" v-model:selected="selectedTarget" @change="doEmitSelectedTarget" />
        <span v-if="selectedTarget !== ''">{{potentialFeatures}}</span>
    </div>
</template>