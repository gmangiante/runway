<script setup lang="ts">
// Dataset list component
// Retrieves public for anonymous users, public + private for authenticated
import { ref } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue'
import { useFetch } from '@/composables/fetch'
import type { Dataset } from '@/models/Dataset'
import { RouterLink } from 'vue-router'
import router from '@/router'
import {  MDBBreadcrumb, MDBBreadcrumbItem, MDBDatatable, MDBBtn } from 'mdb-vue-ui-kit'

const { isAuthenticated } = $(useAuth0())
const { data } = $(await useFetch<Dataset[]>('http://localhost:5000/api/datasets/'))
const tableColumns = [
  { label: 'Sharing', field: 'sharing', width: 80, fixed: true, sort: true },
  { label: 'Name', field: 'name', sort: true },
  { label: 'Author', field: 'created_by', sort: true }
]
const tableLoading = ref(false)

const tableData = { columns: tableColumns,
  rows: data?.map(dataset => {
    return { ...dataset,
      sharing: dataset.is_public ? `<i class="fa fa-share-alt" />` : `<i class="fa fa-lock" />`
    } }) || [] }

const goToDetail = async (tableRowIndex: number) => {
  if (data) await router.push({ name: 'datasetDetail', params: { id: data[tableRowIndex].id }, force: true })
}

</script>

<template>
  <nav aria-label="breadcrumb">
    <MDBBreadcrumb>
      <MDBBreadcrumbItem active>Datasets</MDBBreadcrumbItem>
    </MDBBreadcrumb>
  </nav>
    <RouterLink to="/datasets/create" custom v-slot="{ navigate }" v-if="isAuthenticated">
        <MDBBtn @click="navigate" role="link" color="primary" class="m-3">Add Dataset</MDBBtn>
      </RouterLink>
    <MDBDatatable :dataset="tableData" :maxWidth="750" style="cursor:pointer"
        fixedHeader clickable @row-click="goToDetail" :loading="tableLoading" />
</template>