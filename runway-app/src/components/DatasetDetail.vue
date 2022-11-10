<script setup lang="ts">
import type { Dataset } from '@/models/Dataset'
import { MDBCard, MDBCardBody, MDBCardFooter, MDBBtn, MDBTable, MDBCardHeader, MDBListGroup, MDBListGroupItem, MDBRow, MDBCol } from 'mdb-vue-ui-kit';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import { useAuth0 } from '@auth0/auth0-vue';
import { ref, computed, watchEffect } from 'vue'
import type { Ref } from 'vue'
import router from '@/router';
import type { DatasetAnalysis } from '@/models/DatasetAnalysis'
import ReactivePropChart from '@/components/ReactivePropChart.vue'
import { setChartDatasets } from 'vue-chartjs/dist/utils';

const props = defineProps({
    id: String
})

const { isLoading, hasError, errorMessage, data } =
  $(await useFetch<Dataset>(`http://localhost:5000/api/datasets/${props.id}`))

async function downloadFile(datafile_id: number, datafile_name: string) {
    const fileDownload = await useFetch<Blob>(`http://localhost:5000/api/datasets/datafiles/${datafile_id}`)

    if (!fileDownload.hasError.value) {
        let link = document.createElement('a')
        link.href = window.URL.createObjectURL(fileDownload.blob.value as Blob)
        link.download = datafile_name
        document.body.appendChild(link);
        link.click()
        document.body.removeChild(link);
    }
}

async function deleteFile(datafile_id: number) {
    const delFetch = await useFetch<{success: Boolean}>(`http://localhost:5000/api/datasets/datafiles/${datafile_id}`, 
        { method: 'DELETE' })
    if (delFetch.data.value?.success) {
        data?.files?.splice(data?.files?.findIndex(file => file.id === datafile_id), 1)
    }
}

async function deleteDataset() {
    const delFetch = await useFetch<{success: Boolean}>(`http://localhost:5000/api/datasets/${data?.id}`, 
        { method: 'DELETE' })
    if (delFetch.data.value?.success) {
        await router.push({ name: 'datasets', replace: true, force: true})
    }
}

const { user } = $(useAuth0())

const isOwner = ref(user.email === data?.created_by)

const analysis = ref<DatasetAnalysis>({})

async function analyze() {
    const analysisFetch = await useFetch<DatasetAnalysis>(`http://localhost:5000/api/datasets/analyze/${data?.id}`)
    if (!analysisFetch.hasError.value) {
        analysis.value = analysisFetch.data.value || {}
    }
}

const selectedFile = ref('')

const chartData = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        Object.keys(analysis.value[selectedFile.value].nulls).filter(x => analysis.value[selectedFile.value].nulls[x] > 0).map(x => analysis.value[selectedFile.value].nulls[x]) : [])
const chartLabels = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        Object.keys(analysis.value[selectedFile.value].nulls).filter(x => analysis.value[selectedFile.value].nulls[x] > 0) : [])
const chartDatasets = computed(() => Array({label: 'Nulls', backgroundColor: '#f87979', data: chartData.value }))

</script>

<template>
    <main>
        <MDBCard class="w-100">
            <MDBCardBody>
                <MDBTable>
                    <tr>
                        <th scope="row">Name</th>
                        <td>{{ data?.name }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Public</th>
                        <td>{{ data?.is_public }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Created by</th>
                        <td>{{ data?.created_by }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Created at</th>
                        <td>{{ data?.created_at }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Updated at</th>
                        <td>{{ data?.updated_at }}</td>
                    </tr>
                    <tr>
                        <th scope="row">Files</th>
                        <td></td>
                    </tr>
                    <tr v-for="file in data?.files">
                        <th scope="row">{{ file.name }}</th>
                        <td><MDBBtn v-if="isOwner || data?.is_public" @click="downloadFile(file.id, file.name)">Download</MDBBtn>
                            <MDBBtn v-if="isOwner" @click="deleteFile(file.id)">Delete</MDBBtn>
                        </td>
                    </tr>
                </MDBTable>
            </MDBCardBody>
            <MDBCardFooter>
                <RouterLink to="/datasets"><MDBBtn color="primary">Go back</MDBBtn></RouterLink>
                <MDBBtn color="danger" v-if="isOwner" @click="deleteDataset()">Delete Dataset</MDBBtn>
            </MDBCardFooter>
        </MDBCard>
        <MDBCard class="w-100">
            <MDBCardHeader>
                <MDBBtn color="primary" @click="analyze()">Analyze</MDBBtn>
            </MDBCardHeader>
            <MDBCardBody>
                <MDBRow class="g-3">
                    <MDBCol col="2">
                        <MDBListGroup>
                            <MDBListGroupItem v-for="file in Object.keys(analysis)" tag="button" class="px-3 border-0" action @click="selectedFile = file" :active="selectedFile == file">{{ file }}</MDBListGroupItem>
                        </MDBListGroup>
                    </MDBCol>
                    <MDBCol col="4">
                        <ReactivePropChart v-if="analysis[selectedFile]" :labels="chartLabels" :datasets="chartDatasets" />
                    </MDBCol>
                </MDBRow>
            </MDBCardBody>
        </MDBCard>
    </main>
</template>