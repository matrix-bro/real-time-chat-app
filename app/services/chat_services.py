from app.models import Conversation

def get_or_create_conversation(authUser, recipientUser):
    """
    Get Conversation if it exists or Create conversation if it doesn't exist

    Params:
    - authUser: The authenticated user initiating or participating in the conversation.
    - recipientUser: The user with whom the authenticated user is engaging in conversation.

    Returns:
    - conversation: The conversation object either retrieved or created.
    """
    conversation = Conversation.objects.filter(members=authUser).filter(members=recipientUser).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.members.add(authUser)
        conversation.members.add(recipientUser)
        conversation.save()
    
    return conversation