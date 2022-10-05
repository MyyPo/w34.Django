from django.urls import path
from .apis import GetScenesAPI, Game

urlpatterns = [
    path("scenes/", GetScenesAPI.as_view(), name="get_all_scenes"),
    path("game/", Game.as_view(), name="game"),
]
