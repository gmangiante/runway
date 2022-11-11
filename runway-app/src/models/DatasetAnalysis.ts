export interface DatasetAnalysis {
    [index:string]: DatafileAnalysis
}

export interface ColumnDescription {
    name: string
    dtype: string
}

export interface DatafileAnalysis {
    columns: { [key: string]: ColumnDescription }
    nulls: { [key:string]: number}
}