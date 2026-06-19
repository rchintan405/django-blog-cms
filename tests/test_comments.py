import pytest


@pytest.mark.django_db
def test_list_comments(api_client, published_post, comment):
    res = api_client.get(f"/api/v1/posts/{published_post.slug}/comments/")
    assert res.status_code == 200
    assert len(res.data) >= 1


@pytest.mark.django_db
def test_create_comment(auth_client, published_post):
    res = auth_client.post(f"/api/v1/posts/{published_post.slug}/comments/", {
        "body": "Great post!"
    })
    assert res.status_code == 201


@pytest.mark.django_db
def test_create_reply(auth_client, published_post, comment):
    res = auth_client.post(f"/api/v1/posts/{published_post.slug}/comments/", {
        "body": "I agree!",
        "parent": comment.id,
    })
    assert res.status_code == 201


@pytest.mark.django_db
def test_unauthenticated_cannot_comment(api_client, published_post):
    res = api_client.post(f"/api/v1/posts/{published_post.slug}/comments/", {
        "body": "Spam"
    })
    assert res.status_code == 401


@pytest.mark.django_db
def test_delete_own_comment(auth_client, published_post, comment):
    res = auth_client.delete(f"/api/v1/comments/{comment.id}/")
    assert res.status_code == 204


@pytest.mark.django_db
def test_cannot_delete_others_comment(other_auth_client, comment):
    res = other_auth_client.delete(f"/api/v1/comments/{comment.id}/")
    assert res.status_code == 404
