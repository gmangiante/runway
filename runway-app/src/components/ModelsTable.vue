<script setup lang="ts">
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch';
import type { Model } from '@/models/Model'
import { MDBTable, MDBIcon } from 'mdb-vue-ui-kit';
import { RouterLink } from 'vue-router';
import { useAuth0 } from '@auth0/auth0-vue';

const { isAuthenticated } = $(useAuth0())
const { isLoading, hasError, errorMessage, data } =
  $(await useFetch<Model[]>('http://localhost:5000/api/models/'))

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
        <tr v-for="model in data" :key="model.id">
          <td v-if="isAuthenticated">
            <template v-if="model.is_public">
              <MDBIcon icon="share-alt" />
            </template>
            <template v-else>
              <MDBIcon icon="lock" />
            </template>
          </td>
          <th scope="row"><RouterLink :to="'/models/' + model.id">{{ model.name }}</RouterLink></th>
          <td>{{ model.created_by }}</td>
        </tr>
      </tbody>
    </MDBTable>
  </main>
</template>
