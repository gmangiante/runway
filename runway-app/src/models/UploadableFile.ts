// generic uploadable file description
// somewhat adapted from https://www.smashingmagazine.com/2022/03/drag-drop-file-uploader-vuejs-3/
export class UploadableFile {
    file: File
    id: string
    url: string
	status: string

    constructor(file: File) {
        this.file = file
        this.id = `${file.name}-${file.size}-${file.lastModified}-${file.type}`
        this.url = URL.createObjectURL(file)
        this.status = 'waiting'
    }
}