from rest_framework.views import APIView
from rest_framework import serializers, status, permissions, generics
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from app.services.user_services import create_user_account
from django.shortcuts import get_object_or_404
from app.models import Conversation, ConversationMessage
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterView(APIView):
    """
    API view to creates a new user account.
    """
    class InputSerializer(serializers.ModelSerializer):
        """
        Serializer for user account registration.
        """
        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password')

        password = serializers.CharField(write_only=True)
        confirm_password = serializers.CharField(write_only=True)

        def validate(self, attrs):
            if attrs['password'] != attrs['confirm_password']:
                raise serializers.ValidationError({
                    'password': "Password fields didn't match."
                })
            
            attrs.pop('confirm_password')   # Removing confirm_password from validated_data

            return attrs
        
    def post(self, request):
        """
        POST: Creates a new user account.
        """
        serializer = self.InputSerializer(data=request.data)
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

        response = self.InputSerializer(user)

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
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'first_name', 'last_name']   

    serializer_class = OutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)
    
class UserChatView(APIView):
    """
    API view to display conversation (chat) between users
    """
    class OutputSerializer(serializers.ModelSerializer):
        """
        Serializer for outputting conversation with all messages and their senders
        """
        class MessageSerializer(serializers.ModelSerializer):
            class UserSerializer(serializers.ModelSerializer):
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

    def get(self, request, pk):
        """
        GET: Displays a conversation with messages between users (authenticated user and recipient user)
        - pk: recipientUserId
        """
        recipientUser = get_object_or_404(User, pk=pk)

        # Check if recipient and request.user is same
        if recipientUser == request.user:
            return Response({
                'success': False,
                'msg': 'Invalid recipient.',
                'status': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get Conversation if it exists or Create conversation if it doesn't exist
        conversation = Conversation.objects.filter(members=request.user).filter(members=recipientUser).first()
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.members.add(request.user)
            conversation.members.add(recipientUser)
            conversation.save()
        
        response = self.OutputSerializer(conversation)
        return Response({
            'success': True,
            'success': 'User conversation with messages retrieved successfully.',
            'data': response.data,
            'status': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)