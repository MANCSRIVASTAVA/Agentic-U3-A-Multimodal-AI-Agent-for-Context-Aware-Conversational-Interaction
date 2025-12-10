type WSHandler = (evt: { event: string; data: any }) => void

export function connectWS(base: string, path: string, onEvent: WSHandler){
  const useMock = (window as any).__MSW_ACTIVE__

  if (useMock){
    let closed = false
    const timers: number[] = []
    timers.push(window.setTimeout(() => !closed && onEvent({ event: 'transcript.partial', data: { text: 'hello ' } }), 200))
    timers.push(window.setTimeout(() => !closed && onEvent({ event: 'transcript.partial', data: { text: 'hello world' } }), 500))
    timers.push(window.setTimeout(() => !closed && onEvent({ event: 'transcript.final', data: { text: 'hello world (final)' } }), 1200))
    return {
      send(_b: ArrayBuffer | Uint8Array){ /* mock ignores */ },
      close(){ closed = true; timers.forEach(t => clearTimeout(t)) }
    }
  }

  const proto = location.protocol === 'https:' ? 'wss' : 'ws'
  const url = `${proto}://${new URL(base).host}${path}`
  const ws = new WebSocket(url)
  ws.binaryType = 'arraybuffer'
  ws.onmessage = (e) => {
    try {
      const msg = JSON.parse(typeof e.data === 'string' ? e.data : new TextDecoder().decode(e.data))
      onEvent({ event: msg.event || 'message', data: msg.data })
    } catch {
      // ignore
    }
  }
  return {
    send(b: ArrayBuffer | Uint8Array){ ws.send(b) },
    close(){ ws.close() }
  }
}
