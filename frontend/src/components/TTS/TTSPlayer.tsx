import { useState } from 'react'
import { ttsStream } from '../../features/tts'
import { useTtsStore } from '../../state/useTtsStore'

export function TTSPlayer(){
  const base = import.meta.env.VITE_ORCH_BASE || 'http://localhost:8080'
  const { playing, setPlaying } = useTtsStore()
  const [stopper, setStopper] = useState<null | (()=>void)>(null)

  function start(){
    if (playing) return
    setPlaying(true)
    const stop = ttsStream(base, (_chunk) => {
      console.log('[tts] chunk', _chunk)
    }, () => {
      setPlaying(false)
      setStopper(null)
    })
    setStopper(() => stop)
  }

  function stop(){
    stopper?.()
    setPlaying(false)
    setStopper(null)
  }

  return (
    <div className="row">
      <button onClick={start} disabled={playing}>Start TTS (mock)</button>
      <button className="secondary" onClick={stop} disabled={!playing}>Stop</button>
    </div>
  )
}
