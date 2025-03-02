from django.urls import re_path
from .consumers import ConsumerChat

# web socket url for group chats

websocket_urlpatterns=[
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ConsumerChat.as_asgi()),
]

