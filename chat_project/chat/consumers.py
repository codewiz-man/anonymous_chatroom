# chat/consumers.py

# refer
# https://channels.readthedocs.io/en/latest/tutorial/part_1.html

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #print(self.channel_name)
        self.group_name = self.scope['url_route']['kwargs']['room_name']

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
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
