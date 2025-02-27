from django.urls import path
from .views import ChatRoomView, ClientChatView

app_name = 'chat'

urlpatterns = [
    path("chat/", ChatRoomView.as_view(), name="chat_room"),
    path("client_chat/<int:client_id>/", ClientChatView.as_view(), name="client_chat"),
    #path("chat/<int:user_id>/", views.chat_view, name="chat"),
]