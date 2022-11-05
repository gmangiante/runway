<script setup lang="ts">

import DropZone from '../components/DropZone.vue'
import FilePreview from '../components/FilePreview.vue'
import { useFileUpload } from '@/composables/fileUpload';
import { MDBCard, MDBCardHeader, MDBCardBody, MDBCardTitle, MDBFile, MDBListGroup, MDBListGroupItem, MDBBtn } from 'mdb-vue-ui-kit';

const UPLOAD_URL = 'http://localhost:5000/api/datasets/upload'
const { files, addFiles, removeFile, uploadFiles } = useFileUpload(UPLOAD_URL)

function onInputChange(e: any) {
	addFiles(e.target.files)
}

</script>

<template>
	<MDBCard>
		<MDBCardHeader>UPLOAD NEW DATASET</MDBCardHeader>
		<MDBCardBody>
    		<DropZone @files-dropped="addFiles" #default="{ dropZoneActive }">
				<MDBCardTitle v-if="dropZoneActive">
					Drop here
				</MDBCardTitle>
				<MDBCardTitle v-else>
					Drag files here or
				</MDBCardTitle>
				<MDBFile multiple @change="onInputChange" />
				<MDBListGroup flush v-show="files.length">
					<MDBListGroupItem v-for="file of files" :key="file.id" >
						<FilePreview :file="file" @remove="removeFile" />
					</MDBListGroupItem>
				</MDBListGroup>
			</DropZone>
			<MDBBtn @click="uploadFiles()" color="primary" :disabled="!files.length">Upload</MDBBtn>
		</MDBCardBody>
	</MDBCard>
</template>
