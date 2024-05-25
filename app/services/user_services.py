from django.contrib.auth import get_user_model
User = get_user_model()

def create_user_account(first_name, last_name, email, password):
    user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)
    return user