from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render

from chat.models import *
from django.http import JsonResponse
#from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from .consumers import get_consumer_count
import json

def get_username(request):
    if request.method == "GET":
        return render(request, 'chat/get_username.html')
    if request.method == "POST":
        print(request.POST)
        username = request.POST['username']
        if username == '':
            return HttpResponse("Username is invalid")
        if not ChatUser.objects.filter(username=username).exists():
            user = ChatUser.objects.create(username=username)
            login(request, user)
            return redirect('/chat_room/')
        else:
            #user = User.objects.get(username=username)
            return HttpResponse("Username Taken.")
        

def check_username(request):
    username = request.GET.get('username', None)
    if (username == '') or (username == None):
        return HttpResponse("Username is invalid")
    data = {'is_taken': ChatUser.objects.filter(username=username).exists()}
    return JsonResponse(data)

def chat_room(request, group_name):
    if not request.user.is_authenticated:
        return redirect('/chat_room/get_username/')
    
    #print(group_name)
    #print(ChatGroup.objects.get(name=group_name))

    try:
        group = ChatGroup.objects.get(name=group_name)
        #print(group)
        #if group != None:
        msgs = Message.objects.get(group=group)
        #else:
            
    except Message.DoesNotExist:
        msgs = [] 
    except ChatGroup.DoesNotExist:
        msgs = []
        print("group name does not exists")
        return HttpResponse("Chat Group not found")
    return render(request, 'chat/chat.html', {
        'group_name': group_name,
        'messages': msgs,
        'username': request.user
    })

def download_chatlog(request):
    
    if request.method == "POST":
        try:
            #print(request.POST['chatlog'])
            #print(request.body.decode('utf-8'))
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            #chatlog = data
            #response = HttpResponse(data, content_type="application/json")
            #response['Content-Disposition'] = 'inline; filename=chatlog.json'
            #return response
            #return JsonResponse(data, safe=False)
            response_data = json.dumps(data)
            response = HttpResponse(response_data, content_type='application/json')

            # Set the content-disposition header to trigger a download prompt
            response['Content-Disposition'] = 'attachment; filename="data.json"'

            return response
        except Exception as e:
            print(e)
            #raise Http404
            return JsonResponse({'error': 'Invalid request method'}, status=400)

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Get the channel layer
channel_layer = get_channel_layer()

# Define a function to get active WebSocket connections within a group
@async_to_sync
async def get_active_connections(group_name):
    group_channels = await channel_layer.group_channels(group_name)
    #active_connections = []
    active_conn_count = 0

    for channel_name in group_channels:
        channel_info = await channel_layer.channel_layer.channel_layer.channel_layer.channel_layer.channel_layer.channel_layer.group_channel(channel_name)

        if 'websocket' in channel_info:
            if channel_info['websocket'].state == 'open':
                #active_connections.append(channel_name)
                active_conn_count+=1

    return active_conn_count



def list_chat_groups(request):
    if not request.user.is_authenticated:
        return redirect('/chat_room/get_username/')
    groups = []
    for g in ChatGroup.objects.all():
        g = g.__dict__
        g["active_conn_count"] = get_consumer_count(g['name'])
        print(g)
        groups.append(g)
    return render(request, 'chat/chat_groups.html', {'chat_groups': groups})
    #return render(request, 'chat/chat_groups.html', {'chat_groups': ChatGroup.objects.all()})


def add_chat_group(request):
    if not request.user.is_authenticated:
        return redirect('/chat_room/get_username/')
    
    print(request.POST)
    print(request.POST['group_name'])
    name = request.POST['group_name']
    #user = request.user
    
    try:
        group = ChatGroup.objects.get(name=name)
        return HttpResponse('Group Name Already Exists')
    except ChatGroup.DoesNotExist:
        ChatGroup.objects.create(name=name, creator=request.user)
        return  HttpResponseRedirect('/chat_room/')
    

def delete_chat_group(request, group_name):
    if not request.user.is_authenticated:
        return redirect('/chat_room/get_username/')
    group = get_object_or_404(ChatGroup, name=group_name)
    group.delete()
    return redirect('/chat_room/')
