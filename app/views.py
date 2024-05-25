from rest_framework.views import APIView
from rest_framework import serializers, status, permissions, generics
from rest_framework.response import Response
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from app.services.user_services import create_user_account
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