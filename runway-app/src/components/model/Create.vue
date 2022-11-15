<script setup lang="ts">
import { ref, reactive, computed, onMounted, type Ref } from 'vue'
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue';
import { useFetch } from '@/composables/fetch'
import type { Datafile, Dataset } from '@/models/Dataset'
import type { DatasetAnalysis } from '@/models/DatasetAnalysis'
import { Model, ModelDatafileAssociation, type ModelParams } from '@/models/Model'
import router from '@/router'
import { MDBBreadcrumb, MDBBreadcrumbItem, MDBRow, MDBSelect, MDBInput, MDBBtn, MDBSwitch,
  MDBTextarea, MDBAccordion, MDBAccordionItem } from 'mdb-vue-ui-kit'
import FileRoleChooser from '@/components/model/FileRoleChooser.vue'
import TargetFeatureChooser from '@/components/model/TargetFeatureChooser.vue'
import LinearRegressionParams from '@/components/model/linearRegression/Params.vue'
import LogisticRegressionParams from '@/components/model/logisticRegression/Params.vue'

const props = defineProps({
    dataset_id: String
})

const { user } = $(useAuth0())

const { data } = $(await useFetch<Dataset>(`http://localhost:5000/api/datasets/${props.dataset_id}`))
const analysisFetch = $(await useFetch<DatasetAnalysis>(`http://localhost:5000/api/datasets/analyze/${props.dataset_id}`))

const newModel = reactive(new Model(-1, -1, '', '', false, '', '', {}, '', [], new Date(), 0, 0, 0, user.email || 'error', new Date(), new Date(), []))

const modelTypeOptions = ref([
    { text: "Linear Regression", value: "LinearRegression" },
    { text: "Logistic Regression", value: "LogisticRegression" }
]);

const handleRolesChanged = (args: { roles: { datafile_id: number, role: string }[], selected: boolean} ) => {
  console.log(args.roles)
  const trainFile_id = args.roles.find(r => r.role == 'train' || r.role == 'trainAndValidation')?.datafile_id
  trainFile.value = data?.files?.find(f => f.id == trainFile_id)
  const valFile_id = args.roles.find(r => r.role == 'validation' || r.role == 'trainAndValidation')?.datafile_id
  valFile.value = data?.files?.find(f => f.id == valFile_id)
}

const trainFile = ref<Datafile | undefined>({} as Datafile)
const valFile = ref<Datafile | undefined>({} as Datafile)
const rolesSelected = computed(() => trainFile.value && valFile.value)

const handleTargetSelected = (args: { selectedTarget: string }) => {
  newModel.target_name = args.selectedTarget
}
const targetSelected = computed(() => newModel.target_name && newModel.target_name !== '')

const handleFeaturesSelected = (args: { selectedFeatures: string[] }) => {
  newModel.feature_names = args.selectedFeatures
}
const featuresSelected = computed(() => newModel.feature_names && newModel.feature_names.length > 0)

const readyToSubmit = computed(() => isDup.value || (rolesSelected.value && targetSelected.value && featuresSelected.value))

const handleParamsChanged = ( args: { newParams: ModelParams}) => {
  newModel.params = args.newParams
}

const activeStep = ref('info')

const submitForm = async (e: Event) => {
    e.preventDefault()
    if (!isDup.value)
    {
      newModel.dataset_id = Number.parseInt(props.dataset_id || '-1')
      newModel.datafiles = data?.files?.filter(f => f.role && (f.role !== 'none')).map(f => new ModelDatafileAssociation(f.id, f.role!)) || []
    }
    console.log(newModel)
    const newModelFetch =
        await useFetch<{ new_model_id: number }>('http://localhost:5000/api/models/', { method: 'POST', body: JSON.stringify(newModel) })
    if (!newModelFetch.hasError.value && newModelFetch.data.value) {
        await router.push({ name: 'modelDetail', params: { id: newModelFetch.data.value['new_model_id'] }, replace: true, force: true })
    }
}

const existingParams: Ref<ModelParams | undefined> = ref()
const isDup = ref(false)
onMounted(
  async () => {
    if (router.currentRoute.value.query['dup']) {
      const existing_model_id = router.currentRoute.value.query['dup']
      const existingModelFetch =
        await useFetch<Model>(`http://localhost:5000/api/models/${existing_model_id}`)
      if (!existingModelFetch.hasError.value && existingModelFetch.data.value) {
          Object.assign(newModel, {...existingModelFetch.data.value})
          existingParams.value = JSON.parse(newModel.params.toString())
          isDup.value = true
      }
    }
    const accButtons = document.getElementsByClassName("accordion-button")
    for (let i = 0; i < accButtons.length; i++)
    {
      (accButtons[i] as any).type = "button"
    }
  }
)

</script>

<template>
    <nav aria-label="breadcrumb">
      <MDBBreadcrumb>
        <MDBBreadcrumbItem><a href="/models">Models</a></MDBBreadcrumbItem>
        <MDBBreadcrumbItem active>Create new model</MDBBreadcrumbItem>
      </MDBBreadcrumb>
    </nav>
    <MDBRow tag="form" class="g-3" @submit="submitForm" style="max-width: 750px">
      <MDBAccordion v-model="activeStep">
        <MDBAccordionItem headerTitle="Model info" collapseId="info">
          <span><strong>Dataset name:</strong> {{ data?.name }}</span>
          <MDBInput label="Model name" v-model="newModel.name" class="mb-3 mt-3" required />
          <MDBSwitch v-if="rolesSelected && (newModel.target_name !== '')" :label="newModel.is_public ? 'Public' : 'Private'" v-model="newModel.is_public" />
          <span><strong>Model type</strong></span>
          <MDBSelect v-model:options="modelTypeOptions" v-model:selected="newModel.class_name" />
          <MDBTextarea label="Notes" rows="5" v-model="newModel.notes" class="mt-3" />
        </MDBAccordionItem>
        <MDBAccordionItem headerTitle="Data" collapseId="data" v-if="!isDup">
          <FileRoleChooser :dataset="data || undefined" @roles-changed="handleRolesChanged" />
        </MDBAccordionItem>
        <MDBAccordionItem headerTitle="Target and features" collapseId="targetFeatures" v-if="!isDup">
          <TargetFeatureChooser :analysis="analysisFetch.data || undefined" v-if="rolesSelected" @target-selected="handleTargetSelected" @features-selected="handleFeaturesSelected" />
        </MDBAccordionItem>
        <MDBAccordionItem headerTitle="Model parameters" collapseId="modelParams">
          <span v-if="readyToSubmit"><strong>Model Parameters</strong></span>
          <LinearRegressionParams v-if="newModel.class_name === 'LinearRegression' && readyToSubmit" @params-changed="handleParamsChanged" :existing-params="existingParams" />
          <LogisticRegressionParams v-if="newModel.class_name === 'LogisticRegression' && readyToSubmit" @params-changed="handleParamsChanged" />
        </MDBAccordionItem>
      </MDBAccordion>
      <div>
        <MDBBtn color="primary" type="submit" :class="{ disabled: !readyToSubmit }">Create model</MDBBtn>
        <RouterLink to="/datasets"><MDBBtn color="secondary">Cancel</MDBBtn></RouterLink>
      </div>
      
    </MDBRow>
</template>
