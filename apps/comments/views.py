from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from apps.blog.models import Post
from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer, CommentCreateSerializer


def get_post_or_404(slug):
    try:
        return Post.objects.get(slug=slug, status="published")
    except Post.DoesNotExist:
        raise NotFound("Post not found.")


class CommentListCreateView(generics.ListCreateAPIView):
    """List approved comments for a post, or create a new comment."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = get_post_or_404(self.kwargs["slug"])
        return (
            Comment.objects.filter(post=post, is_approved=True, parent=None)
            .select_related("author")
            .prefetch_related("replies__author")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        post = get_post_or_404(self.kwargs["slug"])
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific comment."""
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer
        return CommentCreateSerializer
