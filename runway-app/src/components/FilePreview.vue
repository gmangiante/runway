<!-- https://www.smashingmagazine.com/2022/03/drag-drop-file-uploader-vuejs-3/ -->
<script setup lang="ts">
import { UploadableFile } from '@/models/UploadableFile';
import { MDBBtn } from 'mdb-vue-ui-kit'

defineProps({
	file: { type: UploadableFile, required: true },
})

defineEmits(['remove'])
</script>


<template>
	<span>{{ file.file.name }}</span>
	<MDBBtn @click="$emit('remove', file)" class="close-icon">&times;</MDBBtn>
	<span v-show="file.status == 'loading'">In Progress</span>
	<span v-show="file.status == 'complete'">Uploaded</span>
	<span v-show="file.status == 'failed'">Error</span>
</template>