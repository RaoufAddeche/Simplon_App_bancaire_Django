from django.urls import path, include
from .views import chat_room

app_name = 'chat'

urlpatterns = [
    path('chat/', chat_room, name='chat'),
    #path("chat/<int:user_id>/", views.chat_view, name="chat"),

]