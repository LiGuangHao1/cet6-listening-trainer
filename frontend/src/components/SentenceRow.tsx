import {Eye,EyeOff} from 'lucide-react'
import type {Sentence,Speaker} from '../types'
import {WordMask} from './WordMask'
export function SentenceRow({sentence,revealedWords,revealedSentence,onWordToggle,onSentenceToggle,showSpeaker}:{sentence:Sentence;revealedWords:Record<string,boolean>;revealedSentence:boolean;onWordToggle:(key:string)=>void;onSentenceToggle:()=>void;showSpeaker:boolean}){
 const words=sentence.text.split(/\s+/).filter(Boolean)
 return <div className="sentence-row"><div className="sentence-speaker">{showSpeaker&&sentence.speaker?speakerLabel(sentence.speaker):''}</div><div className="sentence-text">{words.map((word,i)=><WordMask key={`${sentence.id}-${i}`} word={word} revealed={revealedSentence||!!revealedWords[`${sentence.id}:${i}`]} onToggle={()=>onWordToggle(`${sentence.id}:${i}`)}/>)}</div><button className={`sentence-eye ${revealedSentence?'active':''}`} onClick={onSentenceToggle} aria-label={revealedSentence?'Hide sentence':'Reveal sentence'}>{revealedSentence?<EyeOff size={17}/>:<Eye size={17}/>}</button></div>
}
function speakerLabel(s:Speaker){return <span className={`speaker-badge ${s==='M'?'male':'female'}`}>{s}</span>}
