import { useHistoryStore } from '../../state/useHistoryStore'

export function Sidebar(){
  const { sessions, currentId, createSession, selectSession, deleteSession } = useHistoryStore()
  return (
    <aside className="sidebar">
      <div className="mb-2 flex items-center justify-between">
        <div className="text-sm font-semibold text-slate-300">Chats</div>
        <button className="btn-icon" onClick={()=>createSession()}>＋</button>
      </div>
      <div className="space-y-1">
        {sessions.map(s => (
          <div key={s.id} className={`flex items-center justify-between rounded-xl px-2 py-1 text-sm ${s.id===currentId ? 'bg-slate-800/60' : 'bg-transparent hover:bg-slate-800/40'}`}>
            <button className="text-left flex-1 truncate" onClick={()=>selectSession(s.id)}>{s.title || 'New chat'}</button>
            <button className="ml-2 text-slate-400 hover:text-rose-300" onClick={()=>deleteSession(s.id)}>×</button>
          </div>
        ))}
        {sessions.length===0 && <div className="small">No chats yet.</div>}
      </div>
    </aside>
  )
}
