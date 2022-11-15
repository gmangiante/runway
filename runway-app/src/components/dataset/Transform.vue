<script setup lang="ts">
import type { PropType } from 'vue'
import { ref, onMounted } from 'vue'
import { useFetch } from '@/composables/fetch'
import type { Dataset } from '@/models/Dataset'
import type { DatasetAnalysis } from '@/models/DatasetAnalysis'
import { MDBSelect,
    MDBDropdown, MDBDropdownItem, MDBDropdownMenu, MDBDropdownToggle } from 'mdb-vue-ui-kit'
import DropNulls from '@/components/dataset/transforms/DropNulls.vue'

const props = defineProps({
    dataset: Object as PropType<Dataset>
})
const analysis = ref<DatasetAnalysis>({})
const fileDropdown = ref(false)
const selectedFileName = ref('')
const selectedFileId = ref(0)
onMounted(async () => analyze())

const analyze = async () => {
    const analysisFetch = await useFetch<DatasetAnalysis>(`http://localhost:5000/api/datasets/analyze/${props.dataset?.id}`)
    if (!analysisFetch.hasError.value) {
        analysis.value = analysisFetch.data.value || {}
    }
}

const transformOptions = [
    { text: 'Drop nulls', value: 'dropnulls' }
]
const selectedTransform = ref('dropnulls')

const updateSelectedFile = (datafile_name: string, datafile_id: number) => {
    selectedFileName.value = datafile_name
    selectedFileId.value = datafile_id
}

</script>

<template>
    <div>
        <MDBDropdown v-model="fileDropdown" class="mt-4 mb-4">
            <MDBDropdownToggle @click="fileDropdown = !fileDropdown">
                <span>{{ selectedFileName == '' ? "Choose file" : selectedFileName }}</span>
            </MDBDropdownToggle>
                <MDBDropdownMenu>
                    <MDBDropdownItem v-for="file in props.dataset?.files" tag="button" @click="updateSelectedFile(file.name, file.id)">{{ file.name }}</MDBDropdownItem>
                </MDBDropdownMenu>
        </MDBDropdown>
        <span v-if="selectedFileName == ''" class="ms-4">Choose file above</span>
        <MDBSelect v-if="selectedFileName !== ''" v-model:options="transformOptions" v-model:selected="selectedTransform" style="max-width: 400px" />
        <DropNulls v-if="selectedFileName !== '' && selectedTransform === 'dropnulls'" :dataset_id="dataset?.id" :datafile_id="selectedFileId" :analysis="analysis[selectedFileName]" />
    </div>
</template>