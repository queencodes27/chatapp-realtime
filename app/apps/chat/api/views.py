from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.chat.services.chat import ChatFriendService, ChatGroupService
from apps.chat.services.friends import (
    AddFriendService,
    ListFriendsService,
    RemoveFriendService,
)
from apps.chat.services.group import (
    CreateGroupService,
    DeleteGroupService,
    JoinGroupService,
    LeaveGroupService,
)

from .serializers import CreateGroupSerializer


class CreateGroupAPIView(APIView):
    @swagger_auto_schema(
        request_body=CreateGroupSerializer,
        tags=["group"],
    )
    def post(self, request, *args, **kwargs):
        response = CreateGroupService().create(request, CreateGroupSerializer)
        return response


class DeleteGroupAPIView(APIView):
    @swagger_auto_schema(tags=["group"])
    def post(self, request, *args, **kwargs):
        group_name = self.kwargs["group_name"]
        response = DeleteGroupService().delete(group_name)
        return response


class JoinGroupAPIView(APIView):
    @swagger_auto_schema(tags=["group"])
    def post(self, request, *args, **kwargs):
        group_name = self.kwargs["group_name"]
        response = JoinGroupService().join(request, group_name)
        return response


class LeaveGroupAPIView(APIView):
    @swagger_auto_schema(tags=["group"])
    def post(self, request, *args, **kwargs):
        group_name = self.kwargs["group_name"]
        response = LeaveGroupService().leave(request, group_name)
        return response


class ListFriendsAPIView(APIView):
    @swagger_auto_schema(tags=["friends"])
    def get(self, request, *args, **kwargs):
        response = ListFriendsService().list(request)
        return response


class AddFriendAPIView(APIView):
    @swagger_auto_schema(tags=["friends"])
    def post(self, request, *args, **kwargs):
        response = AddFriendService().add(request, self.kwargs["user_name"])
        return response


class RemoveFriendAPIView(APIView):
    @swagger_auto_schema(tags=["friends"])
    def post(self, request, *args, **kwargs):
        response = RemoveFriendService().remove(
            request, self.kwargs["user_name"]
        )
        return response


class ChatFriendAPIView(APIView):
    @swagger_auto_schema(tags=["chat"])
    def get(self, request, *args, **kwargs):
        """
        Return the websocket url to start your communication with your friend
        """
        response = ChatFriendService().chat(request, self.kwargs["user_name"])
        return response


class ChatGroupAPIView(APIView):
    @swagger_auto_schema(tags=["chat"])
    def get(self, request, *args, **kwargs):
        """
        Return the websocket url to start your communication with your group
        """
        response = ChatGroupService().chat(request, self.kwargs["group_name"])
        return response
