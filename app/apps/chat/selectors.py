from apps.account.models import Friends
from apps.chat.models import Group
from apps.chat.models.chat import GroupMessage, UserMessage


def get_group_by_name(name: str) -> Group | None:
    """
    Get group object by specifying the group name

    :param str name: object' group name

    :return: return the specified object group object or None
    :rtype: Group
    """

    try:
        return Group.objects.filter(name=name).first()
    except Group.DoesNotExist:
        return None


def get_user_friends(user):
    """
    Get all user friends

    :param User user:

    :return: return
    :rtype: QuerySet[User]
    """

    user_friends = Friends.objects.get(user=user)
    return user_friends.friends.all()


def get_messages_by_gruop(group):
    """
    Get all messages associated to one group

    :param Group group: group object to reference related messages

    :return: return all related group messages to the specified group
    :rtype: GroupMessage
    """

    messages = GroupMessage.objects.filter(group=group)
    return messages


def get_messages_by_chat_obj(chat):
    """
    Get all messages associated to chat obj

    :param Chat chat: chat object to reference related messages

    :return: return all related user messages to the specified chat
    :rtype: UserMessage
    """

    messages = UserMessage.objects.filter(chat=chat)
    return messages
