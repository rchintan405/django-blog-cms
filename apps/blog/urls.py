from django.urls import path
from apps.blog.views import (
    TagListCreateView,
    TagDetailView,
    PostListView,
    MyPostListView,
    PostCreateView,
    PostDetailView,
)

urlpatterns = [
    # Tags
    path("tags/", TagListCreateView.as_view(), name="tag-list"),
    path("tags/<slug:slug>/", TagDetailView.as_view(), name="tag-detail"),

    # Posts
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/me/", MyPostListView.as_view(), name="my-posts"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
]
