from django.contrib import admin

from .models import Conversation, InboxMessage

admin.site.register(InboxMessage)
admin.site.register(Conversation)
