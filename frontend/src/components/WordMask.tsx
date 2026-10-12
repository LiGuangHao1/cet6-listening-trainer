import type {MouseEvent} from 'react'
export function WordMask({word,revealed,onToggle}:{word:string;revealed:boolean;onToggle:()=>void}){
 const parts=word.match(/^(.*?)([.,!?;:)'"”’]*)$/); const core=parts?.[1]||word; const punctuation=parts?.[2]||''
 return <button className={`word-token ${revealed?'is-revealed':''}`} onClick={(e:MouseEvent)=>{e.stopPropagation();onToggle()}} aria-label={revealed?`Hide ${core}`:`Reveal ${core}`}><span style={revealed?undefined:{width:`${Math.max(2,Math.min(12,core.length * .58))}em`}}>{revealed?core:'\u00a0'}</span>{punctuation}</button>
}
