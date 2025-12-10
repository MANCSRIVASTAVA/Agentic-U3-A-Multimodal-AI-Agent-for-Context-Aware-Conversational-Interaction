import { create } from 'zustand'
type VoiceState = { recording: boolean; partial: string; finalText: string;
  setRecording:(b:boolean)=>void; setPartial:(t:string)=>void; setFinal:(t:string)=>void; clear:()=>void }
export const useVoiceStore = create<VoiceState>((set)=> ({
  recording:false, partial:'', finalText:'',
  setRecording:(b)=> set({ recording:b }),
  setPartial:(t)=> set({ partial:t }),
  setFinal:(t)=> set({ finalText:t }),
  clear:()=> set({ partial:'', finalText:'' })
}))
