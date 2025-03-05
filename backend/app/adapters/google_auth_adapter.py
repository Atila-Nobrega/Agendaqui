import requests
from sqlalchemy.orm import Session
from app.core.config import settings
from app.logic.auth import create_access_token
from app.db.user import get_user_by_id, create_user

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def exchange_code_for_token(auth_code: str):
    
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": auth_code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    }
    
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    return response.json()

def get_user_info(access_token: str):
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)
    return response.json()

def authenticate_google_user(db: Session, user_info: dict):
    
    user = get_user_by_id(db, user_info["id"])
    
    if not user:
        user_data = {
            "id": user_info["id"],
            "email": user_info["email"],
            "name": user_info["name"],
            "picture": user_info.get("picture", ""),
            "verified": user_info["verified_email"]
        }
        user = create_user(db, user_data)
    
    # Gerar um JWT para autenticação da API
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value, "name": user.name, "email": user.email, "picture": user.picture, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}