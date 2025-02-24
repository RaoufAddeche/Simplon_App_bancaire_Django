from django.shortcuts import render

#room_name allows us to have many discussions groups
def chat_room(request, room_name):
    return render(request, 'chat/chat_room.html', {'room_name': room_name})

def chat_home(request):
    return render(request, 'chat/chat_home.html')