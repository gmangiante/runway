export class Model {
    id: number
    dataset_id: number
    dataset_name: string
    name: string
    is_public: boolean
    class_name: string
    params: ModelParams
    target_name: string
    feature_names: string[]
    fit_at: Date
    train_score: number
    val_score: number
    created_by: string
    created_at: Date
    updated_at: Date
    datafiles: ModelDatafileAssociation[]

    constructor(id: number, dataset_id: number, dataset_name: string, name: string, is_public: boolean,
        class_name: string, params: ModelParams, target_name: string, feature_names: string[],
        fit_at: Date, train_score: number, val_score: number,
        created_by: string, created_at: Date, updated_at: Date, datafiles: ModelDatafileAssociation[]) {
        this.id = id
        this.dataset_id = dataset_id
        this.dataset_name = dataset_name
        this.name = name
        this.is_public = is_public
        this.class_name = class_name
        this.params = params
        this.target_name = target_name
        this.feature_names = feature_names
        this.fit_at = fit_at
        this.train_score = train_score
        this.val_score = val_score
        this.created_by = created_by
        this.created_at = created_at
        this.updated_at = updated_at
        this.datafiles = datafiles
    }
}

export class ModelDatafileAssociation {
    datafile_id: number
    role: string

    constructor(datafile_id: number, role: string) {
        this.datafile_id = datafile_id
        this.role = role
    }
}

export interface ModelParams {
    [key: string]: Object
}