export class Dataset {
    id: number
    name: string
    is_public: boolean
    created_by: string
    created_at: Date
    updated_at: Date

    constructor(id: number, name: string, is_public: boolean, created_by: string, created_at: Date, updated_at: Date) {
        this.id = id
        this.name = name
        this.is_public = is_public
        this.created_by = created_by
        this.created_at = created_at
        this.updated_at = updated_at
    }
}