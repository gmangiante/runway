<script setup lang="ts">
import type { Dataset } from '@/models/Dataset'
import { MDBCard, MDBCardBody, MDBCardFooter, MDBSelect, MDBTabs, MDBTabNav, MDBTabItem, MDBTabContent, MDBTabPane, MDBBtn,
    MDBDropdown, MDBDropdownItem, MDBDropdownMenu, MDBDropdownToggle,
    MDBTable, MDBCheckbox, MDBCardHeader, MDBDatatable, MDBContainer, MDBListGroup, MDBListGroupItem, MDBRow, MDBCol, MDBChart, MDBIcon, MDBSwitch } from 'mdb-vue-ui-kit';
import { $ } from 'vue/macros'
import { useFetch } from '@/composables/fetch'
import { useAuth0 } from '@auth0/auth0-vue';
import { ref, computed, onMounted } from 'vue'
import router from '@/router';
import type { DatasetAnalysis } from '@/models/DatasetAnalysis'

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

onMounted(async () => analyze())

// https://stackoverflow.com/questions/1960473/get-all-unique-values-in-a-javascript-array-remove-duplicates
// https://stackoverflow.com/questions/44387647/group-and-count-values-in-an-array
const dtypeLabels = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        [...new Set(Object.keys(analysis.value[selectedFile.value].columns).map(x => analysis.value[selectedFile.value].columns[x].dtype))] : [])
const dtypeData = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        Object.keys(analysis.value[selectedFile.value].columns).map(x => analysis.value[selectedFile.value].columns[x])
        .reduce((p: { [key: string]: number}, c) => {
            const dtype = c.dtype
            if (!p.hasOwnProperty(dtype)) p[dtype] = 0
            p[dtype]++
            return p }, {}) : [])
const dtypeChartData = computed(() => { return { labels: dtypeLabels.value, datasets: Array({ label: 'Data types',
    backgroundColor: '#f87979', data: dtypeData.value})} } )

const nullLabels = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        Object.keys(analysis.value[selectedFile.value].nulls).filter(x => analysis.value[selectedFile.value].nulls[x] > 0) : [])
const nullData = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        Object.keys(analysis.value[selectedFile.value].nulls).filter(x => analysis.value[selectedFile.value].nulls[x] > 0)
        .map(x => analysis.value[selectedFile.value].nulls[x]) : [])
const nullChartData = computed(() => { return { labels: nullLabels.value, datasets: Array({ label: 'Nulls',
    backgroundColor: '#f87979', data: nullData.value})} } )

const activeTab = ref('datatypes')

const selectedFile = ref('')

const fileDropdown = ref(false)

const exploreViewCharts = ref(true)

async function setPublic(isPublic: boolean) {
    const sharingFetch = await useFetch<{ success: boolean}>(`http://localhost:5000/api/datasets/sharing/${data?.id}/${isPublic}`, { method: 'POST'})
    if (!sharingFetch.hasError.value) {
        if (data) data.is_public = isPublic
    }
}

</script>

