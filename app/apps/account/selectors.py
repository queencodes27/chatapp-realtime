from django.contrib.auth.models import User
from rest_framework.exceptions import APIException

from .models import Friends


def get_user_or_raise_exception(username: str):
    """
    Get user by username, else raise exception

    :param str username: user' username

    :return: get associated user
    :rtype: User

    :raise: if user not found raise api exception
    :raisetype: APIException
    """
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise APIException("User can not be found")


def get_user_friends_obj(user):
    """
    Get user' friends object

    :param User user: friends' user

    :return: associated friends' user
    :rtype: Friends
    """

    return Friends.objects.get(user=user)


def get_user_by_username(username):
    """
    Get user by username

    :param str username: user' username

    :return: get associated user
    :rtype: User

    """
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None
