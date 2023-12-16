from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")

        if not token:
            scope["user"] = AnonymousUser()
            return await self.inner(scope, receive, send)

        try:
            access_token = AccessToken(token[0])
        except TokenError:
            scope["user"] = AnonymousUser()
            return await self.inner(scope, receive, send)
        user = await get_user(access_token["user_id"])

        if isinstance(user, AnonymousUser):
            scope["user"] = AnonymousUser()
            return await self.inner(scope, receive, send)

        if not user.is_active:
            scope["user"] = AnonymousUser()
            return await self.inner(scope, receive, send)

        scope["user"] = user
        return await self.inner(scope, receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(
    AuthMiddlewareStack(inner)
)
