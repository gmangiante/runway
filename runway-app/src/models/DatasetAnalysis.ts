// client-side interfaces for dataset analysis results
export interface DatasetAnalysis {
    [index:string]: DatafileAnalysis
}

export interface ColumnDescription {
    name: string
    dtype: string
}

export interface DatafileAnalysis {
    dataset_id: number,
    datafile_id: number,
    datafile_name: string,
    columns: { [key: string]: ColumnDescription }
    nulls: { [key:string]: number}
    unique: { column: string, unique_val_count: number}[]
    corr: { column1: string, column2: string, corr_val: number }[]
    distributions: { column: string, distribution: { value: string, occurrences: number }[] }[]
}