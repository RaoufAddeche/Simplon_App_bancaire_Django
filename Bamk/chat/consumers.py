import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from django.utils.timezone import now
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_room"
        self.user = self.scope["user"]  # Récupérer l'utilisateur Django connecté
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # Vérifier si l'utilisateur est authentifié
        if self.user.is_authenticated:
            sender_id = self.user.id
            sender_username = self.user.username
        else:
            sender_id = None
            sender_username = "Anonyme"

        # Sauvegarder le message
        await sync_to_async(self.save_message)(sender_id, message)

        # Envoyer aux autres clients
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": sender_username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))

    # Sauvegarde en base de données
    def save_message(self, sender_id, message):
        sender = User.objects.get(id=sender_id) if sender_id else None
        Message.objects.create(sender=sender, content=message)
