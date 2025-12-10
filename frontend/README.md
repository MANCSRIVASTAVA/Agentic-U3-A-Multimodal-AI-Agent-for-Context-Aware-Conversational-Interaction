# Agentic Frontend (Plain)

React + Vite + TypeScript frontend that talks **only to the Orchestrator**.
Includes MSW mocks to run without a backend.

## Run (mocked)
```bash
npm install
npm run dev
```
Open http://localhost:5173

## Switch to real backend
- Set `VITE_ORCH_BASE` in `.env`
- Disable MSW init in `src/app/main.tsx` (remove `worker.start()`)
- `npm run build && npm run preview`
