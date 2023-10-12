# chat/consumers.py

# refer
# https://channels.readthedocs.io/en/latest/tutorial/part_1.html

from django.utils import timezone
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #print(self.channel_name)

        # Update the user's last activity when they connect
        if self.scope["user"].is_authenticated:
            self.scope["user"].last_activity = timezone.now()
        #    self.scope["user"].save()
            await sync_to_async(self.scope["user"].save)()
            
        self.group_name = self.scope['url_route']['kwargs']['room_name']

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Update the user's last activity when they send a message
        if self.scope["user"].is_authenticated:
            self.scope["user"].last_activity = timezone.now()
        #    self.scope["user"].save()
            await sync_to_async(self.scope["user"].save)()

        print(text_data)
        text_data_json = json.loads(text_data)
        text_data_json['type'] = 'send_message'
        #message = text_data_json["message"]

        #self.send(text_data=json.dumps({"message": message}))
        #self.send(text_data=text_data)
        await self.channel_layer.group_send(self.group_name, text_data_json)

    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))
