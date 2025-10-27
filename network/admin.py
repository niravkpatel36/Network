from django.contrib import admin
from .models import User, Post, Follow, Like

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "short", "timestamp")
    search_fields = ("content", "user__username")
    list_filter = ("timestamp", "user")

    def short(self, obj):
        return obj.content[:60]
    short.short_description = "Content"

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "following", "created")
    search_fields = ("follower__username", "following__username")

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created")