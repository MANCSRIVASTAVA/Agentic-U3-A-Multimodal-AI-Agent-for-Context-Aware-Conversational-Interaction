import { useEffect, useRef, useState } from 'react'
import { useChatStore } from '../../state/useChatStore'
import { chatOnce, chatStream } from '../../features/chat'
import { MessageItem } from './MessageItem'
import { TypingDots } from '../ChatUI/TypingDots'
import { ingest } from '../../features/rag'
import { useHistoryStore } from '../../state/useHistoryStore'
import { Composer } from '../ChatUI/Composer'

export function ChatPanel(){
  const base = import.meta.env.VITE_ORCH_BASE || 'http://localhost:8080'
  const { messages, append, setStreaming, streaming } = useChatStore()
  const [input, setInput] = useState('')
  const [streamContent, setStreamContent] = useState('')
  const scrollRef = useRef<HTMLDivElement>(null)
  const { upsertCurrent } = useHistoryStore()

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, streamContent])

  useEffect(()=>{ upsertCurrent(messages) }, [messages, upsertCurrent])

  function onAttach(file: File){
    ingest(file).then(res => {
      setInput(p => (p ? p + '\n' : '') + `Please use my uploaded doc: ${res.doc_id}`)
    })
  }

  function sendSSE(){
    if(!input.trim()) return
    const msgs = [...messages, { role: 'user', content: input }]
    append({ role: 'user', content: input })
    setInput('')
    setStreamContent('')
    setStreaming(true)
    const stop = chatStream(base, msgs, (t) => {
      setStreamContent(s => s + t)
    }, () => {
      setStreaming(false)
      append({ role: 'assistant', content: streamContent || '...' })
      stop()
    })
  }

  async function sendHTTP(){
    if(!input.trim()) return
    const msgs = [...messages, { role: 'user', content: input }]
    append({ role: 'user', content: input })
    setInput('')
    setStreaming(true)
    try{
      const res = await chatOnce(msgs as any)
      append({ role: 'assistant', content: res?.answer || '(no answer)' })
    } finally {
      setStreaming(false)
    }
  }

  function regenerateLast(){
    const msgs = messages
    setStreamContent('')
    setStreaming(true)
    const stop = chatStream(base, msgs, (t) => setStreamContent(s=>s+t), () => {
      setStreaming(false)
      append({ role: 'assistant', content: streamContent || '...' })
      stop()
    })
  }

  return (
    <div className="chat-shell">
      <div ref={scrollRef} className="chat-scroll">
        {messages.map((m,i)=>(<MessageItem key={i} m={m} onRegenerate={regenerateLast} />))}
        {streaming && (
          <div className="mb-3 flex justify-start">
            <div className="msg msg-ai">
              {streamContent ? streamContent : <TypingDots />}
            </div>
          </div>
        )}
      </div>

      <Composer
        value={input}
        onChange={setInput}
        onSendSSE={sendSSE}
        onSendHTTP={sendHTTP}
        onAttach={onAttach}
      />
    </div>
  )
}
