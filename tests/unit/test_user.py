import pytest


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        username="Mykola", email="mykola@gmail.com", password="Qe12wdlas12214Ssdwq2"
    )

    response = client.post("/api/register/", payload)

    data = response.data

    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.django_db
def test_login_user(user, client):
    response = client.post(
        "/api/token/", dict(username="Mykola", password="Qe12wdlas12214Ssdwq2")
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail(client):
    response = client.post(
        "/api/token/",
        dict(username="ThisUserDosntExist", password="Qe12wdlas12214Ssdwq2"),
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_jwt_refresh(client, token):
    payload = dict(refresh=token["refresh"])
    response = client.post("/api/token/refresh/", payload)
    assert response.status_code == 200


@pytest.mark.django_db
def test_jwt_refresh_bad_token(client):
    token = {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    }
    payload = dict(refresh=token["refresh"])
    response = client.post("/api/token/refresh/", payload)
    assert response.status_code == 401


@pytest.mark.django_db
def test_jwt_refresh_no_token(client):
    token = {"refresh": ""}
    payload = dict(refresh=token["refresh"])
    response = client.post("/api/token/refresh/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_user_details(client_jwt):
    response = client_jwt.get("/api/user_details/")
    assert response.status_code == 200
    assert "password" not in response.data


@pytest.mark.django_db
def test_create_fresh_save(client_jwt):
    payload = {"name": "Save 1"}
    response = client_jwt.post("/api/new_game/", payload)
    assert response.status_code == 200
