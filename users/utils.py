import uuid
import random
from django.conf import settings

from djmail import template_mail
import premailer

import logging


# Hide CSS warnings messages if debug mode is disabled
if not getattr(settings, "DEBUG", False):
    premailer.premailer.cssutils.log.setLevel(logging.CRITICAL)


class InlineCSSTemplateMail(template_mail.TemplateMail):
    def _render_message_body_as_html(self, context):
        html = super()._render_message_body_as_html(context)

        # Transform CSS into line style attributes
        return premailer.transform(html)


class MagicMailBuilder(template_mail.MagicMailBuilder):
    pass


mail_builder = MagicMailBuilder(template_mail_cls=InlineCSSTemplateMail)


def get_default_uuid():
    return uuid.uuid4().hex


DEFAULT_PREDEFINED_COLORS = (
    "#fce94f",
    "#edd400",
    "#c4a000",
    "#8ae234",
    "#73d216",
    "#4e9a06",
    "#d3d7cf",
    "#fcaf3e",
    "#f57900",
    "#ce5c00",
    "#729fcf",
    "#3465a4",
    "#204a87",
    "#888a85",
    "#ad7fa8",
    "#75507b",
    "#5c3566",
    "#ef2929",
    "#cc0000",
    "#a40000",
)

PREDEFINED_COLORS = getattr(settings, "PREDEFINED_COLORS", DEFAULT_PREDEFINED_COLORS)


def generate_random_hex_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def generate_random_predefined_hex_color():
    return random.choice(PREDEFINED_COLORS)


from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
