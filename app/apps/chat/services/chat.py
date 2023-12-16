from django.conf import settings
from django.db import transaction
from django.urls import reverse, reverse_lazy
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from apps.account.selectors import (
    get_user_friends_obj,
    get_user_or_raise_exception,
)
from apps.chat.models import GroupMessage, UserMessage
from apps.chat.services.group import GroupService


class GroupMessageSerive:
    @staticmethod
    @transaction.atomic
    def create_msg(from_user, group, chat, content, *args, **kwargs):
        """
        Create group message
        """

        group_obj = GroupMessage(
            from_user=from_user,
            group=group,
            chat=chat,
            content=content,
        )
        group_obj.save()
        return group_obj


class UserMessageSerive:
    @staticmethod
    @transaction.atomic
    def create_msg(from_user, to_user, chat, content):
        """
        Create group message
        """

        group_obj = UserMessage(
            from_user=from_user,
            to_user=to_user,
            chat=chat,
            content=content,
        )
        group_obj.save()
        return group_obj


class ChatFriendService:
    def chat(self, request, username):
        user = get_user_or_raise_exception(username)

        if not self.is_friends(request.user, user):
            raise APIException(
                "Sorry can not connect you to this user,"
                " as you are not a friend of him"
            )

        token = AccessToken().for_user(request.user)
        data = {
            "url": "ws://"
            + request.META["HTTP_HOST"]
            + reverse_lazy(
                "ws_personal",
                args=[username],
                urlconf=settings.CHANNELS_URLCONF,
            )
            + f"?token={token}"
        }

        return Response(data)

    @staticmethod
    def is_friends(user, other_user):
        friends_obj = get_user_friends_obj(user)
        if other_user not in friends_obj.friends.all():
            return False
        return True


class ChatGroupService:
    def chat(self, request, group_name):
        group = GroupService().get_group_or_raise_exception(group_name)

        if not self.is_joined(group, request.user):
            raise APIException(
                "Sorry can not connect you to this group,"
                " as you are not a member of it"
            )

        token = AccessToken().for_user(request.user)
        data = {
            "url": "ws://"
            + request.META["HTTP_HOST"]
            + reverse_lazy(
                "ws_group",
                args=[group_name],
                urlconf=settings.CHANNELS_URLCONF,
            )
            + f"?token={token}"
        }

        return Response(data)

    @staticmethod
    def is_joined(group, user):
        """
        Check whether or not a user is joined to a group
        """
        if user not in group.users.all():
            return False
        return True
