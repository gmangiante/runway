<script setup lang="ts">
// Dataset detail component
// Acts as a shell to display info and tabs for explore, transform, and existing models
import { ref } from 'vue';
import { $ } from 'vue/macros'
import { useAuth0 } from '@auth0/auth0-vue'
import { useFetch } from '@/composables/fetch'
import type { Dataset } from '@/models/Dataset'
import { MDBRow, MDBCol, MDBBtn, MDBIcon, MDBBreadcrumb, MDBBreadcrumbItem, MDBTabs, MDBTabNav,
    MDBTabItem, MDBTabContent, MDBTabPane } from 'mdb-vue-ui-kit'
import DatasetInfo from '@/components/dataset/Info.vue'
import DatasetExplore from '@/components/dataset/Explore.vue'
import DatasetModels from '@/components/dataset/Models.vue'
import DatasetActions from '@/components/dataset/Actions.vue'
import DatasetTransform from '@/components/dataset/Transform.vue'

const props = defineProps({
    id: String
})
const { data } = $(await useFetch<Dataset>(`https://runway-demo.herokuapp.com/api/datasets/${props.id}`))
const activeTab = ref('info')
const { user, isAuthenticated } = $(useAuth0())
const isOwner = ref(user?.email && (user.email === data?.created_by))

const setPublic = async (isPublic: boolean) => {
    const sharingFetch = await useFetch<{ success: boolean}>(
        `https://runway-demo.herokuapp.com/api/datasets/sharing/${data?.id}/${isPublic}`, { method: 'POST'})
    if (!sharingFetch.hasError.value) {
        if (data) data.is_public = isPublic
    }
}
</script>

<template>
    <div>
        <MDBRow>
            <MDBCol class="d-flex">
                <template v-if="isOwner && data?.is_public">
                    <MDBBtn @click="setPublic(false)" floating color="primary">
                        <MDBIcon icon="lock" />
                    </MDBBtn>
                </template>
                <template v-if="isOwner && !data?.is_public">
                    <MDBBtn @click="setPublic(true)" floating color="primary">
                        <MDBIcon icon="share-alt" />
                    </MDBBtn>
                </template>
                <nav aria-label="breadcrumb" class="ms-2 pt-1">
                    <MDBBreadcrumb>
                        <MDBBreadcrumbItem><a href="/datasets">Datasets</a></MDBBreadcrumbItem>
                        <MDBBreadcrumbItem active>{{ data?.name }}</MDBBreadcrumbItem>
                    </MDBBreadcrumb>
                </nav>
            </MDBCol>
        </MDBRow>
        <MDBTabs v-model="activeTab">
            <MDBTabNav tabsClasses="mb-3">
                <MDBTabItem tabId="info" href="info">Info</MDBTabItem>
                <MDBTabItem tabId="explore" href="explore">Explore</MDBTabItem>
                <MDBTabItem tabId="transform" href="transform">Transform</MDBTabItem>
                <MDBTabItem tabId="models" href="models">Models</MDBTabItem>
            </MDBTabNav>
            <MDBTabContent>
                <MDBTabPane tabId="info"><DatasetInfo :dataset="data || undefined" /></MDBTabPane>
                <MDBTabPane tabId="explore"><DatasetExplore :dataset="data || undefined" /></MDBTabPane>
                <MDBTabPane tabId="transform" v-if="isOwner"><DatasetTransform :dataset="data || undefined" /></MDBTabPane>
                <MDBTabPane tabId="models" v-if="isAuthenticated"><DatasetModels :dataset="data || undefined" /></MDBTabPane>
            </MDBTabContent>
        </MDBTabs>
        <DatasetActions :dataset="data || undefined" />
    </div>
</template>