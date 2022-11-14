<script setup lang="ts">
import type { PropType } from 'vue'
import { ref, computed } from 'vue'
import type { DatafileAnalysis } from '@/models/DatasetAnalysis'
import { MDBChart, MDBDatatable, MDBSwitch } from 'mdb-vue-ui-kit'

const props = defineProps({
    analysis: Object as PropType<DatafileAnalysis>
})

const viewCharts = ref(true)
const labels = computed(() => props.analysis ?
    Object.keys(props.analysis.nulls).filter(x => props.analysis!.nulls[x] > 0)
    : [])
const data = computed(() => props.analysis ?
        Object.keys(props.analysis.nulls).filter(x => props.analysis!.nulls[x] > 0)
            .map(x => props.analysis!.nulls[x])
        : [])
const chartData = computed(() => { return {
    labels: labels.value, datasets: Array({ label: 'Nulls', data: data.value})} } )

const tableColumns = [
  { label: 'Column', field: 'name', sort: true },
  { label: 'Nulls', field: 'nulls', sort: true }
]
const tableData = { columns: tableColumns, rows: props.analysis ?
    Object.keys(props.analysis!.nulls).map(col => { return { name: col, nulls: props.analysis!.nulls[col] } })
    : [] }
const tableLoading = ref(false)
</script>

<template>
    <div>
        <template v-if="data.length == 0">
            <span>No nulls found</span>
        </template>
        <template v-else>
            <div>
                <template v-if="viewCharts">
                    <MDBChart id="nullChart" type="bar" :data="chartData" />
                </template>
                <template v-else>
                    <MDBDatatable :dataset="tableData" :loading="tableLoading" max-width="500" />
                </template>]
            </div>
        </template>
        <MDBSwitch :label="viewCharts ? 'View as charts' : 'View as tables'" v-model="viewCharts" /> 
    </div>
</template>