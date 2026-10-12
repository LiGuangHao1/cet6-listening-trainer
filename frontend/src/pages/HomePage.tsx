import {useRef,useState} from 'react'
import {FileUp,LoaderCircle} from 'lucide-react'
import type {ListeningDocument} from '../types'
export function HomePage({onImported}:{onImported:(doc:ListeningDocument)=>void}){
 const input=useRef<HTMLInputElement>(null); const [busy,setBusy]=useState(false); const [error,setError]=useState('')
 const upload=async(file?:File)=>{if(!file)return; setBusy(true);setError('');try{const body=new FormData();body.append('file',file);const r=await fetch('/api/parse',{method:'POST',body});const data=await r.json();if(!r.ok)throw new Error(data.detail||'Could not parse the PDF');onImported(data)}catch(e){setError(e instanceof Error?e.message:'Import failed')}finally{setBusy(false)}}
 return <main className="home-shell"><div className="home-mark">LP</div><h1>Listening Practice</h1><p className="home-subtitle">A quiet workspace for CET-6 listening transcripts.</p><button className="upload-zone" onClick={()=>input.current?.click()} onDragOver={e=>e.preventDefault()} onDrop={e=>{e.preventDefault();void upload(e.dataTransfer.files[0])}} disabled={busy}><input ref={input} type="file" accept="application/pdf" hidden onChange={e=>void upload(e.target.files?.[0])}/>{busy?<LoaderCircle className="spin" size={28}/>:<FileUp size={28}/>}<strong>{busy?'Reading your PDF…':'Upload PDF'}</strong><span>Click to upload or drag & drop</span><small>Import a CET-6 listening PDF</small></button>{error&&<p className="error-text">{error}</p>}</main>
}
