import { ChatMsg } from '../../state/useChatStore'
import { Markdown } from '../ChatUI/Markdown'
import { ttsSpeak } from '../../features/tts'

export function MessageItem({ m, onRegenerate }:{ m: ChatMsg, onRegenerate: ()=>void }) {
  const isUser = m.role === 'user'
  return (
    <div className={`mb-3 flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`msg ${isUser ? 'msg-user' : 'msg-ai'}`}>
        {isUser ? m.content : <Markdown>{m.content}</Markdown>}
        {!isUser && (
          <div className="actions">
            <button className="btn-icon" onClick={()=>ttsSpeak(m.content)}>🔊 Listen</button>
            <button className="btn-icon" onClick={()=>navigator.clipboard.writeText(m.content)}>⧉ Copy</button>
            <button className="btn-icon" onClick={onRegenerate}>↻ Regenerate</button>
          </div>
        )}
      </div>
    </div>
  )
}
