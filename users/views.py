from django.shortcuts import render,redirect
import requests
from django.conf import settings
from django.http import JsonResponse,StreamingHttpResponse
import pickle
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.contrib.auth.models import User
from .models import UserTokens
from django.utils.timezone import now,timedelta
from .utils import get_valid_token,get_user_credentials
def login(request):
    """
    Manage google login and redirect user for Oauth autentication
    """
    client_id =settings.GOOGLE_CLIENT_ID
    redirect_url = "http://" + request.get_host() + settings.REDIRECT_URL
    print(redirect_url)
    auth_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={client_id}&redirect_uri={redirect_url}&scope=https://www.googleapis.com/auth/drive.file openid email profile&access_type=offline&prompt=consent"

    return redirect(auth_url)





def google_callback(request):
    """
    Google callback for authorization
    """
    tokens = get_user_credentials(request)
    if "error" in tokens:
        return JsonResponse({"error":tokens["error"]},status=400)
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    user_info_response = requests.get(user_info_url,headers=headers)
    user_info = user_info_response.json()
    user_object,created = User.objects.get_or_create(username=user_info["email"])
    
    user_token = UserTokens.objects.update_or_create(
        user=user_object,
        defaults={
            "access_token" : tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "expires_at": now() + timedelta(seconds=tokens["expires_in"]),
        }
    )
    return JsonResponse(user_info)



@csrf_exempt
def upload_file_google_drive(request):
    """
    Upload file to google drive
    """
    user = request.GET.get("user")
    if not user:
        return JsonResponse({"error":"please send the user"},status=400)
    
    token = get_valid_token(user)
    if not token:
        return redirect("/auth/login/")
 

    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES.get("file")
        
        
    else:
        return JsonResponse({"error":"Please select file to upload or user missing"},status=400)    
   
    headers = {"Authorization":f"Bearer {token}"}    
    DRIVE_API_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
    metadata = {
        "name": uploaded_file.name,
        "parents": ["root"],
    }
    files = {
        "metadata": ("metadata.json",json.dumps(metadata),"application/json"),
        "file": (uploaded_file.name,uploaded_file.read(),uploaded_file.content_type),
    }
    response = requests.post(url=DRIVE_API_URL,headers=headers,files=files)
    return JsonResponse(response.json())


  


def list_drive_files(request):
    """
    List google drive files
    """
    user = request.GET.get("user")
    if not user:
        return JsonResponse({"error":"please send the user"},status=400)
    
    token = get_valid_token(user)
    
    if not token:
        return redirect("/auth/login/")
    headers = {"Authorization":f"Bearer {token}"} 
    LIST_DRIVE_API_URL="https://www.googleapis.com/drive/v3/files"
    response = requests.get(url=LIST_DRIVE_API_URL,headers=headers)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({"error":"Failed to fetch files"},status=400)
    



def download_drive_file(request,file_id):
    """
    Dowload file from google drive
    """
    user = request.GET.get("user")
    if not user:
        return JsonResponse({"error":"please send the user"},status=400)
    
    token = get_valid_token(user)
    if not token:
        return redirect("/auth/login/")
    headers = {"Authorization":f"Bearer {token}"}
    # Fetch meta data of file from google drive
    META_DATA_DRIVE_API_URL = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=name,mimeType"
    meta_response = requests.get(url=META_DATA_DRIVE_API_URL,headers=headers).json()
    file_name = meta_response.get("name","download_file")
    mime_type = meta_response.get("mimeType","application/octet-stream")

    # Prepare the file to download
    DOWNLOAD_DRIVE_API_URL=f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    response = requests.get(url=DOWNLOAD_DRIVE_API_URL,headers=headers,stream=True)
    if response.status_code == 200:
        
        response = StreamingHttpResponse(response.iter_content(chunk_size=1080),content_type=mime_type)
        response["Content-Disposition"] = f'attachment; filename="{file_name}"'
        return response
    else: 
        return JsonResponse({"error":"Failed to download"},status=response.status_code)
    



    