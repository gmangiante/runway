<script setup lang="ts">
import type { PropType } from 'vue'
import { ref, computed } from 'vue'
import { useFetch } from '@/composables/fetch'
import type { DatafileAnalysis } from '@/models/DatasetAnalysis'
import { MDBCheckbox, MDBDatatable, MDBSwitch, MDBBtn } from 'mdb-vue-ui-kit'

const props = defineProps({
    dataset_id: Number,
    datafile_id: Number,
    analysis: Object as PropType<DatafileAnalysis>
})

const tableColumns = [
  { label: 'Column', field: 'name', sort: true },
  { label: 'Unique values', field: 'unique', sort: true }
]
const tableData = { columns: tableColumns, rows: props.analysis?.unique ?
    props.analysis.unique.map(col => { return { name: col.column, unique: col.unique_val_count } })
    : [] }
const tableLoading = ref(false)

const selectedColumns = ref([] as String[])

const handleColumnsSelected = (rows: any[]) => {
    selectedColumns.value = rows.map(row => row.name)
}

const dropFirst = ref(true)

const canEncode = computed(() => selectedColumns.value.length > 0)

const duplicate = ref(true)

const doEncode = async () => {
    const encodeData = { duplicate: duplicate.value, dropFirst: dropFirst.value, columns: selectedColumns.value }
    const encodeFetch = await useFetch<{success: Boolean, datafile_id: number}>
        (`http://runway-demo.herokuapp.com/api/datasets/datafiles/${props.datafile_id}/transform/onehotencode`, 
        { method: 'POST', body: JSON.stringify(encodeData) })

}

</script>
<template>
    <MDBDatatable :dataset="tableData" selectable multi @selected-rows="handleColumnsSelected" :max-width="750" />
    <div class="d-flex">
        <MDBCheckbox v-model="dropFirst" label="Drop first" />
        <MDBSwitch v-model="duplicate" :label="duplicate ? 'Duplicate' : 'Replace'" class="ms-1" />
        <MDBBtn color="danger" class="ms-3" :class="{ disabled: !canEncode}" @click="doEncode()">Encode</MDBBtn>
    </div>
</template>