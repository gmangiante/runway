<script setup lang="ts">
// Target-feature selector component of model creation
// Only allows selection of NUMERIC columns that are in common among selected data files, thanks to:
// https://stackoverflow.com/questions/37320296/how-to-calculate-intersection-of-multiple-arrays-in-javascript-and-what-does-e
import { computed, ref, getCurrentInstance, onMounted } from 'vue'
import type { PropType } from 'vue'
import type { DatasetAnalysis } from '@/models/DatasetAnalysis'
import { MDBDatatable, MDBSelect, MDBTable } from 'mdb-vue-ui-kit'

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
        .map(c => Object.keys(c).filter(k => c[k].dtype.startsWith('float') || c[k].dtype.startsWith('int')).map(k => c[k].name))
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
    selectedFeatures.value = [] as String[]
    doEmitSelectedFeatures()
}

const potentialFeatures = computed(() => potentialTargets.value.filter(t => t != selectedTarget.value))
const featureTableData = computed(() => { return {
    columns: [
        { label: 'Feature', field: 'feature', sort: true }
    ],
    rows: potentialFeatures.value.map(f => { return { 'feature': f  }})
}})
const selectedFeatures = ref([] as String[])
const doEmitSelectedFeatures = () => {
    currentInst?.emit('featuresSelected', { selectedFeatures: selectedFeatures.value })
}
const handleFeaturesSelected = ( rows: any[] ) => {
    selectedFeatures.value = rows.map(row => row.feature)
    doEmitSelectedFeatures()
}

onMounted(() => { doEmitSelectedTarget(); doEmitSelectedFeatures(); })

</script>
<template>
    <div>
        <span><strong>Target</strong></span>
        <MDBSelect v-model:options="potentialTargetsAsOptions" v-model:selected="selectedTarget" @change="doEmitSelectedTarget" />
        <MDBDatatable v-if="selectedTarget !== ''" :dataset="featureTableData" selectable multi @selected-rows="handleFeaturesSelected"/>
    </div>
</template>