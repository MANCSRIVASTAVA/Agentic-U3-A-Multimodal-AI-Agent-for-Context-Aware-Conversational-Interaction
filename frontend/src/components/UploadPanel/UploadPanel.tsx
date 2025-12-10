import { useState } from 'react'
import { ingest, retrieve } from '../../features/rag'
import { useRagStore } from '../../state/useRagStore'

export function UploadPanel(){
  const [file, setFile] = useState<File | null>(null)
  const { setDocId, setResults, results } = useRagStore()

  async function doIngest(){
    if(!file) return
    const res = await ingest(file)
    setDocId(res.doc_id)
    alert(`Ingested: ${res.doc_id} chunks=${res.chunks_ingested}`)
  }

  async function doRetrieve(){
    const r = await retrieve('What is RAG?', 3)
    setResults(r.results || [])
  }

  return (
    <div>
      <input type="file" onChange={e=>setFile(e.target.files?.[0] || null)} />
      <div className="row" style={{marginTop:8}}>
        <button onClick={doIngest}>POST /v1/ingest</button>
        <button className="secondary" onClick={doRetrieve}>GET /v1/retrieve</button>
      </div>
      <ul className="prov" style={{marginTop:8}}>
        {results.map((s,i)=>(
          <li key={i}><a href={s.source_url} target="_blank">{s.text}</a> <span className="small">({s.score.toFixed(2)})</span></li>
        ))}
      </ul>
    </div>
  )
}
