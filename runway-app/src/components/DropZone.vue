<!-- https://www.smashingmagazine.com/2022/03/drag-drop-file-uploader-vuejs-3/ -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
const emit = defineEmits(['files-dropped'])

let active = ref(false)
let inActiveTimeout = 0

function setActive() {
	active.value = true
	clearTimeout(inActiveTimeout)
}
function setInactive() {
	inActiveTimeout = window.setTimeout(() => {
		active.value = false
	}, 50)
}

function onDrop(e: any) {
	setInactive()
	emit('files-dropped', [...e.dataTransfer.files])
}

function preventDefaults(e: any) {
	e.preventDefault()
}

const events = ['dragenter', 'dragover', 'dragleave', 'drop']

onMounted(() => {
	events.forEach((eventName) => {
		document.body.addEventListener(eventName, preventDefaults)
	})
})

onUnmounted(() => {
	events.forEach((eventName) => {
		document.body.removeEventListener(eventName, preventDefaults)
	})
})
</script>

<template>
	<div :data-active="active" @dragenter.prevent="setActive" @dragover.prevent="setActive" @dragleave.prevent="setInactive" @drop.prevent="onDrop">
		<slot :dropZoneActive="active"></slot>
	</div>
</template>