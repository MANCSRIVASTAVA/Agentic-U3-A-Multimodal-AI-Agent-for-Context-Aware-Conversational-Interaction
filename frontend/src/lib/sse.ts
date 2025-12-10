type EventHandler = (evt: { event: string; data: any }) => void
export function connectSSE(url: string, onEvent: EventHandler, body?: any){
  let aborted = false
  const controller = new AbortController()
  const decoder = new TextDecoder()
  const state = { buffer: '', event: 'message' }
  async function start(){
    const res = await fetch(url, {
      method: body ? 'POST' : 'GET',
      headers: { 
        'Accept': 'text/event-stream',
        ...(body ? { 'Content-Type': 'application/json' } : {})
      },
      body: body ? JSON.stringify(body) : undefined,
      signal: controller.signal
    })
    if (!res.ok || !res.body) throw new Error('SSE connection failed')
    const reader = res.body.getReader()
    while(!aborted){
      const { value, done } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value, { stream: true })
      parseChunk(chunk)
    }
  }
  function parseChunk(chunk: string){
    state.buffer += chunk
    let idx
    while((idx = state.buffer.indexOf('\n')) >= 0){
      const line = state.buffer.slice(0, idx).trimEnd()
      state.buffer = state.buffer.slice(idx + 1)
      if(line === '') { continue }
      if(line.startsWith('event:')){
        state.event = line.slice(6).trim()
      } else if(line.startsWith('data:')){
        const payload = line.slice(5).trim()
        let data: any = payload
        try { data = JSON.parse(payload) } catch {}
        onEvent({ event: state.event, data })
      }
    }
  }
  start().catch(err => onEvent({ event: 'error', data: String(err) }))
  return { close(){ aborted = true; controller.abort() } }
}
