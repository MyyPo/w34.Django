from asyncio import constants
from tabnanny import verbose
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

from django.core import validators
from django.utils.translation import gettext_lazy as _
import re

from game.models import Item, Scene

from .utils import get_default_uuid, generate_random_hex_color


class PermissionsMixin(models.Model):
    """
    A mixin class that adds the fields and methods necessary to support
    Django"s Permission model using the ModelBackend.
    """

    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        """
        Returns True if the user is superadmin and is active
        """
        return self.is_active and self.is_superuser


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.CharField(
        max_length=32,
        editable=False,
        null=False,
        blank=False,
        unique=True,
        default=get_default_uuid,
    )
    username = models.CharField(
        _("username"),
        max_length=255,
        unique=True,
        help_text=_(
            "Required. 30 characters or fewer. Letters, numbers and "
            "/./-/_ characters"
        ),
        validators=[
            validators.RegexValidator(
                re.compile(r"^[\w.-]+$"), _("Enter a valid username."), "invalid"
            )
        ],
    )
    email = models.EmailField(
        _("email address"), max_length=255, null=False, blank=False, unique=True
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    color = models.CharField(
        max_length=9,
        null=False,
        blank=True,
        default=generate_random_hex_color,
        verbose_name=_("color"),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    lang = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        default="",
        verbose_name=_("default language"),
    )
    theme = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="",
        verbose_name=_("default theme"),
    )
    timezone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        default="",
        verbose_name=_("default timezone"),
    )
    new_email = models.EmailField(_("new email address"), null=True, blank=True)
    verified_email = models.BooleanField(null=False, blank=False, default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    def __str__(self):
        return self.username


# class Save(models.Model):
#     name = models.CharField(
#         help_text=_("save_name"), max_length=32, null=False, blank=False
#     )
#     user = models.ForeignKey(
#         "users.User",
#         help_text=_("user"),
#         on_delete=models.CASCADE,
#         blank=False,
#         null=False,
#     )
#     created_at = models.DateTimeField(_("date created"), default=timezone.now)
#     current_health = models.IntegerField(
#         verbose_name=_("current health"), blank=False, null=False
#     )
#     max_health = models.IntegerField(
#         verbose_name=_("maximum health"), blank=False, null=False, default=25
#     )
#     attack = models.IntegerField(
#         verbose_name=_("attack"), blank=False, null=False, default=10
#     )
#     defense = models.IntegerField(
#         verbose_name=_("defense"), blank=False, null=False, default=4
#     )
#     scene = models.ForeignKey(
#         Scene,
#         verbose_name=_("character scene"),
#         on_delete=models.SET_NULL,
#         blank=False,
#         null=True,
#         default=1,
#     )
#     inventory = models.ManyToManyField(
#         Item,
#         through="InventoryItem",
#         verbose_name=_("character inventory"),
#         blank=True,
#         symmetrical=False,
#     )

#     class Meta:
#         verbose_name = "save"
#         verbose_name_plural = "saves"
#         constraints = [
#             models.UniqueConstraint(fields=["name", "user"], name="unique_save_name")
#         ]

#     def __str__(self):
#         return self.name


# class InventoryItem(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     save = models.ForeignKey(Save, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()

#     class Meta:
#         verbose_name = "inventory item"
#         verbose_name_plural = "inventory items"

#     def __str__(self):
#         return self.item + " | " + self.quantity
