import { paths, get, postMultipart } from '../../lib/api'

export async function ingest(file: File){
  const fd = new FormData()
  fd.append('file', file, file.name)
  return postMultipart(paths.ingest, fd)
}

export async function retrieve(q: string, top_k=3){
  return get(paths.retrieve, { q, top_k })
}
