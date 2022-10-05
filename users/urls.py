from django.urls import path
from .apis import RegisterAPI, VerifyEmailAPI, GetUserSelfAPI, StartNewGame

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register_user"),
    path("verify_email/", VerifyEmailAPI.as_view(), name="verify_email"),
    path("user_details/", GetUserSelfAPI.as_view(), name="get_user_self"),
    path("new_game/", StartNewGame.as_view(), name="new_game"),
]
