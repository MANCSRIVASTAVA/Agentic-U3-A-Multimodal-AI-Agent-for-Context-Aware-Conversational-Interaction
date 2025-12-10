import { useRef, useState } from 'react'
import { startVoice } from '../../features/voice'
import { useVoiceStore } from '../../state/useVoiceStore'
import { getMicStream, startMediaRecorder, stopMediaRecorder } from '../../audio/recorder'

type Props = {
  value: string
  onChange: (v: string) => void
  onSendSSE: () => void
  onSendHTTP: () => void
  onAttach: (f: File) => void
}

export function Composer({ value, onChange, onSendSSE, onSendHTTP, onAttach }: Props) {
  const fileRef = useRef<HTMLInputElement>(null)
  const { setPartial, setFinal } = useVoiceStore()

  // WS + recording control
  const wsCtlRef = useRef<any>(null)
  const mediaRef = useRef<MediaRecorder | null>(null)
  const [recording, setRecording] = useState(false)

  function pickFile() {
    fileRef.current?.click()
  }

  function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0]
    if (f) onAttach(f)
    // reset so selecting same file again still triggers change
    e.currentTarget.value = ''
  }

  async function toggleMic() {
    if (recording) {
      setRecording(false)
      wsCtlRef.current?.close()
      wsCtlRef.current = null
      if (mediaRef.current) stopMediaRecorder(mediaRef.current)
      mediaRef.current = null
      return
    }

    const base = import.meta.env.VITE_ORCH_BASE || 'http://localhost:8080'

    // open WS and wire transcript events
    wsCtlRef.current = startVoice(base, ({ event, data }) => {
      if (event === 'transcript.partial') setPartial(data.text)
      if (event === 'transcript.final') {
        setFinal(data.text)
        onChange(data.text) // drop final into the input
      }
    })

    // start mic capture and stream chunks to WS
    const stream = await getMicStream()
    mediaRef.current = startMediaRecorder(stream, async (blob: Blob) => {
      try {
        const buf = await blob.arrayBuffer()
        wsCtlRef.current?.send(buf)
      } catch {
        /* noop */
      }
    })

    setRecording(true)
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      onSendSSE()
    }
  }

  return (
    <div className="chat-composer">
      <div className="flex items-end gap-2 w-full">
        {/* Attach */}
        <button className="btn-icon" title="Attach file" onClick={pickFile}>
          <svg width={18} height={18} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66L9.64 16.2a2 2 0 0 1-2.83-2.83l8.49-8.49"/>
          </svg>
        </button>

        {/* Mic */}
        <button
          className={`btn-icon ${recording ? 'bg-indigo-600 text-white' : ''}`}
          title={recording ? 'Stop recording' : 'Start voice'}
          onClick={toggleMic}
        >
          <svg width={18} height={18} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
            <line x1="12" y1="19" x2="12" y2="22"/>
            <line x1="8" y1="22" x2="16" y2="22"/>
          </svg>
        </button>

        {/* Input */}
        <textarea
          className="input min-h-[44px] max-h-40 resize-none flex-1"
          rows={1}
          value={value}
          placeholder="Message the assistant…"
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        {/* Send (SSE) */}
        <button className="btn btn-primary" onClick={onSendSSE}>
          Send
        </button>

        {/* HTTP fallback */}
        <button className="btn px-3 py-2 bg-slate-800/70 hover:bg-slate-800" onClick={onSendHTTP}>
          HTTP
        </button>
      </div>

      {/* hidden file input */}
      <input ref={fileRef} type="file" className="hidden" onChange={onFile} />

      <div className="small mt-2">Shift+Enter for newline • Enter to send</div>
    </div>
  )
}

export default Composer

