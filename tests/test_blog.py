import pytest


@pytest.mark.django_db
def test_list_published_posts(api_client, published_post):
    res = api_client.get("/api/v1/posts/")
    assert res.status_code == 200
    assert res.data["count"] == 1


@pytest.mark.django_db
def test_draft_not_in_public_list(api_client, draft_post):
    res = api_client.get("/api/v1/posts/")
    assert res.status_code == 200
    assert res.data["count"] == 0


@pytest.mark.django_db
def test_create_post(auth_client):
    res = auth_client.post("/api/v1/posts/create/", {
        "title": "New Article",
        "content": "Great content here with lots of words " * 10,
        "status": "published",
    })
    assert res.status_code == 201
    assert res.data["title"] == "New Article"
    assert res.data["slug"] == "new-article"


@pytest.mark.django_db
def test_create_post_unauthenticated(api_client):
    res = api_client.post("/api/v1/posts/create/", {"title": "X", "content": "Y"})
    assert res.status_code == 401


@pytest.mark.django_db
def test_get_post_detail(api_client, published_post):
    res = api_client.get(f"/api/v1/posts/{published_post.slug}/")
    assert res.status_code == 200
    assert res.data["slug"] == published_post.slug


@pytest.mark.django_db
def test_view_count_increments(api_client, published_post):
    api_client.get(f"/api/v1/posts/{published_post.slug}/")
    api_client.get(f"/api/v1/posts/{published_post.slug}/")
    published_post.refresh_from_db()
    assert published_post.views == 2


@pytest.mark.django_db
def test_update_own_post(auth_client, published_post):
    res = auth_client.patch(f"/api/v1/posts/{published_post.slug}/", {"title": "Updated"})
    assert res.status_code == 200


@pytest.mark.django_db
def test_cannot_update_other_post(other_auth_client, published_post):
    res = other_auth_client.patch(f"/api/v1/posts/{published_post.slug}/", {"title": "Hacked"})
    assert res.status_code == 403


@pytest.mark.django_db
def test_delete_own_post(auth_client, published_post):
    res = auth_client.delete(f"/api/v1/posts/{published_post.slug}/")
    assert res.status_code == 204


@pytest.mark.django_db
def test_search_posts(api_client, published_post):
    res = api_client.get("/api/v1/posts/?search=Test")
    assert res.status_code == 200
    assert res.data["count"] >= 1


@pytest.mark.django_db
def test_filter_by_tag(api_client, published_post, tag):
    res = api_client.get(f"/api/v1/posts/?tag={tag.slug}")
    assert res.status_code == 200
    assert res.data["count"] >= 1


@pytest.mark.django_db
def test_my_posts_includes_drafts(auth_client, published_post, draft_post):
    res = auth_client.get("/api/v1/posts/me/")
    assert res.status_code == 200
    assert res.data["count"] == 2


@pytest.mark.django_db
def test_tag_list(api_client, tag):
    res = api_client.get("/api/v1/tags/")
    assert res.status_code == 200
    assert len(res.data) >= 1
