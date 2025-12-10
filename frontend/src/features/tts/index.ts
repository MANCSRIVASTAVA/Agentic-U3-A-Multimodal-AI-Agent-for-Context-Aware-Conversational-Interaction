import { paths } from '../../lib/api'
import { connectSSE } from '../../lib/sse'

export function ttsSpeak(text: string){
  if (import.meta.env.DEV){
    const u = new SpeechSynthesisUtterance(text)
    u.rate = 1; u.pitch = 1; u.lang = 'en-US'
    speechSynthesis.speak(u)
    return () => speechSynthesis.cancel()
  }
  const base = (import.meta.env.VITE_ORCH_BASE || 'http://localhost:8080').replace(/\/$/, '')
  const url = base + paths.ttsStream + `?q=${encodeURIComponent(text)}`
  const stop = connectSSE(url, ({event, data})=>{
    console.log('[tts]', event, data)
  })
  return () => stop.close()
}

export function ttsStream(base: string, onChunk: (chunk: any) => void, onComplete: () => void) {
  // Mock implementation for TTS streaming
  if (import.meta.env.DEV) {
    const interval = setInterval(() => {
      onChunk({ type: 'audio', data: 'mock-audio-chunk' })
    }, 100)
    
    setTimeout(() => {
      clearInterval(interval)
      onComplete()
    }, 3000)
    
    return () => clearInterval(interval)
  }
  
  // Production implementation would connect to actual TTS stream
  const url = base.replace(/\/$/, '') + paths.ttsStream
  const stop = connectSSE(url, ({event, data}) => {
    if (event === 'chunk') {
      onChunk(data)
    } else if (event === 'complete') {
      onComplete()
    }
  })
  
  return () => stop.close()
}
