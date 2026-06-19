import pytest


@pytest.mark.django_db
def test_register_user(api_client):
    res = api_client.post("/api/v1/auth/register/", {
        "email": "new@example.com",
        "username": "newuser",
        "password": "newpass123",
        "password2": "newpass123",
    })
    assert res.status_code == 201
    assert "tokens" in res.data
    assert res.data["user"]["email"] == "new@example.com"


@pytest.mark.django_db
def test_register_password_mismatch(api_client):
    res = api_client.post("/api/v1/auth/register/", {
        "email": "new@example.com",
        "username": "newuser",
        "password": "pass123",
        "password2": "different",
    })
    assert res.status_code == 400


@pytest.mark.django_db
def test_login(api_client, user):
    res = api_client.post("/api/v1/auth/login/", {
        "email": "author@example.com",
        "password": "testpass123",
    })
    assert res.status_code == 200
    assert "access" in res.data


@pytest.mark.django_db
def test_login_wrong_credentials(api_client, user):
    res = api_client.post("/api/v1/auth/login/", {
        "email": "author@example.com",
        "password": "wrongpass",
    })
    assert res.status_code == 401


@pytest.mark.django_db
def test_get_me(auth_client):
    res = auth_client.get("/api/v1/auth/me/")
    assert res.status_code == 200
    assert res.data["email"] == "author@example.com"


@pytest.mark.django_db
def test_update_me(auth_client):
    res = auth_client.patch("/api/v1/auth/me/", {"bio": "I love Django!"})
    assert res.status_code == 200


@pytest.mark.django_db
def test_public_profile(api_client, user):
    res = api_client.get(f"/api/v1/auth/users/{user.username}/")
    assert res.status_code == 200
    assert res.data["username"] == user.username
