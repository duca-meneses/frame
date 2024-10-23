from django.contrib import admin

from .models import Comment, LikedPost, Post, Reply, Tag

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(LikedPost)
