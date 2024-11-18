from django.urls import path

from .views import (
    inbox_view,
    new_message,
    new_reply,
    notify_inbox,
    notify_message,
    search_users,
)

urlpatterns = [
    path('', inbox_view, name='inbox'),
    path('c/<conversation_id>/', inbox_view, name='inbox'),
    path('search-users/', search_users, name='inbox-search-users'),
    path('new-message/<recipient_id>/', new_message, name='inbox-new-message'),
    path('new-reply/<conversation_id>/', new_reply, name='inbox-new-reply'),
    path('notify/<conversation_id>/', notify_message, name='notify-message'),
    path('notify-inbox/', notify_inbox, name='notify-inbox'),
]
