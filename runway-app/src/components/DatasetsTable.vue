<script setup lang="ts">
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch';
import type { Dataset } from '@/models/Dataset'
import { MDBTable } from 'mdb-vue-ui-kit';
import { RouterLink } from 'vue-router';

const { isLoading, hasError, errorMessage, data } =
  $(await useFetch<Dataset[]>('http://localhost:5000/api/datasets/'))

</script>

<template>
  <main class="m-2">
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
          <th scope="row"><RouterLink :to="'/datasets/' + dataset.id">{{ dataset.name }}</RouterLink></th>
          <td>{{ dataset.is_public }}</td>
          <td>{{ dataset.created_by }}</td>
        </tr>
      </tbody>
    </MDBTable>
  </main>
</template>
