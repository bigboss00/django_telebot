from django.contrib import admin

from post.models import Comment, Like, Post, Rating

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rating)
