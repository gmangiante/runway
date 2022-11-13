<script setup lang="ts">
import { ref, computed, getCurrentInstance, onMounted} from 'vue'
import type { PropType } from 'vue'
import type { Dataset } from '@/models/Dataset'
import { MDBTable, MDBSelect } from 'mdb-vue-ui-kit';

const props = defineProps({
    dataset: Object as PropType<Dataset>
})

defineEmits({
    rolesChanged(args: { roles: { datafile_id: number, role: string }[], selected: boolean} ) { return true }
})

const currentInst = getCurrentInstance()

const roleOptions = ref([
    { text: "Train + validation", value: "trainAndValidation" },
    { text: "Train", value: "train" },
    { text: "Validation", value: "validation" },
    { text: "None", value: "none"}
])

const rolesSelected = computed(() => (props.dataset?.files?.some(f => f.role == "trainAndValidation"))
    || (props.dataset?.files?.some(f => f.role == "train") && props.dataset?.files?.some(f => f.role == "validation"))
)

const doRolesChangedEmit = () => {
    const roles = props.dataset?.files?.map(f => { return { datafile_id: f.id, role: f.role }})
    currentInst?.emit('rolesChanged', { roles: roles, selected: rolesSelected.value })
}

onMounted(() => doRolesChangedEmit())

</script>
<template>
    <MDBTable>
        <tr>
            <th scope="col">File</th>
            <th scope="col">Role</th>
        </tr>
        <tr v-for="file in dataset?.files">
            <td>{{file.name}}</td>
            <td><MDBSelect v-model:options="roleOptions" v-model:selected="file.role" @change="doRolesChangedEmit()" /></td>
        </tr>
    </MDBTable>
</template>