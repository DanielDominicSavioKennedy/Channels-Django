import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_name,
            self.room_group_name,
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        print("disconnected")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        print("recieved")
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        print(data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'ty pe':'chat_message',
                'message':message,
                'username':username,
                'room':room,
            },
        )
        
    async def chat_message(self,event):
        print("sent")
        message = event['message']
        username = event['username']
        room = event['room']
        
        await self.send(text_data=json.dumps({
                'message':message,
                'username':username,
                'room':room,
        }))