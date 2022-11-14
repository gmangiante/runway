<script setup lang="ts">
import type { PropType } from 'vue'
import { ref, computed } from 'vue'
import type { DatafileAnalysis } from '@/models/DatasetAnalysis'
import { MDBChart, MDBDatatable, MDBSwitch } from 'mdb-vue-ui-kit'

const props = defineProps({
    analysis: Object as PropType<DatafileAnalysis>
})

const viewCharts = ref(true)
const minValue = computed(() => props.analysis ? Math.min(...props.analysis.corr.map(c => c.corr_val)) * 100 : 0)
const maxValue = computed(() => props.analysis ? Math.max(...props.analysis.corr.map(c => c.corr_val)) * 100 : 0)
const colors = ["#E3F2FD", "#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5"]
const step = computed(() => (maxValue.value - minValue.value) / (colors.length - 1))
const format = computed(() =>
    props.analysis ?
    props.analysis.corr.map(c => {
        const colorIndex = Math.floor(Math.floor(c.corr_val * 100 - minValue.value) / step.value)
        return {
            backgroundColor: colors[colorIndex],
            fontWeight: 400
        };
    }) : [])
const tableColumns = computed(() => props.analysis ? [{ label: 'Column', field: 'column'} ].concat(Object.keys(props.analysis.columns).map(c =>
    { return { label: props.analysis!.columns[c].name, field: props.analysis!.columns[c].name, /*format*/ }})) : [])
const tableRows = computed(() => props.analysis ? Object.keys(props.analysis.columns).map(col1 =>
    props.analysis!.corr.filter(c => c.column1 === props.analysis!.columns[col1].name)
    .reduce((p, c) => { return {...p, [c.column2]: c.corr_val } }, { 'column': props.analysis!.columns[col1].name })
    ) : [])
const tableData = computed(() => { return { columns: tableColumns.value, rows: tableRows.value}})
const tableLoading = ref(false)
</script>

<template>
    <div>
        <MDBDatatable :dataset="tableData" :loading="tableLoading" :max-width="750" />
    </div>
</template>