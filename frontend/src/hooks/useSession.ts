import { useEffect, useMemo, useState } from 'react'
import { buildHeaders } from '../lib/headers'

export function useSession(){
  const [correlationId, setCorrelationId] = useState<string>('')
  const headers = useMemo(()=> buildHeaders({ correlationId }), [correlationId])
  useEffect(()=>{ setCorrelationId(crypto.randomUUID()) }, [])
  return { headers, newCorrelation: ()=>setCorrelationId(crypto.randomUUID()) }
}
