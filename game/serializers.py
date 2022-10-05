from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField


from .models import Location, Scene, Item, InventoryItem
from users.services import SceneDataClass
from game.services import GameSaveDataClass


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Item
        fields = [
            "name",
        ]


class InventoryItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="item.name", read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            "quantity",
            "name",
        ]


class NPCSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    health = serializers.IntegerField()
    attack = serializers.IntegerField()
    # loot = ItemSerializer()


class LocationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Location
        fields = ["name"]


class SceneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    options = serializers.JSONField(read_only=True)
    # location = serializers.CharField(source="location.name")
    location = LocationSerializer(read_only=True)
    npc = NPCSerializer(allow_null=True)
    alive = serializers.BooleanField(allow_null=True)
    # loot = ItemSerializer(allow_null=True)

    class Meta:
        model = Scene
        fields = [
            "id",
            "name",
            "options",
            "location",
            "npc",
            "alive",
        ]


class GameSerializer(serializers.Serializer):
    # id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    # user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    current_health = serializers.IntegerField(read_only=True)
    max_health = serializers.IntegerField(read_only=True)
    attack = serializers.IntegerField(read_only=True)
    defense = serializers.IntegerField(read_only=True)
    scene = SceneSerializer(read_only=True)
    open_options = serializers.JSONField(read_only=True)
    inventory = InventoryItemSerializer(
        source="inventory_item", read_only=True, many=True
    )

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return GameSaveDataClass(**data)


# class SceneSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(read_only=True)
#     neighbour_scenes = RecursiveField(allow_null=True)
#     location = LocationSerializer(source="name")
#     npc = NPCSerializer(allow_null=True)
#     alive = serializers.BooleanField(allow_null=True)
#     # loot = ItemSerializer(allow_null=True)

#     def to_internal_value(self, data):
#         data = super().to_internal_value(data)

#         return SceneDataClass(**data)
