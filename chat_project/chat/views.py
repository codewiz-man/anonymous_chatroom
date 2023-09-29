from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from chat.models import *

def chat_room(request, group_name):
    try:
        msgs = Message.objects.get(group=ChatGroup.objects.get(name=group_name))
    except Message.DoesNotExist:
        msgs = [] 
    except ChatGroup.DoesNotExist:
        msgs = []
    return render(request, 'chat/chat_room.html', {
        'group_name': group_name,
        'messages': msgs
    })

def list_chat_groups(request):
    return render(request, 'chat/chat_groups.html', {'chat_groups': ChatGroup.objects.all()})

def add_chat_group(request):
    print(request.POST)
    print(request.POST['group_name'])
    name = request.POST['group_name']
    
    try:
        group = ChatGroup.objects.get(name=name)
        return HttpResponse('Group Name Already Exists')
    except ChatGroup.DoesNotExist:
        ChatGroup.objects.create(name=name)
        return  HttpResponseRedirect('/chat_room/')
    

def delete_chat_group(request, group_name):
    group = get_object_or_404(ChatGroup, name=group_name)
    group.delete()
    return redirect('/chat_room/')
