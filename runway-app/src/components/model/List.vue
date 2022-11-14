<script setup lang="ts">
import { ref } from 'vue'
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import type { Model } from '@/models/Model'
import router from '@/router'
import { MDBDatatable, MDBBreadcrumb, MDBBreadcrumbItem } from 'mdb-vue-ui-kit'

const { data } = $(await useFetch<Model[]>('http://localhost:5000/api/models/'))
const tableColumns = [
  { label: 'Sharing', field: 'sharing', width: 50, fixed: true, sort: true },
  { label: 'Name', field: 'name', sort: true },
  { label: 'Author', field: 'created_by', sort: true },
  { label: 'Train score', field: 'train_score', sort: true},
  { label: 'Val score', field: 'val_score', sort: true}
]
const tableLoading = ref(false)

const tableData = { columns: tableColumns,
  rows: data?.map(model => {
    return { ...model,
      sharing: model.is_public ? `<i class="fa fa-share-alt" />` : `<i class="fa fa-lock" />`
    } }) || [] }

const goToDetail = async (tableRowIndex: number) => {
  if (data) await router.push({ name: 'modelDetail', params: { id: data[tableRowIndex].id }, force: true })
}

</script>

<template>
  <nav aria-label="breadcrumb">
    <MDBBreadcrumb>
      <MDBBreadcrumbItem active>Models</MDBBreadcrumbItem>
    </MDBBreadcrumb>
  </nav>
  <MDBDatatable :dataset="tableData" :maxHeight="700" :maxWidth="750" style="cursor:pointer"
        fixedHeader clickable @row-click="goToDetail" :loading="tableLoading" />
</template>