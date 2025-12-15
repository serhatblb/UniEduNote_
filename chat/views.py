from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatMessage
import json

@login_required(login_url='/login/')
def chat_room(request):
    return render(request, 'chat/room.html')

@login_required
def get_messages(request):
    messages = ChatMessage.objects.all().order_by('-created_at')[:50] # Son 50 mesaj
    data = [{
        'user': m.user.username,
        'avatar_url': m.user.avatar.url if m.user.avatar else None,
        'message': m.message,
        'created_at': m.created_at.strftime('%H:%M')
    } for m in reversed(messages)]
    return JsonResponse({'messages': data})

@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        msg = data.get('message')
        if msg:
            ChatMessage.objects.create(user=request.user, message=msg)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})