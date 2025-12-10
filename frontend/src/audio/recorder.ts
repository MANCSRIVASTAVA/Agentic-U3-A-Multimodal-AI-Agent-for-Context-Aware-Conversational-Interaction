export async function getMicStream(): Promise<MediaStream> {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, sampleRate: 16000 }, video: false })
  return stream
}

export function startMediaRecorder(stream: MediaStream, onChunk: (blob: Blob)=>void): MediaRecorder {
  const mime = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
    ? 'audio/webm;codecs=opus'
    : (MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : '')
  const rec = new MediaRecorder(stream, mime ? { mimeType: mime, audioBitsPerSecond: 48000 } : undefined)
  rec.ondataavailable = (e) => {
    if (e.data && e.data.size > 0) onChunk(e.data)
  }
  rec.start(250) // emit chunks every 250ms
  return rec
}

export function stopMediaRecorder(rec: MediaRecorder){
  try{ rec.stop() }catch{}
  rec.stream.getTracks().forEach(t => t.stop())
}
