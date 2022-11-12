<script setup lang="ts">
import type { PropType } from 'vue';
import { ref, computed, reactive } from 'vue'
import type { Dataset } from '@/models/Dataset';
import type { DatasetAnalysis } from '@/models/DatasetAnalysis';
import { Model, ModelDatafileAssociation } from '@/models/Model'
import { MDBRow, MDBCol, MDBSelect, MDBTable, MDBBtn, MDBSwitch, MDBInput } from 'mdb-vue-ui-kit';
import { useFetch } from '@/composables/fetch';
import { useAuth0 } from '@auth0/auth0-vue';
import { $ } from 'vue/macros'
import router from '@/router';

const { user } = $(useAuth0())
const props = defineProps({
    dataset: Object as PropType<Dataset>
})

const roleOptions = ref([
    { text: "Train + validation", value: "trainAndValidation" },
    { text: "Train", value: "train" },
    { text: "Validation", value: "validation" },
    { text: "None", value: "none"}
]);

const rolesSelected = computed(() => (props.dataset?.files?.some(f => f.role == "trainAndValidation"))
    || (props.dataset?.files?.some(f => f.role == "train") && props.dataset?.files?.some(f => f.role == "validation"))
)

// https://stackoverflow.com/questions/37320296/how-to-calculate-intersection-of-multiple-arrays-in-javascript-and-what-does-e

const potentialTargets = computed(() => {
    if (!analysisFetch || !analysisFetch.data.value) return []
    const colNames = Object.keys(analysisFetch.data.value).map(f => analysisFetch.data.value![f].columns)
        .map(c => Object.keys(c).map(k => c[k].name))
    return colNames.reduce((intersection, array) => {
        return intersection.filter(intersectedItem => array.some(item => intersectedItem === item));
    }, colNames[0]).filter(c => !c.startsWith('Unnamed'))
})

const potentialTargetsAsOptions = computed(() => potentialTargets.value ? potentialTargets.value
    .map(t => { return { text: t, value: t}})
    : [])

const potentialFeatures = computed(() => potentialTargets.value.filter(t => t != newModel.target_name))

const analysisFetch =
    await useFetch<DatasetAnalysis>(`http://localhost:5000/api/datasets/analyze/${props.dataset?.id}`)

const newModel = reactive(new Model(-1, -1, '', false, 'LinearRegression', {}, '', [], user.email || 'error', new Date(), new Date(), []))

async function submitForm(e: Event) {
    e.preventDefault()
    newModel.feature_names = potentialFeatures.value
    newModel.dataset_id = props.dataset?.id || -1
    newModel.datafiles = props.dataset?.files?.filter(f => f.role && (f.role !== 'none')).map(f => new ModelDatafileAssociation(f.id, f.role!)) || []
    let { isLoading, hasError, errorMessage, data } =
        await useFetch<{ new_model_id: number }>('http://localhost:5000/api/models/', { method: 'POST', body: JSON.stringify(newModel) })
    if (!hasError.value && data.value) {
        await router.push({ name: 'modelDetail', params: { id: data.value['new_model_id'] }, replace: true, force: true })
    }
}

</script>

<template>
    <main>
        <MDBRow tag="form" class="g-3" @submit="submitForm">
            <MDBCol col="12">
                <MDBInput label="Model name" v-model="newModel.name" class="mb-3" required />
            </MDBCol>
            <MDBCol col="12">
                <MDBTable>
                    <tr>
                        <th scope="col">File</th>
                        <th scope="col">Role</th>
                    </tr>
                    <tr v-for="file in dataset?.files">
                        <td>{{file.name}}</td>
                        <td><MDBSelect v-model:options="roleOptions" v-model:selected="file.role" /></td>
                    </tr>
                </MDBTable>
            </MDBCol>
            <MDBCol v-if="rolesSelected" col="12">
                <MDBSelect v-model:options="potentialTargetsAsOptions" v-model:selected="newModel.target_name" />  
            </MDBCol>
            <MDBCol v-if="rolesSelected && (newModel.target_name !== '')" col="12">
                {{potentialFeatures}}
            </MDBCol>
            <MDBCol col="12">
                <MDBSwitch v-if="rolesSelected && (newModel.target_name !== '')" :label="newModel.is_public ? 'Public' : 'Private'" v-model="newModel.is_public" />
            </MDBCol>
            <MDBCol v-if="rolesSelected && (newModel.target_name !== '')" col="12">
                <MDBBtn color="primary" type="submit">Create model</MDBBtn>
                <RouterLink to="/datasets"><MDBBtn color="secondary">Cancel</MDBBtn></RouterLink>
            </MDBCol>
        </MDBRow>
    </main>
</template>