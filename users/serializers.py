from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from game.models import InventoryItem, Scene

# from .validators import restrict_saves_number
from .models import User
from game.models import GameSave
from .services import create_fresh_save, FreshSaveDataClass
from game.serializers import SceneSerializer


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user

    class Meta:
        model = User
        fields = (
            "uuid",
            "username",
            "email",
            "password",
        )


class InventoryItemSerializer(serializers.ModelSerializer):
    # name = serializers.CharField()
    # quantity = serializers.IntegerField()

    class Meta:
        model = InventoryItem
        fields = [
            "name",
            "quantity",
        ]


class SaveSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    # user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    current_health = serializers.IntegerField(read_only=True)
    max_health = serializers.IntegerField(read_only=True)
    attack = serializers.IntegerField(read_only=True)
    defense = serializers.IntegerField(read_only=True)
    scene = SceneSerializer(read_only=True)
    # inventory = ItemSerializer(read_only=True, many=True)
    inventory = InventoryItemSerializer(read_only=True, many=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return FreshSaveDataClass(**data)
