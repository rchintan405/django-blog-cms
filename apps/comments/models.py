from django.db import models
from django.contrib.auth import get_user_model
from apps.blog.models import Post

User = get_user_model()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    body = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post", "is_approved"]),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on '{self.post.title}'"

    @property
    def is_reply(self):
        return self.parent is not None
