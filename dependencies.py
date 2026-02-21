from fastapi import Request, HTTPException
from jose import jwt, JWTError
from auth import SECRET_KEY, ALGORITHM

def get_current_user(request: Request):
    token = request.cookies.get("token")

    if not token:
        raise HTTPException(status_code=401)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401)
        return email
    except JWTError:
        raise HTTPException(status_code=401)