import { create } from 'zustand'
type SessionState = { token: string; setToken: (t:string)=>void }
export const useSessionStore = create<SessionState>((set)=>({ token:'', setToken:(t)=>set({token:t}) }))
