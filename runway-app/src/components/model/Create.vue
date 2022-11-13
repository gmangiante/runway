<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue';
import { useFetch } from '@/composables/fetch'
import type { Datafile, Dataset } from '@/models/Dataset'
import type { DatasetAnalysis } from '@/models/DatasetAnalysis'
import { Model, ModelDatafileAssociation } from '@/models/Model'
import router from '@/router'
import { MDBBreadcrumb, MDBBreadcrumbItem, MDBRow, MDBSelect, MDBInput, MDBBtn, MDBSwitch } from 'mdb-vue-ui-kit'
import FileRoleChooser from '@/components/model/FileRoleChooser.vue'
import TargetFeatureChooser from '@/components/model/TargetFeatureChooser.vue'
import CreateLinearRegression from '@/components/model/linearRegression/Create.vue'

const props = defineProps({
    dataset_id: String
})

const { user } = $(useAuth0())

const { data } = $(await useFetch<Dataset>(`http://localhost:5000/api/datasets/${props.dataset_id}`))
const analysisFetch = $(await useFetch<DatasetAnalysis>(`http://localhost:5000/api/datasets/analyze/${props.dataset_id}`))
const newModel = reactive(new Model(-1, -1, '', false, 'LinearRegression', {}, '', [], user.email || 'error', new Date(), new Date(), []))

const modelTypeOptions = ref([
    { text: "Linear Regression", value: "linearRegression" },
    { text: "Logistic Regression", value: "logisticRegression" }
]);

const selectedModelType = ref('');

const handleRolesChanged = (args: { roles: { datafile_id: number, role: string }[], selected: boolean} ) => {
  const trainFile_id = args.roles.find(r => r.role == 'train' || r.role == 'trainAndValidation')?.datafile_id
  trainFile.value = data?.files?.find(f => f.id == trainFile_id)
  const valFile_id = args.roles.find(r => r.role == 'validation' || r.role == 'trainAndValidation')?.datafile_id
  valFile.value = data?.files?.find(f => f.id == valFile_id)
}

const trainFile = ref<Datafile | undefined>({} as Datafile)
const valFile = ref<Datafile | undefined>({} as Datafile)
const rolesSelected = computed(() => trainFile.value && valFile.value)

const selectedTarget = ref('')
const handleTargetSelected = (args: { selectedTarget: string }) => {
  selectedTarget.value = args.selectedTarget
}
const targetSelected = computed(() => selectedTarget.value && selectedTarget.value !== '')

const selectedFeatures = ref([] as string[])
const handleFeaturesSelected = (args: { selectedFeatures: string[] }) => {
  selectedFeatures.value = args.selectedFeatures
}
const featuresSelected = computed(() => selectedFeatures.value && selectedFeatures.value.length > 0)

const readyToSubmit = computed(() => rolesSelected.value && targetSelected.value && featuresSelected.value)

const submitForm = async (e: Event) => {
    e.preventDefault()
    newModel.feature_names = selectedFeatures.value
    newModel.dataset_id = Number.parseInt(props.dataset_id || '-1')
    newModel.datafiles = data?.files?.filter(f => f.role && (f.role !== 'none')).map(f => new ModelDatafileAssociation(f.id, f.role!)) || []
    const newModelFetch =
        await useFetch<{ new_model_id: number }>('http://localhost:5000/api/models/', { method: 'POST', body: JSON.stringify(newModel) })
    if (!newModelFetch.hasError.value && newModelFetch.data.value) {
        await router.push({ name: 'modelDetail', params: { id: newModelFetch.data.value['new_model_id'] }, replace: true, force: true })
    }
}
</script>

<template>
    <nav aria-label="breadcrumb">
      <MDBBreadcrumb>
        <MDBBreadcrumbItem><a href="/models">Models</a></MDBBreadcrumbItem>
        <MDBBreadcrumbItem active>Create new model</MDBBreadcrumbItem>
      </MDBBreadcrumb>
    </nav>
    <MDBRow tag="form" class="g-3" @submit="submitForm">
    <span><strong>Dataset name:</strong> {{ data?.name }}</span>
    <MDBInput label="Model name" v-model="newModel.name" class="mb-3" required />
    <MDBSwitch v-if="rolesSelected && (newModel.target_name !== '')" :label="newModel.is_public ? 'Public' : 'Private'" v-model="newModel.is_public" />
    <MDBSelect v-model:options="modelTypeOptions" v-model:selected="selectedModelType" />
    <FileRoleChooser :dataset="data || undefined" @roles-changed="handleRolesChanged" />
    <TargetFeatureChooser :analysis="analysisFetch.data || undefined" v-if="rolesSelected" @target-selected="handleTargetSelected" @features-selected="handleFeaturesSelected" />
    <CreateLinearRegression v-if="readyToSubmit" />
    <MDBBtn color="primary" type="submit" :class="{ disabled: !readyToSubmit }">Create model</MDBBtn>
    <RouterLink to="/datasets"><MDBBtn color="secondary">Cancel</MDBBtn></RouterLink>
  </MDBRow>
</template>
