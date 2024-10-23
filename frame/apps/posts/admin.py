from django.contrib import admin

from .models import (
    Comment,
    LikedComment,
    LikedPost,
    LikedReply,
    Post,
    Reply,
    Tag,
)

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(LikedPost)
admin.site.register(LikedComment)
admin.site.register(LikedReply)
