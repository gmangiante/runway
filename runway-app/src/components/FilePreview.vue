<script setup lang="ts">
// generic file upload component, thanks to:
// https://www.smashingmagazine.com/2022/03/drag-drop-file-uploader-vuejs-3/
import { UploadableFile } from '@/models/UploadableFile';
import { MDBBtn, MDBIcon } from 'mdb-vue-ui-kit'

defineProps({
	file: { type: UploadableFile, required: true },
})

defineEmits(['remove'])
</script>


<template>
	<span>{{ file.file.name }}</span>
	<MDBBtn @click="$emit('remove', file)" floating color="danger" class="ms-2">
		<MDBIcon icon="trash" />
	</MDBBtn>
	<span v-show="file.status == 'loading'">In Progress</span>
	<span v-show="file.status == 'complete'">Uploaded</span>
	<span v-show="file.status == 'failed'">Error</span>
</template>

<style>
.close-icon {
	background-color: red;
	color: white;
	height: 30px;
	width: 30px;
}
</style>