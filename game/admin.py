from django.contrib import admin
from django.forms import TextInput, Textarea, JSONField
from django.db import models


from .models import Location, Scene, NPC, Item, Tag, GameSave, InventoryItem


# class SceneModelAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "id",
#         "location",
#         "npc",
#     )
#     ordering = ("id",)
#     list_filter = ("location",)

#     def formfield_for_dbfield(self, db_field, **kwargs):
#         formfield = super(SceneModelAdmin, self).formfield_for_dbfield(
#             db_field, **kwargs
#         )
#         if db_field.name == "options":
#             formfield.widget = Textarea(attrs=formfield.widget.attrs)
#         return formfield

#     def get_form(self, request, obj=None, **kwargs):
#         form = super(SceneModelAdmin, self).get_form(request, obj, **kwargs)
#         form.base_fields["options"].widget.attrs["style"] = "width: 60em;"
#         form.base_fields["neighbour_scenes"].widget.attrs["style"] = "width: 60em;"
#         return form


# admin.site.register(Scene, SceneModelAdmin)
admin.site.register(GameSave)
admin.site.register(Location)
admin.site.register(Scene)
admin.site.register(NPC)
admin.site.register(Item)
admin.site.register(InventoryItem)
admin.site.register(Tag)
