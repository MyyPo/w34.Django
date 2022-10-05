import dataclasses
from datetime import date, datetime
from django.utils import timezone
from typing import TYPE_CHECKING
from unicodedata import name
from django.conf import settings
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from . import models
from game.models import Scene, GameSave

if TYPE_CHECKING:
    from .models import User


@dataclasses.dataclass
class UserDataClass:
    email: str
    username: str
    password: str = None
    uuid: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            username=user.username,
            email=user.email,
            uuid=user.uuid,
        )


@dataclasses.dataclass
class SceneDataClass:
    slug = str
    options = list
    npc = str
    alive = bool
    # loot =
    location = str

    @classmethod
    def from_instance(cls, scene: "Scene") -> "SceneDataClass":
        return cls(
            slug=scene.slug,
            options=scene.options,
            npc=scene.npc,
            alive=scene.alive,
            location=scene.location,
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    instance = models.User(username=user_dc.username, email=user_dc.email)
    if user_dc.password is not None:
        instance.set_password(user_dc.password)

    instance.save()

    return UserDataClass.from_instance(instance)


@dataclasses.dataclass
class FreshSaveDataClass:
    name: str
    # scene: SceneDataClass
    current_health: int = None
    max_health: int = None
    attack: int = None
    defense: int = None
    scene: SceneDataClass = None
    open_options: list = None
    inventory: str = None
    user: UserDataClass = None
    created_at: datetime = None

    @classmethod
    def from_instance(cls, save: "GameSave") -> "FreshSaveDataClass":
        return cls(
            slug=save.name,
            user=save.user,
            created_at=save.created_at,
            max_health=save.max_health,
            current_health=save.current_health,
            attack=save.attack,
            defense=save.defense,
            scene=save.scene.set(1),
            inventory=save.inventory,
        )


def create_fresh_save(user, save: "FreshSaveDataClass") -> "FreshSaveDataClass":
    current_user_saves = GameSave.objects.filter(user=user)
    if current_user_saves.count() >= 3:
        raise exceptions.ValidationError(
            {"detail": _("Can't create more than 3 saves")}
        )
    if current_user_saves.filter(name=save.name):
        raise exceptions.ValidationError(
            {"detail": _("You can't have several saves with the same name")}
        )

    instance = GameSave(
        name=save.name,
        user=user,
        created_at=timezone.now(),
        max_health=10,
        current_health=10,
        # open_options=[
        #     {"ADD": {"fork": 3}, "NEXT": 2, "PROMPT": "Always"},
        #     {
        #         "ADD": {"fork": 1, "spoon": 3},
        #         "TAG": "confirmed",
        #         "PROMPT": "Seen only with tag",
        #     },
        # ],
        open_options=models.Scene.objects.filter(slug=1)[0].options,
        attack=8,
        defense=8,
        # inventory=save.inventory,
    )
    instance.save()
    return instance
