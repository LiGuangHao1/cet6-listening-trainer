import type {ListeningDocument} from '../types'
const KEY='cet6-listening-trainer:v1'
export type SavedState={document:ListeningDocument|null; current:number; revealed:Record<string,boolean>}
export const loadState=():SavedState=>{try{return JSON.parse(localStorage.getItem(KEY)||'null')||{document:null,current:0,revealed:{}}}catch{return {document:null,current:0,revealed:{}}}}
export const saveState=(state:SavedState)=>localStorage.setItem(KEY,JSON.stringify(state))
