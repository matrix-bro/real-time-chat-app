from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope['user']

        # If user is not authenticated, close the connection
        if not self.user.is_authenticated:
            await self.close()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipientId = data['recipientId']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'recipientId': recipientId,

            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        recipientId = event['recipientId']

        await self.send(text_data=json.dumps({
            'message': message,
            'recipientId': recipientId,
        }))