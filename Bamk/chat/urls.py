from django.urls import path
from .views import chat_room

urlpatterns = [
    path('/chat', chat_room, name='chat'),
    #path("chat/<int:user_id>/", views.chat_view, name="chat"),

]