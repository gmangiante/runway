<script setup lang="ts">
// This is the component to display the datatype summary for a datafile
// Can display as a table or bar chart
// Some fancy grouping thanks to:
// https://stackoverflow.com/questions/1960473/get-all-unique-values-in-a-javascript-array-remove-duplicates
// https://stackoverflow.com/questions/44387647/group-and-count-values-in-an-array

import type { PropType } from 'vue'
import { ref, computed } from 'vue'
import type { DatafileAnalysis } from '@/models/DatasetAnalysis'
import { MDBChart, MDBDatatable, MDBSwitch, MDBBtn } from 'mdb-vue-ui-kit'

const props = defineProps({
    analysis: Object as PropType<DatafileAnalysis>
})

const viewCharts = ref(true)
const labels = computed(() => props.analysis ?
    [...new Set(Object.keys(props.analysis.columns).map(col => props.analysis!.columns[col].dtype))]
    : [])
const data = computed(() => props.analysis ?
        Object.keys(props.analysis.columns).map(x => props.analysis!.columns[x])
        .reduce((p: { [key: string]: number}, c) => {
            const dtype = c.dtype
            if (!p.hasOwnProperty(dtype)) p[dtype] = 0
            p[dtype]++
            return p }, {}) : [])
const chartData = computed(() => { return {
    labels: labels.value, datasets: Array({ label: '# Columns', data: data.value})} } )

const tableColumns = [
  { label: 'Column', field: 'name', sort: true },
  { label: 'Data type', field: 'dtype', sort: true }
]
const tableData = { columns: tableColumns, rows: props.analysis ?
    Object.keys(props.analysis!.columns).map(col => props.analysis!.columns[col])
    : [] }
const tableLoading = ref(false)

const exportImage = async () => {
    const chart = document.getElementById("dataset-viz-chart") as HTMLCanvasElement
    const imageObject = new Image()
    imageObject.src = chart.toDataURL("image/png"); 
    // for later - save viz to database
    /*const dropFetch = await useFetch<{success: Boolean}>
        (`https://runway-demo.herokuapp.com/api/datasets/visualizations/${props.analysis?.dataset_id}`, 
        { method: 'POST', body: imageObject.src })*/
    // or to download
    const link = document.createElement("a")
    link.setAttribute('download', `${props.analysis?.datafile_name}_datatypes.png`)
    link.href = imageObject.src
    link.click()
}
</script>


<template>
    <div>
        <template v-if="viewCharts">
            <MDBChart type="bar" :data="chartData" style="max-width: 500px; max-height: 500px" id="dataset-viz-chart" />
        </template>
        <template v-else>
            <MDBDatatable :dataset="tableData" :loading="tableLoading" :max-width="750" />
        </template>
        <MDBSwitch :label="viewCharts ? 'View as charts' : 'View as tables'" v-model="viewCharts"  />
        <MDBBtn @click="exportImage()" class="ms-3">Save</MDBBtn>
    </div>
</template>