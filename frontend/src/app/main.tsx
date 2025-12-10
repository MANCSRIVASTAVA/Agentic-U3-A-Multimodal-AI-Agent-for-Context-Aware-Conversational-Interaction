import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

async function enableMocksIfDev() {
  if (import.meta.env.DEV) {
    const { worker } = await import('../mocks/browser')
    await worker.start({ onUnhandledRequest: 'bypass' })
    ;(window as any).__MSW_ACTIVE__ = true
  }
}

enableMocksIfDev().finally(() => {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  )
})
