from django.contrib.auth.models import User
from .models import UserTokens
from django.utils.timezone import now,timedelta
from django.conf import settings
import requests

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def get_refresh_access_token(refresh_token: str):
    data = {
        "client_id":settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_access": "refresh_token",
    }
    response = requests.post(url=GOOGLE_TOKEN_URL,json=data)
    return response.json()

def get_valid_token(user: str):
    try:
        user = User.objects.get(username=user)
        user_token = UserTokens.objects.get(user=user.id)
    except Exception:
        return None    
    if user_token.expires_at < now():
        new_access_token = get_refresh_access_token(user_token.refresh_token)
        user_token.access_token = new_access_token["access_token"]
        user_token.expires_at = now() + timedelta(seconds=new_access_token["expires_in"])
        user_token.save()
    return user_token.access_token

def get_user_credentials(request):
    code = request.GET.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://" + request.get_host() + settings.REDIRECT_URL,
        "grant_type": "authorization_code",
    }
    
    response = requests.post(token_url,data=data)
    
    tokens = response.json()
    

    return tokens