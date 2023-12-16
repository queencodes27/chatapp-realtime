from email.headerregistry import Group

from rest_framework.serializers import ModelSerializer

from apps.account.api.serializers import AccountNameSerializer
from apps.chat.models.chat import Chat, Group, GroupMessage, UserMessage


class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = ["name", "chat_type", "thread_id"]


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "users", "chat"]


class CreateGroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ["name"]


class GroupReadSerializer(ModelSerializer):
    chat = ChatSerializer()

    class Meta:
        model = Group
        fields = ["name", "users", "chat"]


class GroupMessageSerializer(ModelSerializer):
    from_user = AccountNameSerializer()

    class Meta:
        model = GroupMessage
        fields = ["id", "content", "timestamp", "from_user"]


class UserMessageSerializer(ModelSerializer):
    from_user = AccountNameSerializer()
    to_user = AccountNameSerializer()

    class Meta:
        model = UserMessage
        fields = ["id", "content", "timestamp", "from_user", "to_user"]
