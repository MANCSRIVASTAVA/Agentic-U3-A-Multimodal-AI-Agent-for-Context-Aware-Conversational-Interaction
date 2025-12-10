import { create } from 'zustand'
import type { ChatMsg } from './useChatStore'

type Session = { id: string; title: string; createdAt: number; messages: ChatMsg[] }
type HS = {
  sessions: Session[]
  currentId?: string
  createSession: ()=>void
  selectSession: (id: string)=>void
  deleteSession: (id: string)=>void
  upsertCurrent: (messages: ChatMsg[])=>void
}
const KEY='chat_sessions_v1'

function load(): { sessions: Session[], currentId?: string }{
  try{ const raw = localStorage.getItem(KEY); if(raw) return JSON.parse(raw) }catch{}
  const id = crypto.randomUUID()
  return { sessions: [{ id, title: 'New chat', createdAt: Date.now(), messages: [] }], currentId: id }
}
function save(s: { sessions: Session[], currentId?: string }){ localStorage.setItem(KEY, JSON.stringify(s)) }

export const useHistoryStore = create<HS>((set,get)=> ({
  ...load(),
  createSession(){
    const id = crypto.randomUUID()
    const s = get()
    const next = { sessions: [{ id, title: 'New chat', createdAt: Date.now(), messages: [] }, ...s.sessions], currentId: id }
    save(next); set(next)
  },
  selectSession(id){
    const s = get(); if(!s.sessions.find(x=>x.id===id)) return
    const next = { ...s, currentId: id }; save(next); set(next)
  },
  deleteSession(id){
    const s = get()
    const sessions = s.sessions.filter(x=>x.id!==id)
    const currentId = s.currentId===id ? sessions[0]?.id : s.currentId
    const next = { sessions, currentId }
    save(next); set(next)
  },
  upsertCurrent(messages){
    const s = get(); if(!s.currentId) return
    const sessions = s.sessions.map(sess => sess.id===s.currentId ? { ...sess, messages, title: messages.find(m=>m.role==='user')?.content?.slice(0,40)||sess.title } : sess)
    const next = { ...s, sessions }
    save(next); set(next)
  }
}))
