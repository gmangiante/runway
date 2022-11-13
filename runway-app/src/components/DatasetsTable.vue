<script setup lang="ts">
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch';
import type { Dataset } from '@/models/Dataset'
import { MDBTable, MDBIcon } from 'mdb-vue-ui-kit';
import { RouterLink } from 'vue-router';
import { useAuth0 } from '@auth0/auth0-vue';

const { isAuthenticated } = $(useAuth0())

const { isLoading, hasError, errorMessage, data } =
  $(await useFetch<Dataset[]>('http://localhost:5000/api/datasets/'))

</script>

<template>
  <main class="m-2">
    <MDBTable>
      <thead>
        <tr>
          <th v-if="isAuthenticated">Shared</th>
          <th scope="col">Name</th>
          <th scope="col">Created By</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dataset in data" :key="dataset.id">
          <td v-if="isAuthenticated">
            <template v-if="dataset.is_public">
              <MDBIcon icon="share-alt" />
            </template>
            <template v-else>
              <MDBIcon icon="lock" />
            </template>
          </td>
          <th scope="row"><RouterLink :to="'/datasets/' + dataset.id">{{ dataset.name }}</RouterLink></th>
          <td>{{ dataset.created_by }}</td>
        </tr>
      </tbody>
    </MDBTable>
  </main>
</template>
