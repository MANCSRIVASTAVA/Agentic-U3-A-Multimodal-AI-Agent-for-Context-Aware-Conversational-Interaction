
import os
import io
import uuid
import time
import chardet
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi import HTTPException
from pydantic import BaseModel

from pypdf import PdfReader
try:
    import docx  # python-docx
except Exception:
    docx = None

try:
    import tiktoken
except Exception:
    tiktoken = None

router = APIRouter()

MAX_TOKENS = int(os.getenv("CHUNK_TOKENS", "800"))
OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

class IngestJSON(BaseModel):
    text: str
    doc_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

def _tokenizer():
    if tiktoken:
        return tiktoken.get_encoding("cl100k_base")
    return None

def chunk_text(text: str, max_tokens: int = MAX_TOKENS, overlap: int = OVERLAP) -> List[str]:
    enc = _tokenizer()
    if enc:
        toks = enc.encode(text)
        chunks = []
        i = 0
        while i < len(toks):
            sub = toks[i : i + max_tokens]
            chunks.append(enc.decode(sub))
            i += max_tokens - overlap
        return [c.strip() for c in chunks if c.strip()]

    # Fallback: word-based
    words = text.split()
    approx_ratio = 3  # ~3 chars/token heuristic
    words_per_chunk = max_tokens * approx_ratio
    step = max(1, words_per_chunk - (overlap * approx_ratio))
    chunks = []
    for i in range(0, len(words), step):
        chunks.append(" ".join(words[i : i + words_per_chunk]))
    return [c.strip() for c in chunks if c.strip()]

def extract_from_pdf(bytes_data: bytes) -> List[Dict[str, Any]]:
    reader = PdfReader(io.BytesIO(bytes_data))
    out = []
    for i, page in enumerate(reader.pages, start=1):
        txt = page.extract_text() or ""
        out.append({"page": i, "text": txt})
    return out

def extract_from_docx(bytes_data: bytes) -> List[Dict[str, Any]]:
    if not docx:
        raise HTTPException(status_code=400, detail="DOCX support not installed. Install python-docx.")
    fh = io.BytesIO(bytes_data)
    document = docx.Document(fh)
    text = "\n".join(p.text for p in document.paragraphs)
    return [{"page": 0, "text": text}]

def extract_from_txt(bytes_data: bytes) -> List[Dict[str, Any]]:
    detected = chardet.detect(bytes_data)
    encoding = detected.get("encoding") or "utf-8"
    text = bytes_data.decode(encoding, errors="ignore")
    return [{"page": 0, "text": text}]

def guess_ext(filename: Optional[str]) -> str:
    if not filename:
        return "bin"
    return (filename.split(".")[-1] or "bin").lower()

@router.post("/ingest")
async def ingest(
    request: Request,
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
):
    """Accepts multipart (file or form-text) OR JSON {text, doc_id?, metadata?}.
    Stores raw to MinIO (app-bucket), extracts+chunks+embeds, upserts to Qdrant.
    Returns: {doc_id, chunks_ingested}
    """
    app = request.app
    minio = app.state.minio
    qdrant = app.state.qdrant
    embedder = app.state.embedder
    metrics = app.state.metrics

    user_id = request.headers.get("X-User-Id", "anon")
    session_id = request.headers.get("X-Session-Id", "default")

    # Normalize input
    body: Optional[Dict[str, Any]] = None
    if request.headers.get("content-type", "").startswith("application/json"):
        body = await request.json()

    input_text: Optional[str] = None
    metadata: Dict[str, Any] = {}
    doc_id = None

    if body and body.get("text"):
        input_text = str(body["text"])[:10_000_000]
        doc_id = body.get("doc_id")
        metadata = body.get("metadata") or {}

    source_key = None
    source_url = None

    # File path
    if file is not None:
        data = await file.read()
        ext = guess_ext(file.filename)
        source_key = minio.build_object_key(user_id, session_id, ext)
        minio.put_bytes(source_key, data, content_type=file.content_type)
        source_url = minio.presigned_get(source_key)

        if ext in ("pdf",):
            pages = extract_from_pdf(data)
        elif ext in ("docx", "doc"):
            pages = extract_from_docx(data)
        elif ext in ("txt", "md"):
            pages = extract_from_txt(data)
        else:
            raise HTTPException(status_code=415, detail=f"Unsupported file type: .{ext}")

        corpus = "\n\n".join(p.get("text", "") for p in pages)
        _doc_id = doc_id or uuid.uuid4().hex
    elif input_text:
        corpus = input_text
        _doc_id = doc_id or uuid.uuid4().hex
    else:
        raise HTTPException(status_code=400, detail="Provide a file upload or JSON with 'text'.")

    start = time.perf_counter()
    chunks = chunk_text(corpus)

    e0 = time.perf_counter()
    vectors = embedder.embed(chunks)
    e1 = time.perf_counter()
    metrics["EMBED_LATENCY"].observe(e1 - e0)

    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    payloads = []
    for i, chunk in enumerate(chunks):
        payloads.append({
            "doc_id": _doc_id,
            "chunk_id": i,
            "page": 0,
            "source_url": source_url,
            "object_key": source_key,
            "created_at": now_iso,
            **(metadata or {}),
        })

    qdrant.upsert(texts=chunks, vectors=vectors, payloads=payloads)

    duration = time.perf_counter() - start
    metrics["INGEST_DURATION"].observe(duration)
    metrics["CHUNKS_INGESTED"].inc(len(chunks))

    return {"doc_id": _doc_id, "chunks_ingested": len(chunks)}
