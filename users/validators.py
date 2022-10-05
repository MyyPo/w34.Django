# import bleach
# from django.core import validators as core_validators
# import re
# from django.utils.translation import gettext_lazy as _
# from rest_framework import serializers

# from .models import User, Save


# def restrict_saves_number(data):
#     if Save.objects.filter(user=data.user).count() >= 3:
#         raise serializers.ValidationError(
#             {"detail": "You can't create more than 3 save files simultaneously"}
#         )
#     return data


# class UserValidator(validators.ModelValidator):

#     class Meta:
#         model = User
#         fields = ("username", "color", "lang",
#                   "theme", "timezone", "is_active")

#     def validate_username(self, attrs, source):
#         value = attrs[source]
#         validator = core_validators.RegexValidator(re.compile(r'^[\w.-]+$'), _("invalid username"),
#                                                    _("invalid"))

#         try:
#             validator(value)
#         except ValidationError:
#             raise ValidationError(_("Required. 255 characters or fewer. Letters, "
#                                     "numbers and /./-/_ characters'"))

#         if (self.object and
#                 self.object.username != value and
#                 User.objects.filter(username=value).exists()):
#             raise ValidationError(_("Invalid username. Try with a different one."))

#         return attrs

#     def validate_full_name(self, attrs, source):
#         value = attrs[source]
#         if value != bleach.clean(value):
#             raise ValidationError(_("Invalid full name"))

#         if re.search(r"http[s]?:", value):
#             raise ValidationError(_("Invalid full name"))

#         return attrs
