import { create } from 'zustand'
type TtsState = { playing: boolean; setPlaying:(b:boolean)=>void }
export const useTtsStore = create<TtsState>((set)=>({ playing:false, setPlaying:(b)=>set({playing:b}) }))
