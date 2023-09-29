import json
from channels.generic.websocket import AsyncWebsocketConsumer

from chat_project.chat.models import Message, ChatGroup

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = "USER"

        await self.save_message(message, user)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': user,  # For simplicity, assume all messages are from the same user.
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    async def save_message(self, message, user):
        Message.objects.create(
            content=message,
            user=user,
            group=ChatGroup.objects.get(name=self.group_name)
        )
