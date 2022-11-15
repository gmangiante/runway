<script setup lang="ts">
import type { PropType } from 'vue'
import { ref, onMounted } from 'vue'
import { useFetch } from '@/composables/fetch'
import type { Dataset } from '@/models/Dataset'
import type { DatasetAnalysis } from '@/models/DatasetAnalysis'
import { MDBSelect,
    MDBDropdown, MDBDropdownItem, MDBDropdownMenu, MDBDropdownToggle } from 'mdb-vue-ui-kit'
import DataTypesAnalysis from '@/components/dataset/analysis/DataTypes.vue'
import NullsAnalysis from '@/components/dataset/analysis/Nulls.vue'
import CorrelationAnalysis from '@/components/dataset/analysis/Correlation.vue'
import DistributionAnalysis from '@/components/dataset/analysis/Distribution.vue'
import UniqueAnalysis from '@/components/dataset/analysis/UniqueValues.vue'

const props = defineProps({
    dataset: Object as PropType<Dataset>
})
const analysis = ref<DatasetAnalysis>({})

const fileDropdown = ref(false)
const selectedFile = ref('')

onMounted(async () => analyze())

const analyze = async () => {
    const analysisFetch = await useFetch<DatasetAnalysis>(`http://runway-demo.herokuapp.com/api/datasets/analyze/${props.dataset?.id}`)
    if (!analysisFetch.hasError.value) {
        analysis.value = analysisFetch.data.value || {}
    }
}

const analysisOptions = [
    { text: 'Data types', value: 'datatypes' },
    { text: 'Nulls', value: 'nulls' },
    { text: 'Unique values', value: 'unique' },
    { text: 'Distribution', value: 'distribution' },
    { text: 'Correlation', value: 'correlation' }
]
const selectedAnalysis = ref('datatypes')

</script>

<template>
    <div>
        <MDBDropdown v-model="fileDropdown" class="mt-4 mb-4">
            <MDBDropdownToggle @click="fileDropdown = !fileDropdown">
                <span>{{ selectedFile == '' ? "Choose file" : selectedFile }}</span>
            </MDBDropdownToggle>
                <MDBDropdownMenu>
                    <MDBDropdownItem v-for="file in props.dataset?.files" tag="button" @click="selectedFile = file.name">{{ file.name }}</MDBDropdownItem>
                </MDBDropdownMenu>
        </MDBDropdown>
        <span v-if="selectedFile == ''" class="ms-4">Choose file above</span>
        <div class='d-flex mb-3' v-if="selectedFile !== ''"><span class="p-1"><strong>Analysis</strong></span><MDBSelect class="ms-2" v-if="selectedFile !== ''" v-model:options="analysisOptions" v-model:selected="selectedAnalysis" style="max-width: 400px" /></div>
        <DataTypesAnalysis v-if="selectedFile !== '' && selectedAnalysis === 'datatypes'" :analysis="analysis[selectedFile]" />
        <NullsAnalysis v-if="selectedFile !== '' && selectedAnalysis === 'nulls'" :analysis="analysis[selectedFile]" />
        <CorrelationAnalysis v-if="selectedFile !== '' && selectedAnalysis === 'correlation'" :analysis="analysis[selectedFile]" />
        <DistributionAnalysis v-if="selectedFile !== '' && selectedAnalysis === 'distribution'" :analysis="analysis[selectedFile]" />
        <UniqueAnalysis v-if="selectedFile !== '' && selectedAnalysis === 'unique'" :analysis="analysis[selectedFile]" />
    </div>
</template>