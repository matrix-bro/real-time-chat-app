from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from app.models import Conversation, ConversationMessage
from django.contrib.auth import get_user_model
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope['user']

        # If user is not authenticated, close the connection
        if not self.user.is_authenticated:
            await self.close()

        # Validate and Check if authenticated user is trying to access other users conversation
        try:
            await self.validate_user_conversation(self.room_name)
        except:
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

        try:

            recipientUser = await self.get_user(recipientId)

            # Check if request.user and recipient user is same
            if recipientUser == self.user:
                await self.send(text_data="Invalid recipient.")
                await self.close()
                return

            # Get conversation
            conversation = await self.get_conversation(self.user, recipientUser)

            # Save message to DB
            await self.save_message(conversation, self.user, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'recipientId': recipientId,

                }
            )

        except Exception as e:
            await self.send(text_data=f"Error: {e}")

    
    async def chat_message(self, event):
        message = event['message']
        recipientId = event['recipientId']

        await self.send(text_data=json.dumps({
            'message': message,
            'recipientId': recipientId,
        }))
    
    @database_sync_to_async
    def validate_user_conversation(self, pk):
        """
        Get the Conversation of the authenticated user.
        - Throws error if tries to access other user's conversation.
        """
        return Conversation.objects.filter(id=pk).filter(members=self.user).get()
    
    @database_sync_to_async
    def get_user(self, pk):
        return User.objects.get(pk=pk)

    @database_sync_to_async
    def get_conversation(self, senderUser, recipientUser):
        """
        Get the Conversation of Sender and Recipient
        """
        return Conversation.objects.filter(members=senderUser).filter(members=recipientUser).get()

    @database_sync_to_async
    def save_message(self, conversation, senderUser, message):
        ConversationMessage.objects.create(conversation=conversation, text=message, sender=senderUser)
    