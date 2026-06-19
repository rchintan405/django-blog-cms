import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.blog.models import Post, Tag
from apps.comments.models import Comment

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="author@example.com",
        username="author",
        password="testpass123",
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        email="other@example.com",
        username="other",
        password="testpass123",
    )


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def other_auth_client(api_client, other_user):
    refresh = RefreshToken.for_user(other_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def tag(db):
    return Tag.objects.create(name="Django", slug="django")


@pytest.fixture
def published_post(db, user, tag):
    post = Post.objects.create(
        title="Test Post",
        slug="test-post",
        content="This is test content for the blog post.",
        status="published",
        author=user,
    )
    post.tags.add(tag)
    return post


@pytest.fixture
def draft_post(db, user):
    return Post.objects.create(
        title="Draft Post",
        slug="draft-post",
        content="Draft content here.",
        status="draft",
        author=user,
    )


@pytest.fixture
def comment(db, published_post, user):
    return Comment.objects.create(
        post=published_post,
        author=user,
        body="This is a test comment.",
    )
