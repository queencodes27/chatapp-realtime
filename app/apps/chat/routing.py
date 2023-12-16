from django.urls import re_path

from .consumers import GroupChatConsumer, UserChatConsumer

urlpatterns = [
    re_path(
        r"ws/group/(?P<group_name>\w+)/$",
        GroupChatConsumer.as_asgi(),
        name="ws_group",
    ),
    re_path(
        r"ws/user/(?P<username>\w+)/$",
        UserChatConsumer.as_asgi(),
        name="ws_personal",
    ),
]
