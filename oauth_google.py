import os
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi import HTTPException, status

# ==========================================
# 👇 請把剛剛網頁複製的那串 ID 貼在引號裡面 👇
GOOGLE_CLIENT_ID = "906734171074-p1ntt61k0milmuhakfng2h1740dnb7ep.apps.googleusercontent.com"
# ==========================================

def verify_google_id_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        return idinfo
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的 Google Token"
        )