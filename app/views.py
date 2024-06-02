from rest_framework.views import APIView
from rest_framework import serializers, status, permissions, generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from app.models import Conversation, ConversationMessage
from app.services.user_services import create_user_account, get_user
from app.services.chat_services import get_or_create_conversation
User = get_user_model()


class RegisterView(APIView):
    """
    API view to creates a new user account.
    """
    class UserInputSerializer(serializers.ModelSerializer):
        """
        Serializer for user account registration.
        """
        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'email', 'password',
                      'confirm_password')

        password = serializers.CharField(write_only=True)
        confirm_password = serializers.CharField(write_only=True)

        def validate(self, attrs):
            if attrs['password'] != attrs['confirm_password']:
                raise serializers.ValidationError({
                    'password': "Password fields didn't match."
                })

            # Removing confirm_password from validated_data
            attrs.pop('confirm_password')

            return attrs
    
    @extend_schema(
        request=UserInputSerializer,
        responses={201: UserInputSerializer},
    )
    def post(self, request):
        """
        Creates a new user account.
        """
        serializer = self.UserInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']

        # Validating password
        try:
            validate_password(password, request.user)
        except ValidationError as e:
            return Response({
                'password': e.messages
            }, status=status.HTTP_400_BAD_REQUEST)

        user = create_user_account(**serializer.validated_data)

        response = self.UserInputSerializer(user)

        return Response({
            'success': True,
            'msg': 'User account created successfully.',
            'data': response.data,
            'status': status.HTTP_201_CREATED,
        }, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    """
    Displays list of users, excluding the authenticated user.
    """
    class UserOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'first_name', 'last_name']

    serializer_class = UserOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


class UserChatView(APIView):
    """
    API view to display conversation (chat) between users
    """
    class ChatOutputSerializer(serializers.ModelSerializer):
        """
        Serializer for representing a conversation -
        with its messages and sender.
        """
        class MessageSerializer(serializers.ModelSerializer):
            """
            Nested Serializer for representing conversation messages.
            """
            class UserSerializer(serializers.ModelSerializer):
                """
                Nested Serializer for representing user
                """
                class Meta:
                    model = User
                    fields = ['id', 'first_name', 'last_name']

            sender = UserSerializer()

            class Meta:
                model = ConversationMessage
                fields = ['text', 'sender', 'created_at']

        messages = MessageSerializer(many=True)

        class Meta:
            model = Conversation
            fields = ['id', 'messages']

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={200: ChatOutputSerializer},
    )
    def get(self, request, pk):
        """
        Displays a conversation with messages between users-
        (authenticated user and recipient user)
        """
        recipient_user = get_user(pk)

        # Check if recipient and request.user is same
        if recipient_user == request.user:
            return Response({
                'success': False,
                'msg': 'Invalid recipient.',
                'status': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get Conversation if it exists or
        # Create conversation if it doesn't exist
        conversation = get_or_create_conversation(request.user, recipient_user)

        response = self.ChatOutputSerializer(conversation)
        return Response({
            'success': True,
            'msg': 'User conversation with messages retrieved successfully.',
            'data': response.data,
            'status': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
