import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

import apps.chat.routing

from .channelsmiddleware import TokenAuthMiddleware

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": TokenAuthMiddleware(
            URLRouter(apps.chat.routing.urlpatterns)
        )
    }
)
