<script setup lang="ts">
// Impute-null transform component for a datafile
// Can impute zero, empty string, median, mode, mean
// NOTE that there is a tricky aspect to this as yet unresolved about how to refresh post-transform!
import type { PropType } from 'vue'
import { ref, computed } from 'vue'
import { useFetch } from '@/composables/fetch'
import type { DatafileAnalysis } from '@/models/DatasetAnalysis'
import { MDBSelect, MDBDatatable, MDBSwitch, MDBBtn } from 'mdb-vue-ui-kit'

const props = defineProps({
    dataset_id: Number,
    datafile_id: Number,
    analysis: Object as PropType<DatafileAnalysis>
})

const tableColumns = [
  { label: 'Column', field: 'name', sort: true },
  { label: 'Nulls', field: 'nulls', sort: true }
]
const tableData = { columns: tableColumns, rows: props.analysis ?
    Object.keys(props.analysis!.nulls).filter(k => props.analysis!.nulls[k] > 0).map(col => { return { name: col, nulls: props.analysis!.nulls[col] } })
    : [] }
const tableLoading = ref(false)

const selectedColumns = ref([] as String[])

const handleColumnsSelected = (rows: any[]) => {
    selectedColumns.value = rows.map(row => row.name)
}

const imputeOptions = [
    { text: 'zero', value: 'zero' },
    { text: 'empty string', value: 'emptystring' },
    { text: 'mean', value: 'mean' },
    { text: 'mode', value: 'mode' },
    { text: 'median', value: 'median' }
]

const selectedImputeOption = ref('zero')

const canImpute = computed(() => selectedColumns.value.length > 0)

const duplicate = ref(true)

const doImpute = async () => {
    const imputeData = { duplicate: duplicate.value, impute: selectedImputeOption.value, columns: selectedColumns.value }
    const imputeFetch = await useFetch<{success: Boolean, datafile_id: number}>
        (`https://runway-demo.herokuapp.com/api/datasets/datafiles/${props.datafile_id}/transform/imputenulls`, 
        { method: 'POST', body: JSON.stringify(imputeData) })

}

</script>
<template>
    <MDBDatatable :dataset="tableData" selectable multi @selected-rows="handleColumnsSelected" :max-width="750" />
    <div class="d-flex">
        <span class="p-2">Impute</span>
        <MDBSelect v-model:options="imputeOptions" v-model:selected="selectedImputeOption" class="ms-3 me-3" />
        <MDBSwitch v-model="duplicate" :label="duplicate ? 'Duplicate' : 'Replace'"/>
        <MDBBtn color="danger" class="ms-3" :class="{ disabled: !canImpute}" @click="doImpute()">Impute</MDBBtn>
    </div>
</template>