import { uuid } from './uuid'
const SESSION_KEY = 'session_id'
function getSessionId(){
  let sid = localStorage.getItem(SESSION_KEY)
  if(!sid){ sid = uuid(); localStorage.setItem(SESSION_KEY, sid) }
  return sid
}
export function buildHeaders(opts?: { token?: string, correlationId?: string }){
  const token = opts?.token || (import.meta.env.VITE_AUTH_TOKEN || '')
  const headers: Record<string,string> = {
    'X-Session-Id': getSessionId(),
    'X-Request-Id': uuid(),
    'X-Correlation-Id': opts?.correlationId || uuid()
  }
  if (token) headers['Authorization'] = `Bearer ${token}`
  return headers
}
