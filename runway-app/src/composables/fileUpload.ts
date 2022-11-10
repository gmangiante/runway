import { ref, unref } from 'vue'
import { UploadableFile } from '@/models/UploadableFile'
import { useFetch } from './fetch'

export const useFileUpload = ()  => {
	const files = ref<UploadableFile[]>([])

    function addFiles(newFiles: File[]) {
        let newUploadableFiles = [...newFiles]
            .map((file) => new UploadableFile(file))
            .filter((file) => !fileExists(file.id))
        files.value = files.value.concat(newUploadableFiles)
    }

    function fileExists(otherId: string) {
        return files.value.some((file: UploadableFile) => file.id === otherId)
    }

    function removeFile(file: UploadableFile) {
        const index = files.value.indexOf(file)

        if (index > -1) files.value.splice(index, 1)
    }

	function uploadFiles(url: string)
	{
		return Promise.all(files.value.map(async (file: UploadableFile) => {
            const formData = new FormData()

			formData.append('file', file.file)

			file.status = 'loading'

			const fetchState = await useFetch(url, { method: 'POST', body: formData})

            file.status = fetchState.hasError.value ? 'failed' : 'complete'
		}))
	}

	return { uploadFiles, files, addFiles, removeFile }
}