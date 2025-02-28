# from django.urls import re_path
# from .consumers import ChatConsumer

# websocket_urlpatterns = [
#     re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
# ]
from django.urls import re_path
from .consumers import ClientChatConsumer, AdvisorChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/advisor/(?P<client_id>\d+)/$", AdvisorChatConsumer.as_asgi()),  # 🔹 Chat privé pour chaque client
    re_path(r"ws/chat/client/$", ClientChatConsumer.as_asgi()),  # 🔹 Chat unique du client vers son conseiller
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
]
