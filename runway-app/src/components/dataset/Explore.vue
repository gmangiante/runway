<script setup lang="ts">
import type { PropType } from 'vue'
import { ref, onMounted } from 'vue'
import { useFetch } from '@/composables/fetch'
import type { Dataset } from '@/models/Dataset'
import type { DatasetAnalysis } from '@/models/DatasetAnalysis'
import { MDBTabs, MDBTabNav, MDBTabContent, MDBTabItem, MDBTabPane,
    MDBDropdown, MDBDropdownItem, MDBDropdownMenu, MDBDropdownToggle } from 'mdb-vue-ui-kit'
import DataTypesAnalysis from '@/components/dataset/analysis/DataTypes.vue'
import NullsAnalysis from '@/components/dataset/analysis/Nulls.vue'

const props = defineProps({
    dataset: Object as PropType<Dataset>
})
const analysis = ref<DatasetAnalysis>({})
const activeTab = ref('datatypes')
const fileDropdown = ref(false)
const selectedFile = ref('')

onMounted(async () => analyze())

const analyze = async () => {
    const analysisFetch = await useFetch<DatasetAnalysis>(`http://localhost:5000/api/datasets/analyze/${props.dataset?.id}`)
    if (!analysisFetch.hasError.value) {
        analysis.value = analysisFetch.data.value || {}
    }
}
</script>

<template>
    <div>
        <MDBDropdown v-model="fileDropdown" class="ms-4 mt-4 mb-4">
            <MDBDropdownToggle @click="fileDropdown = !fileDropdown">
                <span>{{ selectedFile == '' ? "Choose file" : selectedFile }}</span>
            </MDBDropdownToggle>
                <MDBDropdownMenu>
                    <MDBDropdownItem v-for="file in props.dataset?.files" tag="button" @click="selectedFile = file.name">{{ file.name }}</MDBDropdownItem>
                </MDBDropdownMenu>
        </MDBDropdown>
        <span v-if="selectedFile == ''" class="ms-4">Choose file above</span>
        <MDBTabs v-model="activeTab" v-if="selectedFile !== ''" class="mt-4">
            <MDBTabNav tabsClasses="mb-3">
                <MDBTabItem tabId="datatypes" href="datatypes">Data types</MDBTabItem>
                <MDBTabItem tabId="nulls" href="nulls">Nulls</MDBTabItem>
            </MDBTabNav>
            <MDBTabContent>
                <MDBTabPane tabId="datatypes"><DataTypesAnalysis :analysis="analysis[selectedFile]" /></MDBTabPane>
                <MDBTabPane tabId="nulls"><NullsAnalysis :analysis="analysis[selectedFile]" /></MDBTabPane>
            </MDBTabContent>
        </MDBTabs>
    </div>
</template>