from typing import AsyncIterator, Dict, Any
from .tools import rag_retrieve, llm_generate, tts_speak
from .memory import MemoryStore

async def run_turn(text: str, voice: bool, cid: str, sid: str) -> AsyncIterator[Dict[str, Any]]:
    # Yield dict events: {"event": str, "data": Any} in the stable schema.
    mem = MemoryStore()

    # Simple policy: check for knowledge-y cues to use RAG
    is_knowledge = any(q in text.lower() for q in ["what is", "how to", "explain", "compare", "reference", "cite"])
    context = ""
    if is_knowledge:
        res = await rag_retrieve(text, top_k=3, cid=cid, sid=sid)
        context = "\n\n".join([r.get("text","") for r in res.get("results", [])])
        yield {"event":"tool.status","data":{"tool":"rag_retrieve","status":"ok","hits":len(res.get("results",[]))}}

    # Build final prompt
    prompt = f"{context}\n\nUser: {text}\nAssistant:" if context else text

    # LLM
    reply = await llm_generate(prompt, cid=cid, sid=sid)
    await mem.append(sid, "user", text)
    await mem.append(sid, "assistant", reply)

    # Stream tokens primitively (split by space)
    for tok in reply.split(" "):
        yield {"event":"llm.token","data":tok}
    yield {"event":"llm.done","data":{"length":len(reply)}}

    if voice:
        async for chunk in tts_speak(reply, cid=cid, sid=sid):
            yield {"event":"tts.audio.chunk","data":chunk}
        yield {"event":"tts.audio.done","data":{}}  # end of audio
