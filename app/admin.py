from django.contrib import admin
from django.contrib.auth import get_user_model
from app.models import Conversation, ConversationMessage
User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')


admin.site.register(Conversation)
admin.site.register(ConversationMessage)
