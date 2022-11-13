<script setup lang="ts">
// https://stackoverflow.com/questions/1960473/get-all-unique-values-in-a-javascript-array-remove-duplicates
// https://stackoverflow.com/questions/44387647/group-and-count-values-in-an-array

import type { PropType } from 'vue'
import { ref, computed, onMounted } from 'vue'
import { useFetch } from '@/composables/fetch'
import type { Dataset } from '@/models/Dataset'
import type { DatasetAnalysis } from '@/models/DatasetAnalysis';
import { MDBRow, MDBCol, MDBTabs, MDBTabNav, MDBTabContent, MDBTabItem, MDBTabPane, MDBSwitch,
    MDBDropdown, MDBDropdownItem, MDBDropdownMenu, MDBDropdownToggle, MDBChart } from 'mdb-vue-ui-kit';

const props = defineProps({
    dataset: Object as PropType<Dataset>
})
const analysis = ref<DatasetAnalysis>({})
const activeTab = ref('datatypes')
const fileDropdown = ref(false)
const selectedFile = ref('')
const exploreViewCharts = ref(true)

onMounted(async () => analyze())

const analyze = async () => {
    const analysisFetch = await useFetch<DatasetAnalysis>(`http://localhost:5000/api/datasets/analyze/${props.dataset?.id}`)
    if (!analysisFetch.hasError.value) {
        analysis.value = analysisFetch.data.value || {}
    }
}

const dtypeLabels = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        [...new Set(Object.keys(analysis.value[selectedFile.value].columns).map(x => analysis.value[selectedFile.value].columns[x].dtype))] : [])
const dtypeData = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        Object.keys(analysis.value[selectedFile.value].columns).map(x => analysis.value[selectedFile.value].columns[x])
        .reduce((p: { [key: string]: number}, c) => {
            const dtype = c.dtype
            if (!p.hasOwnProperty(dtype)) p[dtype] = 0
            p[dtype]++
            return p }, {}) : [])
const dtypeChartData = computed(() => { return { labels: dtypeLabels.value, datasets: Array({ label: 'Data types', data: dtypeData.value})} } )

const nullLabels = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        Object.keys(analysis.value[selectedFile.value].nulls).filter(x => analysis.value[selectedFile.value].nulls[x] > 0) : [])
const nullData = computed(() => JSON.stringify(analysis.value) !== '{}' && selectedFile.value !== '' ?
        Object.keys(analysis.value[selectedFile.value].nulls).filter(x => analysis.value[selectedFile.value].nulls[x] > 0)
        .map(x => analysis.value[selectedFile.value].nulls[x]) : [])
const nullChartData = computed(() => { return { labels: nullLabels.value, datasets: Array({ label: 'Nulls', data: nullData.value})} } )
</script>

<template>
    <MDBDropdown v-model="fileDropdown" class="ms-4 mt-4 mb-4">
        <MDBDropdownToggle @click="fileDropdown = !fileDropdown">
            {{ selectedFile == '' ? "Choose file" : selectedFile }}
        </MDBDropdownToggle>
            <MDBDropdownMenu>
                <MDBDropdownItem v-for="file in props.dataset?.files" tag="button" @click="selectedFile = file.name">{{ file.name }}</MDBDropdownItem>
            </MDBDropdownMenu>
    </MDBDropdown>
    <span v-if="selectedFile == ''" class="ms-4">Choose file above</span>
    <MDBTabs v-model="activeTab" v-if="selectedFile != ''" class="mt-4">
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
    <MDBSwitch :label="exploreViewCharts ? 'View as charts' : 'View as tables'" v-model="exploreViewCharts" class="ms-auto" /> 
</template>