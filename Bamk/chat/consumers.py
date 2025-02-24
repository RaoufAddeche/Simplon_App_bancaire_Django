import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from django.utils.timezone import now
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        print("📥 Message reçu dans WebSocket")
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]

        print(f"📨 Message: {message}, Username: {username}")

        # Utiliser sync_to_async pour exécuter les requêtes ORM
        sender = await sync_to_async(self.get_or_create_user)(username)
        await sync_to_async(self.save_message)(sender, message)

        # Envoie du message aux autres clients connectés
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))

    # Fonctions synchrones appelées via sync_to_async
    def get_or_create_user(self, username):
        sender, _ = User.objects.get_or_create(username=username)
        return sender

    def save_message(self, sender, message):
        Message.objects.create(sender=sender, content=message)
