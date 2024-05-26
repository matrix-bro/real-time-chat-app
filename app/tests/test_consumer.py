from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import path, reverse

from app.consumers import ChatConsumer
from app.models import Conversation

User = get_user_model()


class ChatConsumerTests(TestCase):
    def setUp(self):
        # User 1 data
        self.first_user_data = {
            "first_name": "john",
            "last_name": "doe",
            "email": "john@gmail.com",
            "password": "password321",
            "confirm_password": "password321"
        }

        # User 2 data
        self.second_user_data = {
            "first_name": "ray",
            "last_name": "doe",
            "email": "ray@gmail.com",
            "password": "password321",
            "confirm_password": "password321"
        }

        # User 3 data
        self.third_user_data = {
            "first_name": "selena",
            "last_name": "doe",
            "email": "selena@gmail.com",
            "password": "password321",
            "confirm_password": "password321"
        }

        self.register_url = reverse('register')

        # Register User 1
        self.client.post(self.register_url, data=self.first_user_data)

        # Register User 2
        self.client.post(self.register_url, data=self.second_user_data)

        # Register User 3
        self.client.post(self.register_url, data=self.third_user_data)

        # Get User 1 and User 2 and Create conversation between them
        self.first_user = User.objects.get(email=self.first_user_data['email'])
        self.second_user = User.objects.get(
            email=self.second_user_data['email']
        )

        # Create a conversation
        self.conversation = Conversation.objects.create()
        self.conversation.members.add(self.first_user)
        self.conversation.members.add(self.second_user)
        self.conversation.save()

        # Get User 3 and Create conversation between User 2 and User 3
        # User 1 should not able to access this conversation
        self.third_user = User.objects.get(email=self.third_user_data['email'])
        self.conversation_two = Conversation.objects.create()
        self.conversation_two.members.add(self.second_user)
        self.conversation_two.members.add(self.third_user)
        self.conversation_two.save()

    async def test_access_to_other_users_conversation(self):
        """
        Test User 1 trying to access User 2 and User 3 conversation
        """
        application = URLRouter([
            path('ws/chat/<str:conversation_id>/', ChatConsumer.as_asgi()),
        ])

        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{self.conversation_two.id}/"
        )

        # Here, first_user is logged in
        communicator.scope['user'] = self.first_user   
        connected, _ = await communicator.connect()

        # Should not be able to connect
        assert not connected

    async def test_access_to_own_conversation(self):
        """
        Test User 1 trying to access his own conversation with User 2
        """
        application = URLRouter([
            path('ws/chat/<str:conversation_id>/', ChatConsumer.as_asgi()),
        ])

        communicator = WebsocketCommunicator(
            application, f"/ws/chat/{self.conversation.id}/"
        )

        # Here, first_user is logged in
        communicator.scope['user'] = self.first_user
        connected, _ = await communicator.connect()

        # Should not be able to connect
        assert connected

    async def test_send_message_to_self(self):
        """
        Test User 1 trying to message to self by changing -
        recipientId to their own
        """
        application = URLRouter([
            path('ws/chat/<str:conversation_id>/', ChatConsumer.as_asgi()),
        ])

        communicator = WebsocketCommunicator(
            application, f"/ws/chat/{self.conversation.id}/"
        )
        communicator.scope['user'] = self.first_user 
        connected, _ = await communicator.connect()

        assert connected

        # Test sending text to themself
        await communicator.send_json_to({
            "message": "Hi Test 1",
            "recipientId": str(self.first_user.id)  # Own id as recipientID
        })

        response = await communicator.receive_from()
        assert response == "Invalid recipient."

    async def test_send_message_to_recipient(self):
        """
        Test User 1 sending message to User 2
        """
        application = URLRouter([
            path('ws/chat/<str:conversation_id>/', ChatConsumer.as_asgi()),
        ])

        communicator = WebsocketCommunicator(
            application, f"/ws/chat/{self.conversation.id}/"
        )
        communicator.scope['user'] = self.first_user                                             
        connected, _ = await communicator.connect()

        assert connected

        # Test sending text from sender user to recipient user
        await communicator.send_json_to({
            "message": "Hi Test 1",
            "recipientId": str(self.second_user.id)
        })

        response = await communicator.receive_json_from()

        assert response['message'] == "Hi Test 1"

        await communicator.disconnect()
