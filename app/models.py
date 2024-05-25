from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid
from django.conf import settings
from django.utils.text import Truncator

class UserAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        """
        Creates normal user
        """
        if not email:
            raise ValueError('Email field is required')
        
        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(first_name=first_name, last_name=last_name, email=email)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, password=None):
        """
        Creates superuser
        """
        user = self.create_user(first_name, last_name, email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)    
    last_name = models.CharField(max_length=100)    
    email = models.EmailField(max_length=200, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
class Conversation(models.Model):
    """
    Model representing a Conversation between Users.
    - Many to Many Relationship with User Model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at', )

    def __str__(self):
        return f"Conversation between {' & '.join(self.members.all().values_list('email', flat=True))}"

class ConversationMessage(models.Model):
    """
    Model representing a message within a conversation.
    - Foreign key relationship with Conversation model.
    - Foreign key relationship with User model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )
    
    def __str__(self):
        return f"{self.sender} --- to --- {self.conversation.members.exclude(email=self.sender).first()} ------ {Truncator(self.text).words(5)}"    