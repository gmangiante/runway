<script setup lang="ts">
import type { PropType } from 'vue'
import { ref, computed } from 'vue'
import type { DatafileAnalysis } from '@/models/DatasetAnalysis'
import { MDBChart, MDBDatatable, MDBSwitch } from 'mdb-vue-ui-kit'

const props = defineProps({
    analysis: Object as PropType<DatafileAnalysis>
})

const viewCharts = ref(true)
const labels = computed(() => props.analysis?.unique ?
    props.analysis.unique.map(col => col.column)
    : [])
const data = computed(() => props.analysis?.unique ?
        props.analysis.unique.map(col => col.unique_val_count)
        : [])
const chartData = computed(() => { return {
    labels: labels.value, datasets: Array({ label: '# unique values', data: data.value})} } )

const tableColumns = [
  { label: 'Column', field: 'name', sort: true },
  { label: 'Unique values', field: 'unique_val_count', sort: true }
]
const tableData = { columns: tableColumns, rows: props.analysis?.unique ?
    props.analysis.unique.map(col => { return { name: col.column, unique_val_count: col.unique_val_count } })
    : [] }
const tableLoading = ref(false)
</script>

<template>
    <div>
        <template v-if="viewCharts">
            <MDBChart id="uniqueChart" type="bar" style="max-width: 500px; max-height: 500px" :data="chartData" />
        </template>
        <template v-else>
            <MDBDatatable :dataset="tableData" :loading="tableLoading" :max-width="750" />
        </template>
        <MDBSwitch v-if="data.length > 0" :label="viewCharts ? 'View as charts' : 'View as tables'" v-model="viewCharts" /> 
    </div>
</template>