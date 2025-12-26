import os
# 👇 新增這行：匯入讀取環境變數的功能
from dotenv import load_dotenv 
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi import HTTPException, status

# 👇 這一行會去讀取專案資料夾裡的 .env 檔案
load_dotenv()

# ==========================================
# 👇 改成這樣：從環境變數中讀取，不再寫死字串
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# ==========================================

def verify_google_id_token(token: str):
    try:
        # 這裡會使用上面讀取到的 ID 進行驗證
        idinfo = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        return idinfo
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無效的 Google Token"
        )