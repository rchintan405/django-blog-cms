from django.contrib import admin
from apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "is_approved", "is_reply", "created_at")
    list_filter = ("is_approved",)
    search_fields = ("author__username", "body", "post__title")
    actions = ["approve_comments"]

    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
