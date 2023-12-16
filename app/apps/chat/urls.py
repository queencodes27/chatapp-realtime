from django.urls import path

from apps.chat.api.views import (
    AddFriendAPIView,
    ChatFriendAPIView,
    ChatGroupAPIView,
    CreateGroupAPIView,
    DeleteGroupAPIView,
    JoinGroupAPIView,
    LeaveGroupAPIView,
    ListFriendsAPIView,
    RemoveFriendAPIView,
)

urlpatterns = [
    path("create-group", CreateGroupAPIView.as_view()),
    path("delete-group/<str:group_name>", DeleteGroupAPIView.as_view()),
    path("join-group/<str:group_name>", JoinGroupAPIView.as_view()),
    path("leave-group/<str:group_name>", LeaveGroupAPIView.as_view()),
    path("list-friends", ListFriendsAPIView.as_view()),
    path("add-friend/<str:user_name>", AddFriendAPIView.as_view()),
    path("remove-friend/<str:user_name>", RemoveFriendAPIView.as_view()),
    path("chat-friend/<str:user_name>", ChatFriendAPIView.as_view()),
    path("chat-group/<str:group_name>", ChatGroupAPIView.as_view()),
]
