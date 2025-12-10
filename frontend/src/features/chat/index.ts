import { paths, post } from '../../lib/api'
import { connectSSE } from '../../lib/sse'

export async function chatOnce(messages: any[]){
  // Convert messages to the format expected by orchestrator
  const lastMessage = messages[messages.length - 1]
  return post(paths.chat, { 
    query: lastMessage.content,
    session_id: 'frontend_session'
  })
}

export function chatStream(base: string, messages: any[], onToken: (t: string) => void, onDone: (meta?: any) => void){
  const url = base.replace(/\/$/, '') + paths.chatStream
  const lastMessage = messages[messages.length - 1]
  
  // Send the request body with the query
  const requestBody = {
    query: lastMessage.content,
    session_id: 'frontend_session'
  }
  
  const controller = connectSSE(url, ({ event, data }) => {
    if (event === 'llm.token') onToken(typeof data === 'string' ? data : data?.token ?? '')
    if (event === 'llm.done') onDone(data)
  }, requestBody)
  return () => controller.close()
}
