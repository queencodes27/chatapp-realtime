from channels.routing import ProtocolTypeRouter, URLRouter

import apps.chat.routing

from .channelsmiddleware import TokenAuthMiddleware

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": TokenAuthMiddleware(
            URLRouter(apps.chat.routing.websocket_urlpatterns)
        )
    }
)
