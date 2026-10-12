import {ArrowLeft,Save} from 'lucide-react'
import {useState} from 'react'
import type {ListeningDocument} from '../types'
export function EditPage({document,itemId,onSave,onCancel}:{document:ListeningDocument;itemId:string;onSave:(doc:ListeningDocument)=>void;onCancel:()=>void}){
 const item=document.items.find(i=>i.id===itemId)||document.items[0]; const [title,setTitle]=useState(item?.title||''); const [text,setText]=useState(item?.transcript||'')
 const save=()=>{if(!item)return;const sentences=text.split(/\n+/).flatMap((line,i)=>line.trim()?[{id:`manual-${i}`,text:line.trim(),speaker:null as null}]:[]);onSave({...document,items:document.items.map(i=>i.id===item.id?{...i,title,transcript:text,sentences,word_count:text.trim()?text.trim().split(/\s+/).length:0,confidence:'medium'}:i)})}
 return <main className="edit-shell"><header className="practice-header"><button className="text-button" onClick={onCancel}><ArrowLeft size={16}/> Back to preview</button><span className="eyebrow">EDIT TRANSCRIPT</span><span/></header><div className="edit-form"><label>Item title<input value={title} onChange={e=>setTitle(e.target.value)}/></label><label>Transcript <span>One sentence per line is recommended</span><textarea value={text} onChange={e=>setText(e.target.value)} rows={18}/></label><div className="edit-actions"><button className="button secondary" onClick={onCancel}>Cancel</button><button className="button primary" onClick={save}><Save size={16}/> Save changes</button></div></div></main>
}
