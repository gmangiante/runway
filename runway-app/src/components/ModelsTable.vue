<script setup lang="ts">
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch';
import type { Model } from '@/models/Model'
import { MDBTable } from 'mdb-vue-ui-kit';
import { RouterLink } from 'vue-router';

const { isLoading, hasError, errorMessage, data } =
  $(await useFetch<Model[]>('http://localhost:5000/api/models/'))

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
        <tr v-for="model in data" :key="model.id">
          <th scope="row"><RouterLink :to="'/models/' + model.id">{{ model.name }}</RouterLink></th>
          <td>{{ model.is_public }}</td>
          <td>{{ model.created_by }}</td>
        </tr>
      </tbody>
    </MDBTable>
  </main>
</template>
