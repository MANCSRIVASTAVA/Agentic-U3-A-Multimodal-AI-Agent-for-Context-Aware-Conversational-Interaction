import { http, HttpResponse, delay } from 'msw'
const json = (data: any) => HttpResponse.json(data)

export const handlers = [
  http.get('*/v1/health', async () => { await delay(100); return json({ status: 'OK', timestamp: Date.now() }) }),
  http.get('*/v1/config', async () => { await delay(100); return json({ name: 'mock-orchestrator', features: { sse: true, ws: true }, models: { llm: 'gpt-mock' } }) }),
  http.post('*/v1/chat', async () => { await delay(250); return json({ answer: 'Mocked non-stream answer.', fallback_used: false }) }),
  http.get('*/v1/chat/stream', () => {
    const encoder = new TextEncoder()
    const stream = new ReadableStream<Uint8Array>({
      start(controller) {
        const send = (event: string, data: any) => {
          controller.enqueue(encoder.encode(`event: ${event}\n`))
          controller.enqueue(encoder.encode(`data: ${typeof data === 'string' ? data : JSON.stringify(data)}\n\n`))
        }
        const tokens = ['R','A','G',' ','=',' ','Retrieval','-Augmented ','Generation']
        let i = 0
        const iv = setInterval(() => {
          if (i < tokens.length) send('llm.token', tokens[i++]); else { clearInterval(iv); send('llm.done', { fallback_used: false }); controller.close() }
        }, 150)
      }
    })
    return new Response(stream, { headers: { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' } })
  }),
  http.get('*/v1/tts/stream', () => {
    const encoder = new TextEncoder()
    const stream = new ReadableStream<Uint8Array>({
      start(controller) {
        const send = (event: string, data: any) => {
          controller.enqueue(encoder.encode(`event: ${event}\n`))
          controller.enqueue(encoder.encode(`data: ${typeof data === 'string' ? data : JSON.stringify(data)}\n\n`))
        }
        let i = 0; const iv = setInterval(() => { if (i++ < 3) send('tts.audio.chunk', { seq: i }); else { clearInterval(iv); send('tts.done', {}); controller.close() } }, 300)
      }
    })
    return new Response(stream, { headers: { 'Content-Type': 'text/event-stream' } })
  }),
  http.post('*/v1/ingest', async () => { await delay(200); return json({ doc_id: `doc_${Math.random().toString(36).slice(2,7)}`, chunks_ingested: 5 }) }),
  http.get('*/v1/retrieve', async ({ request }) => {
    await delay(200)
    const url = new URL(request.url)
    const q = url.searchParams.get('q') || ''
    const results = [
      { text: `Snippet about ${q} #1`, score: 0.91, source_url: 'https://example.com/doc1#frag' },
      { text: `Snippet about ${q} #2`, score: 0.85, source_url: 'https://example.com/doc2#frag' },
      { text: `Snippet about ${q} #3`, score: 0.79, source_url: 'https://example.com/doc3#frag' }
    ]
    return json({ results })
  })
]
