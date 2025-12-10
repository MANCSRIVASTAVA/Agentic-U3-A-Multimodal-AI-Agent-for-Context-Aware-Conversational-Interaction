export function ProvenanceChips({ items }:{ items: { text: string; source_url: string }[] }){
  if(!items?.length) return null
  return (
    <div className="small">
      Sources:{" "}
      {items.map((it, i)=>(
        <a key={i} href={it.source_url} target="_blank" style={{ marginRight: 6 }}>
          [{i+1}]
        </a>
      ))}
    </div>
  )
}
