from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    excerpt = models.TextField(max_length=500, blank=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="posts/covers/", blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    views = models.PositiveIntegerField(default=0)
    read_time = models.PositiveSmallIntegerField(default=1, help_text="Estimated read time in minutes")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-published_at"]),
            models.Index(fields=["author", "status"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Auto-calculate read time (~200 words/min)
        word_count = len(self.content.split())
        self.read_time = max(1, round(word_count / 200))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comments.filter(is_approved=True).count()
