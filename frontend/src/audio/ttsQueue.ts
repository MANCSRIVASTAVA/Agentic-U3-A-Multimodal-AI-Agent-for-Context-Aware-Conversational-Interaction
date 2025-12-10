export class TtsQueue {
  private items: any[] = []
  push(chunk: any){ this.items.push(chunk) }
  clear(){ this.items = [] }
  size(){ return this.items.length }
}
