from django.urls import path
from .views import chat_room, chat_home

urlpatterns = [
    path('<str:room_name>/', chat_room, name='chat_room'),
    path('', chat_home, name='chat_home'),
]