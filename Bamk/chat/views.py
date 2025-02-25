from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def chat_room(request):
    messages = Message.objects.order_by('-timestamp')[:50]  # Charger les 50 derniers messages
    return render(request, 'chat/chat_room.html', {'messages': messages})

