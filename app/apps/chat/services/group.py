import json

from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from apps.chat.api.serializers import (
    CreateGroupSerializer,
    GroupReadSerializer,
)
from apps.chat.models.chat import Chat, Group
from apps.chat.selectors import get_group_by_name


class GroupService:
    @transaction.atomic
    def create_group(self, group_name: str, chat: Chat) -> Group:
        group = Group(name=group_name, chat=chat)
        group.save()
        return group

    def join_group(self, group_name, user):
        group = get_group_by_name(group_name)

        if group:
            if user not in group.users:
                group.users.add(user)

        return True

    def leave_group(self, group_name, user):
        group = get_group_by_name(group_name)

        if group:
            if user in group.users:
                group.users.remove(user)

        return True

    @transaction.atomic
    def delete_group(self, group: Group):
        """
        Takes group object and delete it
        """
        group.delete()
        return True

    @staticmethod
    def get_group_or_raise_exception(group_name):
        group = get_group_by_name(group_name)
        if group is None:
            raise APIException("This group doesn't exists")
        return group


class CreateGroupService:
    def create(self, request, serializer):
        seralizer = serializer(data=json.loads(request.body))
        seralizer.is_valid(raise_exception=True)

        group_name = seralizer.validated_data["name"]
        chat = Chat.objects.get_or_create_group_thread(group_name)
        group = GroupService().create_group(group_name, chat)

        return Response(
            GroupReadSerializer(instance=group).data,
            status=status.HTTP_201_CREATED,
        )


class DeleteGroupService:
    def delete(self, group_name):
        group = GroupService().get_group_or_raise_exception(group_name)
        GroupService().delete_group(group)
        return Response(status=status.HTTP_200_OK)


class JoinGroupService:
    def join(self, request, group_name):
        user = request.user
        group = GroupService().get_group_or_raise_exception(group_name)

        if not user in group.users.all():
            group.users.add(user)
            return Response("Succussfully joined.")

        raise APIException("You are already joined this group")


class LeaveGroupService:
    def leave(self, request, group_name):
        user = request.user
        group = GroupService().get_group_or_raise_exception(group_name)

        if user in group.users.all():
            group.users.remove(user)
            return Response("Succussfully removed.")

        raise APIException("You are not in this group")
