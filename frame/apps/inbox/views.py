from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Conversation


@login_required
def inbox_view(request, conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)
    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)
    else:
        conversation = None
    context = {
        'conversation': conversation,
        'my_conversations': my_conversations
    }
    return render(request, 'inbox/inbox.html', context)
