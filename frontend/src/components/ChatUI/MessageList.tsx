import { Markdown } from './Markdown'
import { ChatMsg } from '../../state/useChatStore'

export function MessageList({ messages, onCopy, onRegenerate }:{ messages: ChatMsg[]; onCopy:(text:string)=>void; onRegenerate:()=>void }){
  return (
    <div>
      {messages.map((m,i)=>{
        const isUser = m.role === 'user'
        return (
          <div key={i} className={`mb-3 flex ${isUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`msg ${isUser ? 'msg-user' : 'msg-ai'}`}>
              {isUser ? m.content : <Markdown>{m.content}</Markdown>}
              {!isUser && (
                <div className="mt-2 flex gap-2 text-xs text-slate-400">
                  <button className="hover:text-slate-200" onClick={()=>onCopy(m.content)}>Copy</button>
                  <span>•</span>
                  <button className="hover:text-slate-200" onClick={onRegenerate}>Regenerate</button>
                </div>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}
