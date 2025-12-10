import { paths } from '../../lib/api'
import { connectWS } from '../../lib/ws'

export function startVoice(base: string, onEvent: (e:{event:string,data:any}) => void){
  const ws = connectWS(base, paths.wsTranscribe, onEvent)
  return ws
}
