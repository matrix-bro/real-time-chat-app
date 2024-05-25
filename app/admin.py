from django.contrib import admin
from app.models import Conversation, ConversationMessage
from django.contrib.auth import get_user_model
User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')

admin.site.register(Conversation)    
admin.site.register(ConversationMessage)    