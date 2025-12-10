import { create } from 'zustand'
export type ChatMsg = { role: 'user'|'assistant'; content: string }
type ChatState = {
  messages: ChatMsg[]; streaming: boolean; fallbackUsed: boolean;
  append: (m: ChatMsg) => void; setStreaming: (b: boolean) => void; setFallback: (b: boolean) => void; clear: () => void
}
export const useChatStore = create<ChatState>((set)=> ({
  messages: [], streaming: false, fallbackUsed: false,
  append: (m)=> set(s=>({ messages: [...s.messages, m] })),
  setStreaming: (b)=> set({ streaming: b }),
  setFallback: (b)=> set({ fallbackUsed: b }),
  clear: ()=> set({ messages: [], fallbackUsed: false })
}))
