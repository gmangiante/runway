<script setup lang="ts">
// This is the component to display histograms/value-counts per-file per-column
// Can display as chart or table
// Useful chart options thanks to:
// https://www.educative.io/answers/chartjs---create-a-histogram
import type { PropType } from 'vue'
import { ref, computed } from 'vue'
import type { DatafileAnalysis } from '@/models/DatasetAnalysis'
import { MDBChart, MDBDatatable, MDBSwitch, MDBSelect } from 'mdb-vue-ui-kit'

const props = defineProps({
    analysis: Object as PropType<DatafileAnalysis>
})

const selectedCol = ref('')
const colOptions = computed(() =>
    props.analysis?.distributions
    ? props.analysis.distributions.map(d =>{ return { 'text': d.column, 'value': d.column } })
    : [])

const viewCharts = ref(true)
const labels = computed(() => props.analysis?.distributions && selectedCol.value != ''
    ? props.analysis.distributions.find(d => d.column === selectedCol.value)?.distribution.map(x => x.value)
    : [])
const data = computed(() => props.analysis?.distributions && selectedCol.value != ''
    ? props.analysis.distributions.find(d => d.column === selectedCol.value)?.distribution.map(x => x.occurrences)
    : [])
const chartData = computed(() => { return {
    labels: labels.value, datasets: Array({ label: '# Occurrences', data: data.value})} } )

const tableColumns = [
  { label: 'Value', field: 'value', sort: true },
  { label: 'Occurrences', field: 'occurrences', sort: true }
]
const tableData = computed(() => { return { columns: tableColumns, rows: 
    selectedCol.value && props.analysis?.distributions
    ? props.analysis.distributions.find(d => d.column === selectedCol.value)!.distribution
    : [] }})

const tableLoading = ref(false)


const chartOptions = {
    scales: {
      xOne: {
        display: false,
        barPercentage: 1.3,
        ticks: {
          max: 3,
        }
      },  
      y: {
        ticks: {
          beginAtZero: true
        }
      }
    }
  }

</script>

<template>
    <div>
        <div class="d-flex">
          <span class="p-1">Column</span>
          <MDBSelect v-model:options="colOptions" v-model:selected="selectedCol" style="max-width: 400px" class="ms-2" />
        </div>
          <template v-if="viewCharts">
            <MDBChart id="distChart" type="bar" style="max-width: 500px; max-height: 500px" :data="chartData" :options="chartOptions" />
        </template>
        <template v-else>
            <MDBDatatable :dataset="tableData" :loading="tableLoading" :max-width="750" />
        </template>
        <MDBSwitch v-if="!data || data.length > 0" :label="viewCharts ? 'View as charts' : 'View as tables'" v-model="viewCharts" /> 
    </div>
</template>