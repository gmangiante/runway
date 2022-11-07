<script setup lang="ts">
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch';
import type { Dataset } from '@/models/Dataset'
import { MDBTable } from 'mdb-vue-ui-kit';

const { isLoading, hasError, errorMessage, data } =
  $(await useFetch<Dataset[]>('http://localhost:5000/api/datasets/list'))

</script>

<template>
  <main class="m-2">
    <h2>Datasets</h2>
    <MDBTable>
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="Col">Public</th>
          <th scope="col">Created By</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dataset in data" :key="dataset.id">
          <th scope="row">{{ dataset.name }}</th>
          <td>{{ dataset.is_public }}</td>
          <td>{{ dataset.created_by }}</td>
        </tr>
      </tbody>
    </MDBTable>
  </main>
</template>
