from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.adapters.google_auth_adapter import exchange_code_for_token, get_user_info, authenticate_google_user
from app.core.config import settings

router = APIRouter()

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
REDIRECT_URI = "http://localhost:8000/auth/google/callback"

@router.get("/google")
def google_auth_redirect():

    google_oauth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=email%20profile"
        f"&access_type=offline"
    )

    return RedirectResponse(url=google_oauth_url)

@router.get("/google/callback")
def google_auth_callback(code: str = Query(...), db: Session = Depends(get_db)):

    token_response = exchange_code_for_token(code)

    if "error" in token_response:
        raise HTTPException(status_code=400, detail=token_response["error_description"])

    user_info = get_user_info(token_response["access_token"])

    jwt_response = authenticate_google_user(db, user_info)
    
    return RedirectResponse(f"http://localhost:5173/dashboard?access_token={jwt_response['access_token']}")