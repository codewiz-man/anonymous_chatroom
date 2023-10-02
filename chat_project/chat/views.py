from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from chat.models import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

def get_username(request):
    if request.method == "GET":
        return render(request, 'chat/get_username.html')
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        if username == '':
            return HttpResponse("Username is invalid")
        if not User.objects.filter(username=username).exists():
            user = User.objects.create(username=username)
            login(request, user)
            return redirect('/chat_room/')
        else:
            #user = User.objects.get(username=username)
            return HttpResponse("Username Taken.")
        

def check_username(request):
    username = request.GET.get('username', None)
    if (username == '') or (username == None):
        return HttpResponse("Username is invalid")
    data = {'is_taken': User.objects.filter(username=username).exists()}
    return JsonResponse(data)

def chat_room(request, group_name):
    if not request.user.is_authenticated:
        return redirect('/chat_room/get_username/')

    try:
        msgs = Message.objects.get(group=ChatGroup.objects.get(name=group_name))
    except Message.DoesNotExist:
        msgs = [] 
    except ChatGroup.DoesNotExist:
        msgs = []
    return render(request, 'chat/chat.html', {
        'group_name': group_name,
        'messages': msgs,
        'username': request.user
    })



def list_chat_groups(request):
    if not request.user.is_authenticated:
        return redirect('/chat_room/get_username/')
    return render(request, 'chat/chat_groups.html', {'chat_groups': ChatGroup.objects.all()})

def add_chat_group(request):
    if not request.user.is_authenticated:
        return redirect('/chat_room/get_username/')
    
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
    if not request.user.is_authenticated:
        return redirect('/chat_room/get_username/')
    group = get_object_or_404(ChatGroup, name=group_name)
    group.delete()
    return redirect('/chat_room/')
