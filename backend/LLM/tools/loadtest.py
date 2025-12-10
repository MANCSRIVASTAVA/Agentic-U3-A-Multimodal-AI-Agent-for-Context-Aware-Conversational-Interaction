
#!/usr/bin/env python3
import time, json, sys, requests

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8200/v1/generate"
payload = {
  "messages":[
    {"role":"system","content":"You are terse."},
    {"role":"user","content":"One sentence greeting."}
  ],
  "stream": True,
  "max_tokens": 64,
  "metadata":{"session_id":"local","correlation_id":"loadtest"}
}

print("POST", URL)
with requests.post(URL, json=payload, stream=True) as r:
    r.raise_for_status()
    t0=None
    for line in r.iter_lines(decode_unicode=True):
        if not line: 
            continue
        if line.startswith("event:"):
            evt=line.split(":",1)[1].strip()
        elif line.startswith("data:"):
            data=json.loads(line.split(":",1)[1].strip())
            if evt=="llm.token":
                if t0 is None:
                    t0=time.time()
                    print("first token at ms:", int((time.time()-t0)*1000))
                print(data.get("delta",""), end="", flush=True)
            elif evt=="llm.done":
                print("\nDONE", data)
                break
