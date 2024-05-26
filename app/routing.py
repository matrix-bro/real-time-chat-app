from django.urls import path
from app.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:conversation_id>/', ChatConsumer.as_asgi()),
]
