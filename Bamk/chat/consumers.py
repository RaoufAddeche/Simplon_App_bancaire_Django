import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import Message

class ClientChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connexion WebSocket pour le chat unique d'un client vers son conseiller"""
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        # Vérifie que l'utilisateur a un conseiller
        self.advisor = await self.get_advisor()

        if self.advisor:
            self.room_group_name = f"client_chat_{self.user.id}"  # 🔹 Un seul chat par client

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Déconnexion WebSocket"""
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Réception d’un message et enregistrement en base"""
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return

        # Sauvegarde en base de données
        msg = await self.save_message(message)

        # Envoi du message à la room WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "username": self.user.username,
                "timestamp": msg.timestamp.strftime("%H:%M"),
            },
        )

    async def chat_message(self, event):
        """Envoi du message au WebSocket"""
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_advisor(self):
        """Récupère le conseiller du client"""
        return self.user.profile.advisor if hasattr(self.user, "profile") else None

    @sync_to_async
    def save_message(self, message):
        """Sauvegarde le message en base de données"""
        return Message.objects.create(sender=self.user, receiver=self.advisor, content=message)

class AdvisorChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connexion WebSocket pour le conseiller qui parle à un client spécifique"""
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        # Récupère l'ID du client depuis l'URL WebSocket
        self.client_id = self.scope["url_route"]["kwargs"]["client_id"]
        self.client = await self.get_client(self.client_id)

        if self.client:
            self.room_group_name = f"advisor_chat_{self.user.id}_{self.client.id}"  # 🔹 Une room par client

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        """Déconnexion WebSocket"""
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Réception d’un message et enregistrement en base"""
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return

        # Sauvegarde en base de données
        msg = await self.save_message(message)

        # Envoi du message aux WebSockets connectés
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "username": self.user.username,
                "timestamp": msg.timestamp.strftime("%H:%M"),
            },
        )

    async def chat_message(self, event):
        """Envoi du message au WebSocket"""
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_client(self, client_id):
        """Récupère un client spécifique"""
        return User.objects.get(pk=client_id)

    @sync_to_async
    def save_message(self, message):
        """Sauvegarde le message en base de données"""
        return Message.objects.create(sender=self.user, receiver=self.client, content=message)
