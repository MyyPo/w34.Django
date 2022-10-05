from email.policy import default
import uuid
from django.db import models

from django.utils import timezone

# from django.contrib.postgres.fields import ArrayField, HStoreField
# from django.contrib.postgres.fields.jsonb import JSONField

from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    id = models.IntegerField(
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("location id"),
    )
    name = models.CharField(max_length=32, verbose_name=_("location name"))

    def __str__(self):
        return self.name


class Scene(models.Model):
    slug = models.SlugField(
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("scene slug"),
    )

    options = models.JSONField()

    npc = models.ForeignKey(
        "game.NPC",
        verbose_name=_("NPC"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    alive = models.BooleanField(_("mob or npc alive"), default=True)
    location = models.ForeignKey(
        "game.Location",
        verbose_name=_("scene location"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Scene " + self.slug


class NPC(models.Model):
    name = models.CharField(_("npc name"), max_length=50)
    health = models.IntegerField(_("mob max health"), null=False, blank=False)
    attack = models.IntegerField(_("mob attack"), null=False, blank=False)


class Item(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(_("item name"), max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    slug = models.SlugField(
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("tag slug"),
    )

    def __str__(self):
        return "Tag " + self.slug


class GameSave(models.Model):
    name = models.CharField(
        help_text=_("save_name"), max_length=32, null=False, blank=False
    )
    user = models.ForeignKey(
        "users.User",
        help_text=_("user"),
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(_("date created"), default=timezone.now)
    current_health = models.IntegerField(
        verbose_name=_("current health"), blank=False, null=False
    )
    max_health = models.IntegerField(
        verbose_name=_("maximum health"), blank=False, null=False, default=25
    )
    attack = models.IntegerField(
        verbose_name=_("attack"), blank=False, null=False, default=10
    )
    defense = models.IntegerField(
        verbose_name=_("defense"), blank=False, null=False, default=4
    )
    scene = models.ForeignKey(
        Scene,
        verbose_name=_("character scene"),
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        default=1,
    )
    open_options = models.JSONField(blank=True, null=True)
    inventory = models.ManyToManyField(
        "game.Item",
        through="game.InventoryItem",
        related_name="inventory_items",
        verbose_name=_("character inventory"),
        blank=True,
        symmetrical=False,
    )
    tags = models.ManyToManyField(
        "game.Tag",
        related_name="tags",
        verbose_name=_("save tags"),
        blank=True,
        symmetrical=False,
    )

    class Meta:
        verbose_name = "game save"
        verbose_name_plural = "game saves"
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="unique_save_name")
        ]

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    item = models.ForeignKey(
        Item, related_name="inventory_item", on_delete=models.CASCADE
    )
    game_save = models.ForeignKey(
        GameSave, related_name="inventory_item", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "inventory item"
        verbose_name_plural = "inventory items"

    def __str__(self):
        return self.item.name
