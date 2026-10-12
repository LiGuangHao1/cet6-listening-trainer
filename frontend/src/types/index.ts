export type Speaker = 'M' | 'W'
export type Sentence = { id:string; text:string; speaker?:Speaker|null }
export type SpeakerTurn = { speaker:Speaker; text:string; source_page:number }
export type Question = { number?:string|null; stem:string; options:string[] }
export type ListeningItem = { id:string; section:'A'|'B'|'C'; type:'conversation'|'passage'|'recording'; title:string; transcript:string; speaker_turns:SpeakerTurn[]; sentences:Sentence[]; questions:Question[]; source_pages:number[]; confidence:'high'|'medium'|'low'; extraction_method:'pdf-text'|'ocr'|'mixed'; word_count:number; detected:boolean; warning?:string|null }
export type ListeningDocument = { title:string; items:ListeningItem[]; source_filename?:string|null; warnings:string[] }
