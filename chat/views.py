from django.shortcuts import render

# Create your views here.


def chat(request):
    """
    A simple route to render chat tamplate to user
    """
    return render(request,"chat/chat.html")