from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from accounts.models import Account
from .models import Message

import json

# chat/views.py
from django.shortcuts import render

@login_required
def index(request):
    return render(request, 'chats/index.html')

@login_required
def room(request):
    username = Account.objects.filter(username=request.user).first()
    messages = Message.objects.filter(author=request.user)
    dms = []
    for message in messages:
        if message.receiver in dms:
            continue
        dms.append(message.receiver)
    return render(request, 'chats/room.html', {
        'username': username,
        'dms': dms
    })