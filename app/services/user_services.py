from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()


def create_user_account(first_name, last_name, email, password):
    """
    Create user account in database
    """
    user = User.objects.create_user(first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    password=password)
    return user


def get_user(pk):
    """
    Get user from the database
    """
    user = get_object_or_404(User, pk=pk)
    return user
