import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import Message

# ✅ Client Chat Consumer
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
            self.room_group_name = f"chat_{self.user.id}_{self.advisor.id}"  # 🔹 Un seul chat partagé

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

        # Envoi du message à la WebSocket room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "username": self.user.username,
                "timestamp": msg.timestamp.strftime("%H:%M"),
            },
        )

        # 🔴 Envoi d'une notification au conseiller
        await self.channel_layer.group_send(
            f"notifications_{self.advisor.id}",
            {
                "type": "new_message_notification",
                "unread_count": await self.get_unread_count(self.advisor)
            }
        )

    async def chat_message(self, event):
        """Envoi du message au WebSocket"""
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_advisor(self):
        """Récupère le conseiller du client"""
        try:
            return self.user.profile.advisor if hasattr(self.user, "profile") else None
        except User.profile.RelatedObjectDoesNotExist:
            return None

    @sync_to_async
    def save_message(self, message):
        """Sauvegarde le message en base de données"""
        return Message.objects.create(sender=self.user, receiver=self.advisor, content=message)

    @sync_to_async
    def get_unread_count(self, user):
        """Retourne le nombre de messages non lus pour un utilisateur"""
        return Message.objects.filter(receiver=user, is_read=False).count()


# ✅ Advisor Chat Consumer
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
            self.room_group_name = f"chat_{self.client.id}_{self.user.id}"  # 🔹 Même room que le client

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

        # Envoi du message à la WebSocket room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "username": self.user.username,
                "timestamp": msg.timestamp.strftime("%H:%M"),
            },
        )

        # 🔴 Envoi d'une notification au client
        await self.channel_layer.group_send(
            f"notifications_{self.client.id}",
            {
                "type": "new_message_notification",
                "unread_count": await self.get_unread_count(self.client)
            }
        )

    async def chat_message(self, event):
        """Envoi du message au WebSocket"""
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_client(self, client_id):
        """Récupère un client spécifique"""
        try:
            return User.objects.get(pk=client_id)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def save_message(self, message):
        """Sauvegarde le message en base de données"""
        return Message.objects.create(sender=self.user, receiver=self.client, content=message)

    @sync_to_async
    def get_unread_count(self, user):
        """Retourne le nombre de messages non lus pour un utilisateur"""
        return Message.objects.filter(receiver=user, is_read=False).count()


# ✅ Notification Consumer
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connexion WebSocket pour les notifications"""
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_group_name = f"notifications_{self.user.id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # 🔴 Envoi du nombre de messages non lus à la connexion
        await self.send(text_data=json.dumps({
            "unread_count": await self.get_unread_messages(self.user)
        }))

    async def disconnect(self, close_code):
        """Déconnexion WebSocket"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def new_message_notification(self, event):
        """Envoi d'une mise à jour du nombre de messages non lus"""
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def get_unread_messages(self, user):
        """Compte les messages non lus"""
        unread_counts = {}

        if hasattr(user, "profile") and user.profile.advisor:
            advisor = user.profile.advisor
            unread_counts[advisor.id] = Message.objects.filter(receiver=user, sender=advisor, is_read=False).count()
        else:
            clients = User.objects.filter(profile__advisor=user)
            for client in clients:
                unread_counts[client.id] = Message.objects.filter(receiver=user, sender=client, is_read=False).count()

        return unread_counts
