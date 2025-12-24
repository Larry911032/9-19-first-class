from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from oauth_google import verify_google_id_token, GOOGLE_CLIENT_ID
from auth_utils import create_access_token, get_current_user_email

app = FastAPI()

class TokenRequest(BaseModel):
    id_token: str

@app.post("/auth/google")
async def google_auth(request: TokenRequest):
    # 1. 驗證 Google 身分
    user_info = verify_google_id_token(request.id_token)
    email = user_info.get("email")
    
    # 2. 發放我們自己的 JWT
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "email": email}

@app.get("/users/me")
async def read_users_me(email: str = Depends(get_current_user_email)):
    return {"message": "驗證成功！", "email": email}

@app.get("/", response_class=HTMLResponse)
def root():
    return f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h2>Google 登入測試</h2>
        <div id="g_id_onload"
             data-client_id="{GOOGLE_CLIENT_ID}"
             data-callback="handleCredentialResponse">
        </div>
        <div class="g_id_signin" data-type="standard"></div>
        <p id="result"></p>
        <script src="https://accounts.google.com/gsi/client" async defer></script>
        <script>
            function handleCredentialResponse(response) {{
                fetch("/auth/google", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ id_token: response.credential }})
                }})
                .then(res => res.json())
                .then(data => {{
                    document.getElementById("result").innerText = 
                        "登入成功！\\nJWT Token: " + data.access_token;
                }});
            }}
        </script>
    </body>
    </html>
    """