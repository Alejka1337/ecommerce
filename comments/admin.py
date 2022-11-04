from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    list_display = ("message", "name", "email", "product", "created_at")
    list_filter = ("created_at",)
    search_fields = ("message",)