<template>
    <MDBCard border="dark" style="max-width: 800px" >
        <MDBCardHeader border="dark">
            <MDBRow>
                <MDBCol col="8">Dataset info</MDBCol>
                <MDBCol col="3">
                    <span><strong>Sharing:</strong> {{ data?.is_public ? "Public" : "Private" }}</span>
                </MDBCol>
                <MDBCol col="1">
                    <template v-if="isOwner && data?.is_public">
                        <MDBBtn @click="setPublic(false)" floating color="primary" class="me-2">
                            <MDBIcon icon="lock" />
                        </MDBBtn>
                    </template>
                    <template v-if="isOwner && !data?.is_public">
                        <MDBBtn @click="setPublic(true)" floating color="primary" class="me-2">
                            <MDBIcon icon="share-alt" />
                        </MDBBtn>
                    </template>
                </MDBCol>
            </MDBRow>
        </MDBCardHeader>
        <MDBCardBody>
            <MDBRow>
                <MDBCol col="3"><strong>Name</strong></MDBCol>
                <MDBCol col="9">{{ data?.name }}</MDBCol>
            </MDBRow>
            <MDBRow>
                <MDBCol col="3"><strong>Author</strong></MDBCol>
                <MDBCol col="9">{{ data?.created_by }}</MDBCol>
            </MDBRow>
            <MDBRow>
                <MDBCol col="3"><strong>Created</strong></MDBCol>
                <MDBCol col="9">{{ data ? new Date(data.created_at).toLocaleString() : "" }}</MDBCol>
            </MDBRow>
            <MDBRow>
                <MDBCol col="3"><strong>Updated</strong></MDBCol>
                <MDBCol col="9">{{ data ? new Date(data.updated_at).toLocaleString() : "" }}</MDBCol>
            </MDBRow>
        </MDBCardBody>
    </MDBCard>
    <MDBCard border="dark" class="mt-2" style="max-width: 800px">
        <MDBCardHeader border="dark">Files</MDBCardHeader>
        <MDBCardBody>
            <MDBRow v-for="file in data?.files" class="justify-content-between">
                <MDBCol col="7"><strong>{{ file.name }}</strong></MDBCol>
                <MDBCol col="5">
                    <MDBBtn v-if="isOwner || data?.is_public" @click="downloadFile(file.id, file.name)" floating color="primary" class="me-2">
                        <MDBIcon icon="download" />
                    </MDBBtn>
                    <MDBBtn v-if="isOwner" @click="deleteFile(file.id)" floating color="danger">
                        <MDBIcon icon="trash" />
                    </MDBBtn>
                </MDBCol>
            </MDBRow>
        </MDBCardBody>
    </MDBCard>
    <MDBCard border="dark" class="mt-2" style="max-width: 800px">
        <MDBCardHeader border="dark">
            <MDBRow>
                <MDBCol col="4">Explore</MDBCol>
                <MDBCol col="8">
                    <MDBDropdown v-model="fileDropdown">
                        <MDBDropdownToggle @click="fileDropdown = !fileDropdown">
                            {{ selectedFile == '' ? "Choose file" : selectedFile }}
                        </MDBDropdownToggle>
                            <MDBDropdownMenu>
                                <MDBDropdownItem v-for="file in data?.files" tag="button" @click="selectedFile = file.name">{{ file.name }}</MDBDropdownItem>
                            </MDBDropdownMenu>
                    </MDBDropdown>
                </MDBCol>
            </MDBRow>
        </MDBCardHeader>
            <MDBCardBody>
                <MDBRow>
                    <MDBCol col="12">
                        <span v-if="selectedFile == ''">Choose file above</span>
                        <MDBTabs v-model="activeTab" v-if="selectedFile != ''">
                            <MDBTabNav tabsClasses="mb-3">
                                <MDBTabItem tabId="datatypes" href="datatypes" v-if="analysis[selectedFile]">Data types</MDBTabItem>
                                <MDBTabItem tabId="nulls" href="nulls">Nulls</MDBTabItem>
                            </MDBTabNav>
                            <MDBTabContent>
                                <MDBTabPane tabId="datatypes">
                                    <template v-if="exploreViewCharts">
                                        <MDBChart type="bar" :data="dtypeChartData" />
                                    </template>
                                    <template v-else>
                                        <MDBRow>
                                            <MDBCol col="4">
                                                <u><strong>Column</strong></u>
                                            </MDBCol>
                                            <MDBCol col="8">
                                                <u><strong>Data type</strong></u>
                                            </MDBCol>
                                        </MDBRow>
                                        <MDBRow v-for="col in analysis[selectedFile].columns">
                                            <MDBCol col="4">
                                                <strong>{{ col.name }}</strong>
                                            </MDBCol>
                                            <MDBCol col="8">
                                                {{ col.dtype }}
                                            </MDBCol>
                                        </MDBRow>
                                    </template>
                                </MDBTabPane>
                                <MDBTabPane tabId="nulls">
                                    <template v-if="nullData.length == 0">
                                        No nulls found
                                    </template>
                                    <template v-else>
                                        <template v-if="exploreViewCharts">
                                            <MDBChart id="nullChart" type="bar" :data="nullChartData" />
                                        </template>
                                        <template v-else>
                                            <MDBRow>
                                                <MDBCol col="4">
                                                    <u><strong>Column</strong></u>
                                                </MDBCol>
                                                <MDBCol col="8">
                                                    <u><strong>Nulls</strong></u>
                                                </MDBCol>
                                            </MDBRow>
                                            <MDBRow v-for="col, index in nullLabels">
                                                <MDBCol col="4">
                                                    {{ col }}
                                                </MDBCol>
                                                <MDBCol col="8">
                                                    {{ nullData[index] }}
                                                </MDBCol>
                                            </MDBRow>
                                        </template>
                                    </template>
                                </MDBTabPane>
                            </MDBTabContent>
                        </MDBTabs>
                    </MDBCol>
                </MDBRow>
            </MDBCardBody>
            <MDBCardFooter>
                <MDBSwitch :label="exploreViewCharts ? 'View as charts' : 'View as tables'" v-model="exploreViewCharts" /> 
            </MDBCardFooter>
        </MDBCard>
    
   
        <MDBCard border="dark" class="mt-2" style="max-width: 800px">
            <MDBCardHeader>Actions</MDBCardHeader>
            <MDBCardBody>
                <RouterLink :to="'/models/create/' + data?.id">
                    <MDBBtn color="primary">Create Model</MDBBtn>
                </RouterLink>
                <MDBBtn color="danger" @click="deleteDataset()">Delete dataset</MDBBtn>
            </MDBCardBody>
        </MDBCard>
</template>