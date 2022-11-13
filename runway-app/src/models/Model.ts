import type { Datafile } from "./Dataset"

export class Model {
    id: number
    dataset_id: number
    name: string
    is_public: boolean
    class_name: string
    params: object
    target_name: string
    feature_names: string[]
    created_by: string
    created_at: Date
    updated_at: Date
    datafiles: Datafile[]

    constructor(id: number, dataset_id: number, name: string, is_public: boolean,
        class_name: string, params: object, target_name: string, feature_names: string[],
        created_by: string, created_at: Date, updated_at: Date, datafiles: Datafile[]) {
        this.id = id
        this.dataset_id = dataset_id
        this.name = name
        this.is_public = is_public
        this.class_name = class_name
        this.params = params
        this.target_name = target_name
        this.feature_names = feature_names
        this.created_by = created_by
        this.created_at = created_at
        this.updated_at = updated_at
        this.datafiles = datafiles
    }
}