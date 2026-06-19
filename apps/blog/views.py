from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from apps.blog.models import Post, Tag
from apps.blog.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer,
    TagSerializer,
)
from apps.blog.permissions import IsAuthorOrReadOnly
from apps.blog.filters import PostFilter


# ── Tag Views ──────────────────────────────────────────────────────────────────

class TagListCreateView(generics.ListCreateAPIView):
    """List all tags or create a new one."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a tag by slug."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"


# ── Post Views ─────────────────────────────────────────────────────────────────

class PostListView(generics.ListAPIView):
    """List published posts with filtering, search, and ordering."""
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ["title", "excerpt", "content", "author__username", "tags__name"]
    ordering_fields = ["published_at", "views", "created_at"]
    ordering = ["-published_at"]

    def get_queryset(self):
        return Post.objects.filter(status="published").select_related("author").prefetch_related("tags")


class MyPostListView(generics.ListAPIView):
    """List all posts (any status) for the authenticated author."""
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PostFilter
    ordering_fields = ["created_at", "published_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).select_related("author").prefetch_related("tags")


class PostCreateView(generics.CreateAPIView):
    """Create a new blog post."""
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a post by slug."""
    queryset = Post.objects.select_related("author").prefetch_related("tags")
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count on each retrieve
        Post.objects.filter(pk=instance.pk).update(views=instance.views + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
