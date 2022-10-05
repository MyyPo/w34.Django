import dataclasses
from datetime import date, datetime
from django.utils import timezone
from typing import TYPE_CHECKING
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from users.services import SceneDataClass, UserDataClass
from game import models
from django.db.models import F

from django.db.models import Count
from game.utils import get_from_dict, get_available_options


if TYPE_CHECKING:
    from game.models import GameSave


@dataclasses.dataclass
class GameSaveDataClass:
    name: str
    scene: SceneDataClass
    current_health: int = None
    max_health: int = None
    attack: int = None
    defense: int = None
    scene: SceneDataClass = None
    inventory: str = None
    user: UserDataClass = None
    created_at: datetime = None

    @classmethod
    def from_instance(cls, save: "GameSave") -> "GameSaveDataClass":
        return cls(
            name=save.name,
            user=save.user,
            created_at=save.created_at,
            max_health=save.max_health,
            current_health=save.current_health,
            attack=save.attack,
            defense=save.defense,
            scene=save.scene,
            inventory=save.inventory,
        )


def play(user, choice):
    instance = models.GameSave.objects.filter(user=user, name=choice["name"])
    save_id = instance[0].id

    # all_prompts = []
    # for option in instance[0].scene.options:
    #     path = [option, "PROMPT"]
    #     all_prompts.append(get_from_dict(instance[0].scene.options, path))
    # models.GameSave.objects.update(
    #     user=user, name=choice["name"], open_options=available_options
    # )

    # instance.update(open_options=get_available_options(instance[0]))
    # print(instance[0].open_options)

    player_choice = instance[0].open_options[choice["choice"]]

    print(player_choice)
    print(instance[0].scene.options)

    if "ADD" in player_choice:
        inventory = models.InventoryItem.objects.filter(game_save=save_id)
        for item in player_choice["ADD"]:
            if inventory.filter(item=item).exists():
                existing_item = models.InventoryItem.objects.filter(
                    game_save_id=save_id, item=item
                )
                existing_item.update(
                    quantity=F("quantity") + player_choice["ADD"][item],
                )
            else:
                models.InventoryItem.objects.create(
                    game_save_id=save_id,
                    item=models.Item.objects.get(slug=item),
                    quantity=player_choice["ADD"][item],
                )
    if "NEXT" in player_choice:
        instance.update(
            scene=player_choice["NEXT"],
        )
        instance.update(open_options=get_available_options(instance[0]))

    return instance


def get_save(user, data):
    instance = models.GameSave.objects.filter(user=user, name=data["name"])

    return instance
