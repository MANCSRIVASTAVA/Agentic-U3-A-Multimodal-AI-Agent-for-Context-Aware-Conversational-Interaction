import base64

def to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode()
