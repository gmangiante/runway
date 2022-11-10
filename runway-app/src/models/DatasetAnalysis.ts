export interface DatasetAnalysis {
    [index:string]: DatafileAnalysis
}

export interface DatafileAnalysis {
    nulls: { [key:string]: number}
}