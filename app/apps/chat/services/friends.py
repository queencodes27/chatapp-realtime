from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from apps.account.api.serializers import AccountNameSerializer
from apps.account.selectors import (
    get_user_friends_obj,
    get_user_or_raise_exception,
)
from apps.chat.selectors import get_user_friends


class FriendsService:
    @staticmethod
    def add_friend(friend_obj, user):
        """
        Add user to friends list

        :param Friends friend_obj: Friends object for adding a user
        :param User user: user to be added to the friends list

        :return: user' friend object
        :return: Friends
        """

        friend_obj.add_friend(user)
        return friend_obj

    @staticmethod
    def remove_friend(friend_obj, user):
        """
        Remove user to friends list

        :param Friends friend_obj: Friends object for removing a user
        :param User user: user to be removed to the friends list

        :return: user' friend object
        :return: Friends
        """

        friend_obj.remove_friend(user)
        return friend_obj

    @staticmethod
    def list_friends(user):
        return get_user_friends(user)

    @staticmethod
    def is_friends(user, other_user):
        return user.is_friends(other_user)


class ListFriendsService:
    @staticmethod
    def list(request):
        user = request.user
        friends = FriendsService().list_friends(user)
        return Response(
            AccountNameSerializer(friends, many=True).data,
            status=status.HTTP_200_OK,
        )


class AddFriendService:
    @staticmethod
    def add(request, user_name):
        user_account = request.user
        user_account_freinds_obj = get_user_friends_obj(user_account)
        friend_user_account = get_user_or_raise_exception(user_name)

        if friend_user_account in user_account_freinds_obj.friends.all():
            raise APIException("Your are a friend with this user")

        FriendsService().add_friend(
            user_account_freinds_obj, friend_user_account
        )
        return Response("Succussfly added friend")


class RemoveFriendService:
    @staticmethod
    def remove(request, user_name):
        user_account = request.user
        user_account_freinds_obj = get_user_friends_obj(user_account)
        friend_user_account = get_user_or_raise_exception(user_name)

        if friend_user_account not in user_account_freinds_obj.friends.all():
            raise APIException("You are not a friend with user name")

        FriendsService().remove_friend(
            user_account_freinds_obj, friend_user_account
        )
        return Response("Succussfly removed friend")
