from django.contrib import admin
from .models import Video, Comment

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploader', 'views_count', 'likes_count', 'created_at']
    list_filter = ['uploader', 'created_at']
    search_fields = ['title', 'description']
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'text', 'created_at']
    list_filter = ['created_at']