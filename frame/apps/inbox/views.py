from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ..users.models import Profile
from .forms import InboxNewMessageForm
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


def search_users(request):
    letters = request.GET.get('search_user')
    if request.htmx:
        if len(letters) > 0:
            profiles = Profile.objects.filter(
                realname__icontains=letters).exclude(realname=request.user.profile.realname)
            users_id = profiles.values_list('user', flat=True)
            users = User.objects.filter(
                Q(username__icontains=letters) | Q(id__in=users_id)
            ).exclude(username=request.user.username)
            template = 'inbox/list_search_user.html'
            return render(request, template, {'users': users})
        else:
            return HttpResponse('')
    else:
        raise Http404()


@login_required
def new_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    new_message_form = InboxNewMessageForm()

    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user

            my_conversations = request.user.conversations.all()
            for c in my_conversations:
                if recipient in c.participants.all():
                    message.conversation = c
                    message.save()
                    c.last_message_created = timezone.now()
                    c.save()
                    return redirect('inbox', c.id)

            new_conversation = Conversation.objects.create()
            new_conversation.participants.add(request.user, recipient)
            new_conversation.save()
            message.conversation = new_conversation
            message.save()
            return redirect('inbox', new_conversation.id)

    context = {
        'recipient': recipient,
        'new_message_form': new_message_form
    }
    return render(request, 'inbox/form_new_message.html', context)


@login_required
def new_reply(request, conversation_id):
    new_message_form = InboxNewMessageForm()
    my_conversations = request.user.conversations.all()
    conversation = get_object_or_404(my_conversations, id=conversation_id)

    if request.method == 'POST':
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            conversation.last_message_created = timezone.now()
            conversation.save()
            return redirect('inbox', conversation.id)

    context = {
        'new_message_form': new_message_form,
        'conversation': conversation
    }

    return render(request, 'inbox/form_new_reply.html', context)
