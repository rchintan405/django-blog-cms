from django.contrib import admin
from apps.blog.models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "views", "read_time", "published_at", "created_at")
    list_filter = ("status", "tags")
    search_fields = ("title", "content", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    filter_horizontal = ("tags",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
