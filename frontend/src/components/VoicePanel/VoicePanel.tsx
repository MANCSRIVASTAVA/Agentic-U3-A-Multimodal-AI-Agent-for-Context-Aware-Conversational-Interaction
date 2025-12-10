import { useState } from 'react'
import { useVoiceStore } from '../../state/useVoiceStore'
import { startVoice } from '../../features/voice'
import { LevelsMeter } from './LevelsMeter'

export function VoicePanel(){
  const base = import.meta.env.VITE_ORCH_BASE || 'http://localhost:8080'
  const { partial, finalText, setPartial, setFinal, setRecording } = useVoiceStore()
  const [wsCtl, setWsCtl] = useState<any>(null)

  function start(){
    setRecording(true)
    const ctl = startVoice(base, ({event, data}) => {
      if(event === 'transcript.partial') setPartial(data.text)
      if(event === 'transcript.final') setFinal(data.text)
    })
    setWsCtl(ctl)
  }

  function stop(){
    setRecording(false)
    wsCtl?.close()
  }

  return (
    <div>
      <div className="row">
        <button onClick={start}>Start (mock)</button>
        <button className="secondary" onClick={stop}>Stop</button>
      </div>
      <LevelsMeter />
      <div className="small"><b>Partial:</b> {partial || '—'}</div>
      <div className="small"><b>Final:</b> {finalText || '—'}</div>
    </div>
  )
}
