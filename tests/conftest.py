import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        username="Mykola", email="mykola@gmail.com", password="Qe12wdlas12214Ssdwq2"
    )


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def client_jwt(user, db):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def token(user, db):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
