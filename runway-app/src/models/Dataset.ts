import type { Model } from "./Model"

export interface Datafile {
    id: number,
    name: string,
    role: string | undefined
}

export class Dataset {
    id: number
    name: string
    is_public: boolean
    notes: string
    created_by: string
    created_at: Date
    updated_at: Date
    files: Datafile[] | null
    models: Model[] | null

    constructor(id: number, name: string, is_public: boolean, notes: string, created_by: string,
        created_at: Date, updated_at: Date, files: Datafile[] | null, models: Model[] | null) {
        this.id = id
        this.name = name
        this.is_public = is_public
        this.notes = notes
        this.created_by = created_by
        this.created_at = created_at
        this.updated_at = updated_at
        this.files = files
        this.models = models
    }
}