from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json
from .models import Chat


# Render index
@login_required
def index(request):
    current_user = request.user
    users = User.objects.exclude(pk=current_user.pk)
    return render(request, "chat/index.html", {'users': users, 'my_username': current_user.username})

# Get chat object
def get_current_chat(chat_id):
    return get_object_or_404(Chat, id=chat_id)

def get_or_create_chat(user1, user2):
    chat = Chat.objects.filter(user1=user1, user2=user2).first() \
           or Chat.objects.filter(user1=user2, user2=user1).first()

    if not chat:
        chat = Chat.objects.create(user1=user1, user2=user2)

    return chat

# Render room by user
@login_required
def room_by_user(request, user_id):
    selected_user = get_object_or_404(User, pk=user_id)
    chat = get_or_create_chat(request.user, selected_user)
    context = {
        'chat_id_json': mark_safe(json.dumps(chat.id)),
        'username': mark_safe(json.dumps(request.user.username)),
    }
    return render(request, 'chat/room.html', context)

# Render room by chat
@login_required
def room_by_chat(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id)
    context = {
        'chat_id_json': mark_safe(json.dumps(chat.id)),
        'username': mark_safe(json.dumps(request.user.username)),
    }
    return render(request, 'chat/room.html', context)
    
