from fastapi import FastAPI, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()

fake_user_db = {
    "alice": {"username": "alice", "password": "secret123"}
}

# JWT config
SECRET_KEY = "777"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# 修正 1: 拼字修正 (tpken -> token, delts -> delta)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        # 修正 2: algorithms 需要是 List
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post("/login")
# 修正 3: response 必須加上型別宣告 (: Response)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # 修正函式呼叫名稱
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # 修正 4: samesites -> samesite
    response.set_cookie(
        key="jwt",
        value=access_token,
        httponly=True,
        samesite="lax"
    ) 
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user/me")
def me(
    token: Optional[str] = Depends(oauth2_schema),
    # 修正 5: 加上 alias="jwt" 以對應 login 設定的 cookie 名稱
    jwt_cookie: Optional[str] = Cookie(None, alias="jwt")
):
    if token:
        username = verify_token(token)
    elif jwt_cookie:
        username = verify_token(jwt_cookie)
    else:
        raise HTTPException(status_code=401, detail="Missing token or cookie")
    
    # 修正 6: 加上 f-string
    return {"message": f"Hello, {username}! You are authenticated."}