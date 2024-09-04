export declare interface Stats {
    capturing: boolean
    recording: boolean
    recording_start_time: number
    continuity_threshold: number
    strategy: Strategy
}

export enum Strategy {
    live = 'live',
    record = 'record',
    motion_detection = 'motion_detection',
    entity_recognition = 'entity_recognition',
    off = 'off' 
}