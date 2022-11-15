<script setup lang="ts">
// Drop-null transform component for a datafile
// Can drop by row or column
// NOTE that there is a tricky aspect to this as yet unresolved about how to refresh post-transform!
import type { PropType } from 'vue'
import { ref, computed, getCurrentInstance } from 'vue'
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

const dropOptions = [
    { text: 'rows', value: 0 },
    { text: 'columns', value: 1 }
]

const selectedDropOption = ref(0)

const canDrop = computed(() => selectedColumns.value.length > 0)

const duplicate = ref(true)

const doDrop = async () => {
    const dropData = { duplicate: duplicate.value, axis: selectedDropOption.value, columns: selectedColumns.value }
    const dropFetch = await useFetch<{success: Boolean, datafile_id: number}>
        (`http://localhost:5000/api/datasets/datafiles/${props.datafile_id}/transform/dropnulls`, 
        { method: 'POST', body: JSON.stringify(dropData) })
    if (!dropFetch.hasError.value) window.location.reload()
}

</script>
<template>
    <MDBDatatable :dataset="tableData" selectable multi @selected-rows="handleColumnsSelected" :max-width="750" />
    <div class="d-flex">
        <span class="p-2">Drop</span>
        <MDBSelect v-model:options="dropOptions" v-model:selected="selectedDropOption" class="ms-3 me-3" />
        <MDBSwitch v-model="duplicate" :label="duplicate ? 'Duplicate' : 'Replace'"/>
        <MDBBtn color="danger" class="ms-3" :class="{ disabled: !canDrop}" @click="doDrop()">Drop</MDBBtn>
    </div>
</template>