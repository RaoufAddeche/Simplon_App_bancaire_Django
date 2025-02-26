from django.urls import path, include
from .views import chat_room

urlpatterns = [
    path('', chat_room, name='chat'),
]