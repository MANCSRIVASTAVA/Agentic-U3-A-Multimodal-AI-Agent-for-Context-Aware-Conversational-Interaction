import { buildHeaders } from './headers'
// Use relative path when running in container, fallback to localhost for development
const ORCH = (import.meta.env.VITE_ORCH_BASE || '/api').replace(/\/$/, '')
export async function get<T=any>(path: string, params?: Record<string,string | number>){
  const url = new URL(ORCH + path)
  if(params) Object.entries(params).forEach(([k,v]) => url.searchParams.set(k, String(v)))
  const res = await fetch(url.toString(), { headers: buildHeaders() })
  if(!res.ok) throw await res.json().catch(() => ({ message: res.statusText }))
  return res.json() as Promise<T>
}
export async function post<T=any>(path: string, body?: any){
  const url = ORCH + path
  const res = await fetch(url, {
    method: 'POST',
    headers: { ...buildHeaders(), 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined
  })
  if(!res.ok) throw await res.json().catch(() => ({ message: res.statusText }))
  return res.json() as Promise<T>
}
export async function postMultipart<T=any>(path: string, form: FormData){
  const url = ORCH + path
  const res = await fetch(url, { method: 'POST', headers: buildHeaders(), body: form })
  if(!res.ok) throw await res.json().catch(() => ({ message: res.statusText }))
  return res.json() as Promise<T>
}
export const paths = {
  chat: '/v1/chat',
  chatStream: '/v1/chat/stream',
  ttsStream: '/v1/tts/stream',
  ingest: '/v1/ingest',
  retrieve: '/v1/retrieve',
  health: '/v1/health',
  config: '/v1/config',
  wsTranscribe: '/v1/transcribe/ws'
}
