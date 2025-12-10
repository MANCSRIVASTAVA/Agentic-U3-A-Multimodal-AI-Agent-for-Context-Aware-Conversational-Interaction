from fastapi import HTTPException
def json_error(code: str, message: str, status: int = 400, details=None):
    raise HTTPException(status_code=status, detail={"code":code,"message":message,"details":details})
