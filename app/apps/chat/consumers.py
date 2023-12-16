import asyncio
import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.account.selectors import get_user_by_username, get_user_friends_obj
from apps.chat.api.serializers import (
    GroupMessageSerializer,
    UserMessageSerializer,
)
from apps.chat.models.chat import Chat
from apps.chat.selectors import (
    get_group_by_name,
    get_messages_by_chat_obj,
    get_messages_by_gruop,
)
from apps.chat.services.chat import GroupMessageSerive, UserMessageSerive
from apps.chat.services.friends import FriendsService


class GroupChatConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def get_messages(self, number=10):
        """
        Return the specified number of messages from the Group message,
        if number is not specified 10 is the default number
        """

        messages = get_messages_by_gruop(self.group)

        # get the number of messages to be parsed
        number = number if len(messages) > number else len(messages)

        # serialize messages
        serialized_messages = GroupMessageSerializer(
            messages[:number], many=True
        ).data

        # meta information about
        meta = {
            "meta": {
                "number_msgs": number,
                "has_more": len(messages) > number,
            }
        }
        return {"messages": serialized_messages, **meta}

    @database_sync_to_async
    def validate_connection(self):
        dis_msg = {"action": "disconect", "message": ""}

        # if group does not exists
        if self.group is None:
            dis_msg["message"] = "This group does not exists"
            async_to_sync(self.send)(json.dumps(dis_msg))
            async_to_sync(self.close)()

        # if user is not authenticated close the connection
        elif self.scope["user"].is_anonymous == True:
            dis_msg["message"] = "anonymous user connect to this group"
            async_to_sync(self.send)(json.dumps(dis_msg))
            async_to_sync(self.close)()

        # if group does not exists
        elif self.scope["user"] not in self.group.users.all():
            dis_msg["message"] = "You are not joined this group"
            async_to_sync(self.send)(json.dumps(dis_msg))
            async_to_sync(self.close)(json.dumps(dis_msg))

    @database_sync_to_async
    def get_group_chat(self, group):
        group_chat = Chat.objects.get_or_create_group_thread(group)
        return group_chat

    async def connect(self):
        group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.group = await sync_to_async(get_group_by_name)(group_name)
        self.group_chat = await self.get_group_chat(self.group)

        self.room_name = group_name
        self.room_group_name = self.group_chat.name

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
        await self.validate_connection()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        action = text_data_json.get("action")

        if action == "send_message":
            message = text_data_json.get("message")

            if message:
                await self.send_message_action(message)

        elif action == "retrieve_message":
            number = text_data_json.get("number")
            await self.retrieve_msgs_action(
                number if number is not None else 10
            )

    async def send_message_action(self, message):
        message = await sync_to_async(GroupMessageSerive().create_msg)(
            self.scope["user"],
            self.group,
            self.group_chat,
            message,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_message",
                "data": {
                    "message": GroupMessageSerializer(instance=message).data,
                },
            },
        )

    async def retrieve_msgs_action(self, number):
        messages = await self.get_messages(number)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "retrieve_message",
                "data": {
                    "action": "retrieve_message",
                    "data": messages,
                    "to_user": self.scope["user"].username,
                },
            },
        )

    async def send_message(self, data):
        await self.send_message_json(data["data"])

    async def retrieve_message(self, event):
        # return data for the user that request it
        if self.scope["user"].username == event["data"]["to_user"]:
            await self.send_message_json(event["data"])

    async def send_message_json(self, data):
        await self.send(text_data=json.dumps(data))


class UserChatConsumer(AsyncWebsocketConsumer):
    actions = ["send_message", "retrieve_msgs"]

    @database_sync_to_async
    def get_messages(self, number=10):
        """
        Return the specified number of messages from the Group message,
        if number is not specified 10 is the default number
        """

        messages = get_messages_by_chat_obj(self.user_chat)

        # get the number of messages to be parsed
        number = number if len(messages) > number else len(messages)

        # serialize messages
        serialized_messages = UserMessageSerializer(
            messages[:number], many=True
        ).data

        # meta information about
        meta = {
            "meta": {
                "number_msgs": number,
                "has_more": len(messages) > number,
            }
        }
        return {"messages": serialized_messages, **meta}

    @database_sync_to_async
    def get_user_chat(self, user, other_user):
        group_chat = Chat.objects.get_or_create_personal_thread(
            user, other_user
        )
        return group_chat

    async def connect(self):
        username = self.scope["url_route"]["kwargs"]["username"]
        self.other_user = await sync_to_async(get_user_by_username)(username)
        self.friends_obj = await sync_to_async(get_user_friends_obj)(
            self.scope["user"]
        )
        is_friends = await sync_to_async(FriendsService().is_friends)(
            self.friends_obj, self.other_user
        )

        if not self.other_user:
            await self.close()
        elif is_friends is False:
            await self.close()
        else:
            self.user_chat = await self.get_user_chat(
                self.scope["user"], self.other_user
            )

            self.room_name = self.user_chat.thread_id
            self.room_group_name = self.user_chat.name

            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
            await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get("action", None)

        if action == "send_message":
            message = text_data_json.get("message")
            if message:
                await self.send_message_action(text_data_json)
        elif action == "retrieve_message":
            number = text_data_json.get("number")
            await self.retrieve_message_action(
                number if number is not None else 10
            )

    async def send_message_action(self, message_text):
        message = await sync_to_async(UserMessageSerive().create_msg)(
            self.scope["user"],
            self.other_user,
            self.user_chat,
            message_text,
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_message",
                "message": UserMessageSerializer(instance=message).data,
            },
        )

    async def retrieve_message_action(self, number):
        messages = await self.get_messages(number)
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "retrieve_message", "data": messages},
        )

    async def retrieve_message(self, event):
        await self.send_message_json(event["data"])

    async def send_message(self, event):
        await self.send_message_json({"data": event["message"]})

    async def send_message_json(self, data):
        await self.send(text_data=json.dumps(data))
