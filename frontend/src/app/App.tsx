import './styles.css'
import { Header } from '../components/Header/Header'
import { Sidebar } from '../components/Layout/Sidebar'
import { ChatPanel } from '../components/ChatPanel/ChatPanel'

export default function App() {
  return (
    <div className="page">
      {/* Top bar with title/health */}
      <Header />

      {/* Divided layout: sidebar card + chat card */}
      <div className="main-grid">
        <aside className="sidebar">
          <Sidebar />
        </aside>

        <main className="center">
          <ChatPanel />
        </main>
      </div>
    </div>
  )
}


