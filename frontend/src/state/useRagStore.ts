import { create } from 'zustand'
export type Snippet = { text: string; score: number; source_url: string }
type RagState = { docId?: string; results: Snippet[]; setDocId:(id:string)=>void; setResults:(r:Snippet[])=>void; clear:()=>void }
export const useRagStore = create<RagState>((set)=> ({
  results: [], setDocId:(id)=> set({ docId:id }), setResults:(r)=> set({ results:r }), clear:()=> set({ docId: undefined, results: [] })
}))
