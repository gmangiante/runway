export class Dataset {
    id: number
    name: string
    is_public: boolean
    created_by: string

    constructor(id: number, name: string, is_public: boolean, created_by: string) {
        this.id = id
        this.name = name
        this.is_public = is_public
        this.created_by = created_by
    }
}