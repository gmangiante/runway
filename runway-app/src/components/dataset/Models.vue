<script setup lang="ts">
// Models subcomponent for dataset detail
// Shows related models
// Retrieves public for anonymous, public + private for authenticated
import type { PropType } from 'vue'
import { ref } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue';
import type { Dataset } from '@/models/Dataset'
import router from '@/router';
import { MDBDatatable } from 'mdb-vue-ui-kit';

const props = defineProps({
    dataset: Object as PropType<Dataset>
})

const { user } = $(useAuth0())
const isOwner = ref(user?.email && (user.email === props.dataset?.created_by))

const modelTableColumns = [
  { label: 'Sharing', field: 'sharing', width: 100, fixed: true, sort: true },
  { label: 'Name', field: 'name', sort: true },
  { label: 'Type', field: 'class_name', sort: true },
  { label: 'Author', field: 'created_by', sort: true },
  { label: 'Train score', field: 'train_score', sort: true},
  { label: 'Val score', field: 'val_score', sort: true}
]
const modelTableLoading = ref(false)

const modelTableData = { columns: modelTableColumns,
  rows: props.dataset?.models?.map(model => {
    return { ...model,
      sharing: model.is_public ? `<i class="fa fa-share-alt" />` : `<i class="fa fa-lock" />`
    } }) || [] }

const goToModelDetail = async (tableRowIndex: number) => {
    if (props.dataset?.models) await router.push({ name: 'modelDetail', params: { id: props.dataset.models[tableRowIndex].id }, force: true })
}

</script>

<template>
    <MDBDatatable :dataset="modelTableData" :maxWidth="1000" style="cursor:pointer"
        fixedHeader clickable @row-click="goToModelDetail" :loading="modelTableLoading" />
</template>