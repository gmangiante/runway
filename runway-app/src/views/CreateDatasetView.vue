<script setup lang="ts">
import { Dataset } from '@/models/Dataset'
import { reactive } from 'vue'
import { MDBInput, MDBCard, MDBCardBody, MDBBreadcrumb, MDBBreadcrumbItem, MDBCheckbox, MDBBtn, MDBRow, MDBCol } from 'mdb-vue-ui-kit';
import { useAuth0 } from '@auth0/auth0-vue';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import router from '@/router';
import CreateDataset from '@/components/CreateDataset.vue'

</script>

<template>
  <main>
    <nav aria-label="breadcrumb">
          <MDBBreadcrumb>
            <MDBBreadcrumbItem><a href="/datasets">Datasets</a></MDBBreadcrumbItem>
            <MDBBreadcrumbItem active>
              Create new dataset
            </MDBBreadcrumbItem>
          </MDBBreadcrumb>
        </nav>
    <CreateDataset />
  </main>
</template>
